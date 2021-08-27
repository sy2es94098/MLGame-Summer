import random

class MLPlay:
    def __init__(self):
        print("Initial ml script")

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        # print("AI received data from game :", scene_info)
        actions = ["SPEED", "BRAKE", "LEFT", "RIGHT"]
        bullets = sorted(scene_info[0]['bullets'], key = lambda s: s[1], reverse=True)
        bullets = sorted(scene_info[0]['bullets'], key = lambda s: s[0])
        print("bef: ", bullets)
        print()
        find = -1
        rm = []
        for i in bullets:
            if i[0] != find:
                find = i[0]
            else:
                rm.append(i)
        print(rm)
        for i in rm:
            bullets.remove(i)

        print("aft: ", bullets)
        print()
        bullets_interval = []
        try:
            bullets_interval.append([bullets[0][0]-0,0])
            for i in range(len(bullets)-1):
                bullets_interval.append([bullets[i+1][0] - bullets[i][0], bullets[i][0]])
            bullets_interval.append([600-bullets[-1][0], bullets[-1][0]])
        except:
            pass
        #print(bullets_interval)
        return random.sample(actions, 1)

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass