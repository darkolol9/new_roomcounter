import cv2

mask = cv2.imread('resources/map3.png')
test = cv2.imread('resources/map2.png')


i=28
j=28


def grid(img,i,j):
    for n in range(8):
        for b in range(8):
            cv2.circle(mask,(j,i),2,(0,0,255),3)
            j+=32
        j= 28
        i+=32
    
    cv2.imshow('r',mask)
    dst = cv2.addWeighted(test,1,mask,0.7,0)
    cv2.imshow('result',dst)
    cv2.waitKey(0)

    cv2.imwrite('resources/newmask.png',mask)
    cv2.imwrite('resources/test.png',dst)

grid(mask,i,j)
    
    

