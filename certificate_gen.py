from email.mime import image
from unittest.mock import patch
import cv2 as cv
import numpy as np
import os
import csv
from PIL import ImageFont,ImageDraw,Image


f1 = open("names.txt","r")
names_list = f1.read().split("\n")
# print(names_list)

f2 = open("coordinates.txt","r")
coordinates = f2.read().split("\n")
# print(coordinates)

flag = True

for i in range(len(names_list)):
    name_to_print = names_list[i]
    date_to_print = "20-09-2022"

    image = cv.imread("certificate.png")

    cv_im_rgb  = cv.cvtColor(image,cv.COLOR_BGR2RGB)

    pil_im = Image.fromarray(cv_im_rgb)

    draw = ImageDraw.Draw(pil_im)

    font1 = ImageFont.truetype("./Fonts/Lato-Black.ttf",28)
    
    font2 = ImageFont.truetype("./Fonts/Lato-Black.ttf",24)

    # Drawing text on certifcate

    draw.text((int(coordinates[0]),int(coordinates[1])),name_to_print,font=font1,fill='gold')
    draw.text((int(coordinates[2]),int(coordinates[3])),date_to_print,font=font2,fill='gold')


    cv_im_processed= cv.cvtColor(np.array(pil_im),cv.COLOR_RGB2BGR)

    if flag:
        cv.imshow('certificate',cv_im_processed)
        flag = False
    path= ''

    cv.imwrite('./printed_cert/'+name_to_print+'.png',cv_im_processed)

    cv.waitKey(0)

    cv.destroyAllWindows()



