import cv2

mask = cv2.imread('resources/blank.png')



i=30
j=30


def grid(img,i,j):
    for n in range(8):
        for b in range(8):
            cv2.circle(mask,(j,i),1,(0,0,255),3)
            j+=32
        j= 30
        i+=32
    
    cv2.imshow('r',mask)
    cv2.waitKey(0)

    cv2.imwrite('resources/newmask_2.png',mask)
    

grid(mask,i,j)
    
    

