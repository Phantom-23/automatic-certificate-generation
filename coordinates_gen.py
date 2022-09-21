import cv2 as cv
import os

current_dir = os.path.dirname(__file__)
data_folder_path = os.path.join(current_dir, 'data//')

def generate_coordinates(certificate_template_filename):

    coordinates_file_path = os.path.join(data_folder_path, 'coordinates.txt')
    file = open(coordinates_file_path,"w")

    def set_coordinates(event,x,y,flags,param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            cv.putText(img,"coordinates = (%d,%d)"%(x,y),(50,50),2,1,(0,0,0))
            file.write(str(x)+"\n")
            file.write(str(y)+"\n")

    certificate_template_path = os.path.join(data_folder_path, certificate_template_filename)
    img = cv.imread(certificate_template_path)
    cv.namedWindow('SETTING_COORDINATES')
    cv.resizeWindow('SETTING_COORDINATES',100,100)
    cv.setMouseCallback('SETTING_COORDINATES',set_coordinates)

    while(1):
        cv.imshow('SETTING_COORDINATES',img)
        if cv.waitKey(10)& 0xFF ==13: #press enter to save changes
            break
    cv.destroyAllWindows()

    file.close()