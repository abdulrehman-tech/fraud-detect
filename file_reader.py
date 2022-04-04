
import cv2
import os
import pandas as pd
from PIL import Image
import os,io
import tkinter as tk
from tkinter import filedialog
from google.cloud import vision_v1
import gc
request = vision_v1.GetProductSetRequest(name="name")
from google.cloud.vision_v1 import types
# os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'coral-rider-336111-478563a957a9.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'coral-rider-336111-e27dddcddd3d.json'
client=vision_v1.ImageAnnotatorClient()


def reader():
    FILEOPENOPTIONS = dict(defaultextension=".jpg", filetypes=[('image files', '.png'),('image files', '.jpg'),])
    root = tk.Tk()
    root.withdraw()


    root.attributes("-topmost", True)
    file_path1 = filedialog.askopenfilename(**FILEOPENOPTIONS)
    root.attributes("-topmost", False)
    # root.attributes("-topmost", True)




# image = cv2.imread(file_path1)
#     print(file_path1)
#     if file_path1=='':
#         print(file_path1)
#         root.destroy()
#     else:
#         print(file_path1)


#         type(image)
#         cv2.imwrite('Email.jpg', image)

#         print('Image Saved')
#         filename = 'Email.jpg'


#         root.destroy()







    if file_path1 == '':
        # return
        root.mainloop()
    else:

        image = cv2.imread(file_path1)
        type(image)
        cv2.imwrite('Email.jpg', image)

        print('Image Saved')
        filename = 'Email.jpg'


        root.destroy()
    #cv2.imshow('Test image',image)
    #root.mainloop()
    with io.open('Email.jpg', 'rb') as image_file:
        content = image_file.read()
        image = vision_v1.types.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        for text in texts:
            txt = text.description
            return txt

            break





    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

   
    
     
    
   

