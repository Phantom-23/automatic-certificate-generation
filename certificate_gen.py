import cv2 as cv
import numpy as np
from PIL import ImageFont,ImageDraw,Image
from datetime import date
import os

current_dir = os.path.dirname(__file__)
data_folder_path = os.path.join(current_dir, 'data')

import coordinates_gen

def generate_certificates(names_list, certificate_template_name , PRINT_DATE = False):

    certificate_template_path = os.path.join(data_folder_path, certificate_template_name)

    gen_certificate_file_names = []

    coordinates_gen.generate_coordinates(certificate_template_name)

    coordinates_file_path = os.path.join(data_folder_path, 'coordinates.txt')

    f2 = open(coordinates_file_path,"r")
    coordinates = f2.read().split("\n")
    # print(coordinates)

    flag = True
    n = len(names_list)
    for i in range(n):
        name_to_print = names_list[i]

        if PRINT_DATE:
            date_to_print = date.today()
            date_to_print = date_to_print.strftime("%d/%m/%Y")

        image = cv.imread( certificate_template_path)

        cv_im_rgb  = cv.cvtColor(image,cv.COLOR_BGR2RGB)

        pil_im = Image.fromarray(cv_im_rgb)

        draw = ImageDraw.Draw(pil_im)

        font1 = ImageFont.truetype("./Fonts/Lato-Black.ttf",80)
        
        if PRINT_DATE:
            font2 = ImageFont.truetype("./Fonts/Lato-Black.ttf",24)

        # Drawing text on certifcate

        draw.text((int(coordinates[0]),int(coordinates[1])),name_to_print,font=font1,fill='black')
        if PRINT_DATE:
            draw.text((int(coordinates[2]),int(coordinates[3])),date_to_print,font=font2,fill='black')


        cv_im_processed= cv.cvtColor(np.array(pil_im),cv.COLOR_RGB2BGR)

        if flag:
            cv.imshow('certificate',cv_im_processed)
            flag = False

        name_for_filename = '_'.join(name_to_print.strip().split(' '))
        file_name = f'{name_for_filename}_{str(i + 1)}.png'
        path= f'./certificates/{file_name}'
        gen_certificate_file_names.append(file_name)

        cv.imwrite(path,cv_im_processed)

        cv.waitKey(0)

        cv.destroyAllWindows()

    return gen_certificate_file_names