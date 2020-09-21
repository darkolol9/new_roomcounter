import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract as ts
import datetime


img_exit = cv2.imread('resources/map_exit.png')
img_time = cv2.imread('resources/time.png',0)

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

def find_time():
    scrnshot = ImageGrab.grab()
    mat_scrnshot = np.array(scrnshot)
    img = cv2.cvtColor(mat_scrnshot,cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img,img_time,cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    time_left =  (max_loc[0]+18,max_loc[1]-39)
    time_right = (time_left[0]+70,time_left[1]+25)


    time_pic = np.array(ImageGrab.grab(bbox = (time_left[0],time_left[1],time_right[0],time_right[1]))) #first screenshot of map
    time_pic = cv2.bitwise_not(time_pic)
    time_pic = cv2.cvtColor(time_pic,cv2.COLOR_BGR2GRAY)
    #_,time_pic = cv2.threshold(time_pic,110,255,cv2.THRESH_BINARY)

    cv2.imshow('rsd',time_pic)
    cv2.waitKey(0)

    scale_percent = 250

    #calculate the 50 percent of original dimensions
    width = int(time_pic.shape[1] * scale_percent / 100)
    height = int(time_pic.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)

    # resize image
    time_pic = cv2.resize(time_pic, dsize)

    time_str = ts.image_to_string(time_pic,config='-c tessedit_char_whitelist=0123456789: -oem 0')
    time_str = time_str.replace(' ','')
    print(time_str)
    
    final_time = datetime.datetime.strptime(time_str, "%H:%M:%S")
    a_timedelta = final_time - datetime.datetime(1900, 1, 1)
    seconds = a_timedelta.total_seconds()
    return int(seconds)



find_time()



