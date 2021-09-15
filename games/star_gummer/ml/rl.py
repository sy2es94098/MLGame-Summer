from __future__ import print_function

import argparse
import skimage as skimage
from skimage import transform, color, exposure
from skimage.transform import rotate
from skimage.viewer import ImageViewer
import sys
import random
import numpy as np
from collections import deque
#import mlgame.global_variable as gv

import json
#from keras.initializers import normal, identity
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv2D , MaxPooling2D
from keras.optimizers import SGD , Adam
import tensorflow as tf

GAME = 'bird' # the name of the game being played for log files
CONFIG = 'nothreshold'
ACTIONS = 2 # number of valid actions
GAMMA = 0.99 # decay rate of past observations
OBSERVATION = 3200. # timesteps to observe before training
EXPLORE = 3000000. # frames over which to anneal epsilon
FINAL_EPSILON = 0.0001 # final value of epsilon
INITIAL_EPSILON = 0.1 # starting value of epsilon
REPLAY_MEMORY = 50000 # number of previous transitions to remember
BATCH = 32 # size of minibatch
FRAME_PER_ACTION = 1
LEARNING_RATE = 1e-4
LOAD = True
RUN = False

img_rows , img_cols = 80, 80
#Convert image into Black and white
img_channels = 4 #We stack 4 frames


def buildmodel():
    print("Now we build the model")
    model = Sequential()
    model.add(Conv2D (32, 8, 4, padding ='same',input_shape=(img_rows,img_cols,img_channels)))  #80*80*4
    model.add(Activation('relu'))
    model.add(Conv2D (64, 4, 2, padding ='same'))
    model.add(Activation('relu'))
    model.add(Conv2D (64, 3, 1, padding ='same'))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(2))
    
    adam = Adam(lr=LEARNING_RATE)
    model.compile(loss='mse',optimizer=adam)
    print("We finish building the model")
    return model


    

class MLPlay:
    def __init__(self):
        print("Initial ml script")
        self.model = buildmodel()
        self.D = deque()
        self.actions = ["LEFT", "RIGHT"]
        self.t = 0
        self.fist = True
        self.pixels = np.zeros(360000, dtype=np.int)
        if LOAD:
            print ("Now we load weight")
            self.model.load_weights("model.h5")
            adam = Adam(lr=LEARNING_RATE)
            self.model.compile(loss='mse',optimizer=adam)
            print ("Weight load successfully")    

    def convert_rgb(self, hex_s):
        data = []
        for i in range(3):
            hex = "0x" + hex_s[2*i+1:2*i+3]
            num = int(hex,16)
            data.append(num)
        return sum(data)

    def fill_rect_pixels(self, data):
        init_coor = data['y'] * 600 + data['x']
        c = ""
        try:    
            c = self.convert_rgb(data['color'])
        except:
            c = self.convert_rgb("#AAAAAA")
        for i in range(data["height"]):
            for j in range(data["width"]):
                try:
                    self.pixels[i*600 + init_coor+j] = c
                except:
                    pass

    def get_pixels(self,info):
        self.pixels = np.zeros(360000, dtype=np.int)
        self.fill_rect_pixels(info['player'])
        try:
            self.fill_rect_pixels(info['boss'])
        except:
            pass

        for e in info["enemies"]:
            self.fill_rect_pixels(e)

        for b in info["bullets"]:
            self.fill_rect_pixels(b)

        for m in info["meteor"]:
            self.fill_rect_pixels(m)

        for p in info["props"]:
            self.fill_rect_pixels(p)

        return self.pixels


    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        if RUN:
            OBSERVE = 999999999    #We keep observe, never train
            epsilon = FINAL_EPSILON
        else:
            OBSERVE = OBSERVATION
            epsilon = INITIAL_EPSILON
        # print("AI received data from game :", scene_info)
        #print(scene_info[0]['pixels'])
        if scene_info[0] == []:
            return
    
        if self.fist:
            x_t = self.get_pixels(scene_info[0])
            x_t = np.array(x_t)
            x_t = np.reshape(x_t,(600, 600))

            x_t = skimage.transform.resize(x_t,(80,80))
            x_t = skimage.exposure.rescale_intensity(x_t,out_range=(0,255))

            x_t = x_t / 255.0

            self.st = np.stack((x_t, x_t, x_t, x_t), axis=2)
            self.st = self.st.reshape(1, self.st.shape[0], self.st.shape[1], self.st.shape[2])  #1*80*80*4

            r_t = scene_info[0]['reward']
            terminal = False if scene_info[0]['state'] == "GAME_ALIVE" else True
            self.fist = False
        else:
            loss = 0
            Q_sa = 0
            action_index = 0
            r_t = 0
            a_t = 0
        
            if self.t % FRAME_PER_ACTION == 0:
                if random.random() <= epsilon:
                    #print("----------Random Action----------")
                    action_index = random.randrange(ACTIONS)
                    a_t = action_index
                else:
                    q = self.model.predict(self.st)       #input a stack of 4 images, get the prediction
                    max_Q = np.argmax(q)
                    action_index = max_Q
                    a_t = max_Q

            #We reduced the epsilon gradually
            if epsilon > FINAL_EPSILON and self.t > OBSERVE:
                epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

            #run the selected action and observed next state and reward


            x_t1 = self.get_pixels(scene_info[0])

            x_t1 = np.array(x_t1)
            x_t1 = np.reshape(x_t1,(600, 600))

            x_t1 = skimage.transform.resize(x_t1,(80,80))
            x_t1 = skimage.exposure.rescale_intensity(x_t1, out_range=(0, 255))
            x_t1 = x_t1 / 255.0
            x_t1 = x_t1.reshape(1, x_t1.shape[0], x_t1.shape[1], 1) #1x80x80x1
            s_t1 = np.append(x_t1, self.st[:, :, :, :3], axis=3)

            r_t = scene_info[0]['reward']
            terminal = False if scene_info[0]['state'] == "GAME_ALIVE" else True

            # store the transition in D
            self.D.append((self.st, action_index, r_t, s_t1, terminal))
            if len(self.D) > REPLAY_MEMORY:
                self.D.popleft()

            #only train if done observing
            if self.t > OBSERVE:
                #sample a minibatch to train on
                minibatch = random.sample(self.D, BATCH)

                #Now we do the experience replay
                state_t, action_t, reward_t, state_t1, terminal = zip(*minibatch)
                state_t = np.concatenate(state_t)
                state_t1 = np.concatenate(state_t1)
                targets = self.model.predict(state_t)
                Q_sa = self.model.predict(state_t1)
                targets[range(BATCH), action_t] = reward_t + GAMMA*np.max(Q_sa, axis=1)*np.invert(terminal)

                loss += self.model.train_on_batch(state_t, targets)

            self.st = s_t1
            self.t = self.t + 1

            # save progress every 10000 iterations
            if self.t % 1000 == 0:
                print("Now we save model")
                self.model.save_weights("model.h5", overwrite=True)
                with open("model.json", "w") as outfile:
                    json.dump(self.model.to_json(), outfile)

            # print info
            state = ""
            if self.t <= OBSERVE:
                state = "observe"
            elif self.t > OBSERVE and self.t <= OBSERVE + EXPLORE:
                state = "explore"
            else:
                state = "train"

            print("TIMESTEP", self.t, "/ STATE", state, \
                "/ EPSILON", epsilon, "/ ACTION", action_index, "/ REWARD", r_t, \
                "/ Q_MAX " , np.max(Q_sa), "/ Loss ", loss)
            return self.actions[a_t]

        #return "RIGHT"
        

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
