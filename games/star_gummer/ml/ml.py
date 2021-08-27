import random

class MLPlay:
    def __init__(self):
        print("Initial ml script")
        self.tik = False

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

        locate = []
        try:
            locate = max(rect, key = lambda s:  s[0] if s[4] == True else 0)
        except:
            pass

        if len(locate) > 0:   
            props = sorted(props, key = lambda s: s[1], reverse=True)      
            x_coor = locate[2] + locate[1]/2
            ob = False
            if pos[0] < x_coor:
                for i in rect:
                    if i[2] > pos[0] and i[2] < locate[0]:
                        if i[3]+40 > pos[1]:
                            ob = True
                if not ob:
                    return "RIGHT"
                else:
                    if len(props) > 0:
                        if pos[1] < props[0][1]:
                            return"BRAKE"
                        else:
                            return "SPEED"
                    else:
                        if pos[1] < 450:
                            return "BRAKE"
                        else:    
                            self.tik = not self.tik
                            return "SPEED" if self.tik else "BRAKE"
            else:
                for i in rect:
                    if i[2] > locate[0]  and i[2] < pos[0]:
                        if i[3]+40 > pos[1]:
                            ob = True
                if not ob:
                    return "LEFT"
                else:
                    if len(props) > 0:
                        if pos[1] < props[0][1]:
                            return"BRAKE"
                        else:
                            return "SPEED"
                    else:
                        if pos[1] < 450:
                            return "BRAKE"
                        else:    
                            self.tik = not self.tik
                            return "SPEED" if self.tik else "BRAKE"
        else:
            if len(props) > 0:
                if props[0][1] > 300:
                    if pos[1] < props[0][1]-20 and pos[1] > props[0][1]+20:
                        if pos[0] < props[0][0]:
                            return "RIGHT"
                        else:
                            return "LEFT"
                    elif pos[1] < props[0][1]:
                        return "BRAKE"
                    else:
                        return "SPEED"
            else:
                if pos[1] < 450:
                    return "BRAKE"
                else:    
                    return "SPEED"

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass