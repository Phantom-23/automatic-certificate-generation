import cv2 as cv

file = open("coordinates.txt","w")

def set_coordinates(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.putText(img,"coordinates = (%d,%d)"%(x,y),(50,50),2,1,(0,0,0))
        file.write(str(x)+"\n")
        file.write(str(y)+"\n")


img = cv.imread("certificate.png")
cv.namedWindow('SETTING_COORDINATES')
cv.resizeWindow('SETTING_COORDINATES',100,100)
cv.setMouseCallback('SETTING_COORDINATES',set_coordinates)

while(1):
    cv.imshow('SETTING_COORDINATES',img)
    if cv.waitKey(10)& 0xFF ==13: #press enter to save changes
        break
cv.destroyAllWindows()

file.close()

###