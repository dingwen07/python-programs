import numpy
import cv2


img = cv2.imread("<image>",cv2.IMREAD_UNCHANGED)
cv2.namedWindow('img',cv2.WINDOW_AUTOSIZE)
cv2.imshow("img",img)
cv2.waitKey(0)
print(img.shape)

img[427:478,146:492] = (0,0,255)
cv2.imshow("img",img)
cv2.waitKey(0)

cv2.putText(img,"TEST",(150,470),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
cv2.imshow("img",img)
cv2.waitKey(0)