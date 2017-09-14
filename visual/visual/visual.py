
#coding: utf-8

import numpy as np
import cv2

x1 = 10
x2 = 20
x3 = 70
x4 = 50
y1 = 5
y2 = 30
y3 = 20
y4 = 10

g1 = (x1+x2+x3+x4)/4.0
g2 = (y1+y2+y3+y4)/4.0

print (str(g1))
print(str(int(g1)))

gt1 = str(int(g1))
gt2 = str(int(g2))

# Create a black image
img = np.zeros((512,512,3), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
img = cv2.line(img,(0,0),(511,511),(255,0,0),5)

pts = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4]], np.int32)
pts = pts.reshape((-1,1,2))
img = cv2.polylines(img,[pts],True,(0,255,255))

pts = np.array([[20,30],[60,50],[50,80],[30,80]], np.int32)
pts = pts.reshape((-1,1,2))
img = cv2.polylines(img,[pts],True,(0,255,255))

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'0',(int(g1),int(g2)), font, 4,(255,255,255),2,cv2.LINE_AA)


cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()