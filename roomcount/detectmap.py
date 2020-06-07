import cv2
import numpy as np
from PIL import ImageGrab


img_exit = cv2.imread('resources/map_exit.png')

def find_map_loc():
    scrnshot = ImageGrab.grab()
    mat_scrnshot = np.array(scrnshot)
    img = cv2.cvtColor(mat_scrnshot,cv2.COLOR_BGR2RGB)

    res = cv2.matchTemplate(img,img_exit,cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    map_left =  (max_loc[0]-265,max_loc[1])
    map_right = (map_left[0]+281,map_left[1]+281)
    

    print(max_loc)
    return map_left

