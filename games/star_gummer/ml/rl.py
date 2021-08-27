import random
import numpy as np
import pickle
from keras.layers import Dense
from keras.models import Sequential

from easy_tf_log import tflog
from datetime import datetime
from keras import callbacks
import os

from karpathy import prepro, discount_rewards

class MLPlay:
    def __init__(self):
        print("Initial ml script")
        self.tik = False
        self.H = 200
        self.D = 8
        self.resume = False # resume from previous checkpoint?

        self.RIGHT_ACTION = 2
        self.LEFT_ACTION = 3
        self.RIGHT_ACTION = 2
        self.LEFT_ACTION = 3
        if self.resume:
            model = pickle.load(open('save.p', 'rb'))
        else:
            model = Sequential()
            model.add(Dense(units=200,input_dim=80*80, activation='relu', kernel_initializer='glorot_uniform'))
            model.add(Dense(units=1, activation='sigmoid', kernel_initializer='RandomNormal'))
            model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        self.gamma = 0.99 # discount factor for reward
        self.decay_rate = 0.99 # decay factor for RMSProp leaky sum of grad^2

        # initialization of variables used in the main loop
        self.x_train, self.y_train, self.rewards = [],[],[]
        self.reward_sum = 0
        self.episode_nb = 0

        # initialize variables
        self.running_reward = None
        self.epochs_before_saving = 10
        log_dir = './log' + datetime.now().strftime("%Y%m%d-%H%M%S") + "/"

        # load pre-trained model if exist
        if (self.resume and os.path.isfile('my_model_weights.h5')):
            print("loading previous weights")
            model.load_weights('my_model_weights.h5')
            
        # add a callback tensorboard object to visualize learning
        self.tbCallBack = callbacks.TensorBoard(log_dir=log_dir, histogram_freq=0,  
                write_graph=True, write_images=True)

    def getObs(player):
        observation = []
        observation.append(scene_info['ball'][0])
        observation.append(scene_info['ball'][1])
        observation.append(scene_info['ball_speed'][0])
        observation.append(scene_info['ball_speed'][1])
        observation.append(scene_info['blocker'][0])
        observation.append(scene_info['blocker'][1])
        
        observation = np.array(observation)
        return observation

    def move_to(x, pred) : #move platform to predicted position to catch ball 
        if x+20  > (pred-20) and x+20 < (pred+20): return 0 # NONE
        elif x+20 <= (pred-20) : return 1 # goes right
        else : return 2 # goes left
 

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        # print("AI received data from game :", scene_info)
        actions = ["SPEED", "BRAKE", "LEFT", "RIGHT"]
        up_down = ["SPEED", "BRAKE"]
        
        obstacle = []
        obstacle.extend(scene_info[0]['bullets'])
        obstacle.extend(scene_info[0]['meteor'])
        obstacle.extend(scene_info[0]['enemies'])

        obstacle = sorted(obstacle, key = lambda s: s[1], reverse=True)
        obstacle = sorted(obstacle, key = lambda s: s[0])
        pos = scene_info[0]['player']
        props = scene_info[0]['props']
        

        find = -1
        rm = []
        for i in obstacle:
            if i[0] != find:
                find = i[0]
            else:
                rm.append(i)
        for i in rm:
            obstacle.remove(i)
        obstacle_interval = []
        height = [] 
        try:
            obstacle_interval.append([obstacle[0][0]-0,0])
            height.append(obstacle[0][1])
            for i in range(len(obstacle)-1):
                obstacle_interval.append([obstacle[i+1][0] - obstacle[i][0], obstacle[i][0]])
                height.append(max(obstacle[i+1][1],obstacle[i][1]))
            obstacle_interval.append([600-obstacle[-1][0], obstacle[-1][0]])
            height.append(obstacle[-1][1])
        except:
            pass

        rect = []
        for i in range(len(obstacle_interval)):
            
            rect.append([obstacle_interval[i][0]+height[i], obstacle_interval[i][0], obstacle_interval[i][1], height[i], True if obstacle_interval[i][0] > 60 and height[i] else False])
        
        proba = self.model.predict(np.expand_dims(rect, axis=1).T)
        action = self.RIGHT_ACTION if np.random.uniform() < proba else self.LEFT_ACTION
        y = 1 if action == 2 else 0 # 0 and 1 are our labels

        self.x_train.append(rect)
        self.y_train.append(y)  

        if scene_info[0]['state'] == 'GAME_ALIVE':
            self.reward = 0
            self.done = False
        elif scene_info[0]['state'] == 'GAME_PASS':
            self.reward = 2
        elif scene_info[0]['state'] == 'GAME_OVER':
            self.reward = -1



        self.rewards.append(reward)
        self.reward_sum += reward      

        if self.done: # an episode finished
            print('At the end of episode', self.episode_nb, 'the total reward was :', self.reward_sum)

            # increment episode number
            self.episode_nb += 1
            
            # training
            self.model.fit(x=np.vstack(self.x_train), y=np.vstack(self.y_train), verbose=1, callbacks=[self.tbCallBack], sample_weight=discount_rewards(self.rewards, self.gamma))
            
            # Saving the weights used by our model
            if self.episode_nb % self.epochs_before_saving == 0:    
                self.model.save_weights('my_model_weights' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.h5')
            
            # Log the reward
            running_reward = self.reward_sum if self.running_reward is None else self.running_reward * 0.99 + self.reward_sum * 0.01
            tflog('running_reward', running_reward, custom_dir=self.log_dir)
            
            # Reinitialization
            self.x_train, self.y_train, self.rewards = [],[],[]
            self.reward_sum = 0


        if action == 2:
            return "RIGHT"
        else:
            return "LEFT"


    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass