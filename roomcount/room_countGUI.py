import cv2
import numpy as np
from PIL import ImageGrab
import os
import detectmap
from sys import exit
from datetime import datetime


import tkinter as tk

img2 = cv2.imread('resources/newmask_1.png') #mask tool
template = cv2.imread('resources/masked_4.png') #masked single room
mark_flag = False
count =0

print('loaded resources successfully! begining to count rooms..\n')
def capture():
	xloc = root.winfo_x()
	yloc = root.winfo_y()
	
	scrnshot = ImageGrab.grab(bbox = (xloc,yloc,xloc+282,yloc+285)) 
	formatted_scrnsht = np.array(scrnshot)

	img = cv2.cvtColor(formatted_scrnsht, cv2.COLOR_BGR2RGB) 
	time = datetime.now().time()
	time = str(time)[6:]

	path = time+'.png'
	cv2.imwrite('screenshots/'+path,img)
	print(f'saved new file: {path}')


def hide_bar(root,b):
	map_loc = detectmap.find_map_loc()
	xloc = map_loc[0]
	yloc = map_loc[1]
	xlocstr = str(xloc)
	ylocstr = str(yloc-4)
	root.overrideredirect(1)
	root.geometry('+'+xlocstr+'+'+ylocstr)
	#b.pack_forget()
	
	mark_flag = True
	text_cv = tk.Canvas(root,height=20,width = 281,bg = 'grey')
	text_cv.pack()
	w = tk.Label(text_cv, text='0',background ='gray',fg='white',font='helvetica 8')
	w.pack()
	

	root.wm_attributes("-transparentcolor", "yellow")
	countrooms(seconds,root,canvas,w)


def countrooms(seconds,root,canvas,w):
	

	count =0
	xloc = root.winfo_x()
	yloc = root.winfo_y()
	
	scrnshot = ImageGrab.grab(bbox = (xloc,yloc+1,xloc+282,yloc+283)) #first screenshot of map
	
	formatted_scrnsht = np.array(scrnshot)

	img = cv2.cvtColor(formatted_scrnsht, cv2.COLOR_BGR2RGB)  
	cv2.imwrite('scrn.png',img)

	dst = cv2.addWeighted(img,1,img2,0.7,0) #0.7
	cv2.imwrite('weigghted.png',dst)  #mask the screenshot
	threshold = 0.998 #accuracy threshold 997 was working fine

	res = cv2.matchTemplate(dst,template,cv2.TM_CCORR_NORMED) #find the matches
	loc = np.where(res >= threshold)

	for pt in zip(*loc[::-1]): #count
		count = count + 1
		canvas.create_rectangle(pt[0]-8,pt[1]-6,pt[0]+16,pt[1]+16,outline='red')

	if count == 0:
		seconds = 0 
		canvas.delete("all")
	else:
		try:
			seconds = detectmap.find_time()
		except:
			seconds = 1

	rpm =0

	if seconds !=0:
		rpm = (count/ (seconds/60))

	rpm_string = "{:.2f}".format(rpm)
	estimated_time = 'N/A'

	if rpm != 0:
		estimated_time = "{:.2f}".format(57/rpm)
	else:
		estimated_time = 'N/A'	

	seconds_str = str(seconds)	

	roomsleft1 = str(64 - count)
	roomsleft2 = str(50-count)	

	string = 'Rooms open: ' + str(count) + '| RPM: '  +  rpm_string + "| (estimated end time: " + estimated_time + ")" 
	#print(string)

	w.config(text = string)
	root.after(1000,countrooms,seconds,root,canvas,w)




root = tk.Tk()
root.geometry("281x330")
root.title('room counter')


root.overrideredirect(0)
root.configure(background='grey')

canvas = tk.Canvas(root,height=281,width = 281,bg = 'yellow')
canvas.delete("all")
canvas.pack()

b = tk.Button(root,text='find map',command = lambda: hide_bar(root,b))
exit_b = tk.Button(root,text='exit',command=exit)
exit_b.place(x=0,y=284)
capture_b = tk.Button(root,text='save',command=capture)
capture_b.place(x=250,y=284)
b.pack()



seconds = 0

	
#root.attributes('-alpha', 0.3)
root.call('wm', 'attributes', '.', '-topmost', '1')  


root.mainloop()
