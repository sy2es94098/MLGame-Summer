import os
import pickle
import numpy as np
from sklearn.model_selection import train_test_split

path = "games\star_gummer\log"

def transformCommand(command):
    if 'RIGHT' in str(command):
       return 2
    elif 'LEFT' in str(command):
        return 1
    else:
        return 0

def fill(arr, num):
  if(len(arr) < num):
    for i in range(num-len(arr)):
      arr.append([-1,-1])
  else:
    arr = arr[:num]
  return arr

def get_data(log):
  frames = []
  bullets = []
  meteor = []
  commands = []
  playerPos = []


  for scene_info in log['scene_info']:
    frames.append(scene_info[0]['frames'])
    b_arr = fill(scene_info[0]['bullets'],15)
    if len(b_arr)  != 15:
      print(len(b_arr))
    bullets.append(b_arr)
    m_arr = fill(scene_info[0]['meteor'],6)
    if len(m_arr)  != 6:
      print(len(m_arr))
    meteor.append(m_arr)
    playerPos.append(scene_info[0]['player'])

  for comm in log['command']:
    try:
      commands.append(comm[0])
    except:
      commands.append("None")

  commands_ary = np.array(commands)
  commands_ary = commands_ary.reshape((len(commands), 1))
  frame_ary = np.array(frames)
  frame_ary = frame_ary.reshape((len(frames), 1))
  b_arr = np.array(bullets)
  b_arr = b_arr.reshape(len(b_arr),-1)
  m_arr = np.array(meteor)
  m_arr = m_arr.reshape(len(m_arr),-1)
  data = np.hstack((frame_ary, playerPos, b_arr, m_arr, commands_ary))
  print(data.shape)
  return data



  



files = os.listdir(path)
for file in files:
  # 產生檔案的絕對路徑
  fullpath = os.path.join(path, file)
  # 判斷 fullpath 是檔案還是目錄
  if os.path.isfile(fullpath):
    data = None
    with open(fullpath, 'rb') as f:
      data = pickle.load(f)
    all_data = get_data(data['1P'])
    all_data=all_data[1::]
    mask = [n for n in range(1,45)]

    x = all_data[:,mask]
    Y = all_data[:-1]
    




    #print(len(data['1P']['scene_info']))

  