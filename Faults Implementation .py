#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import filters
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
import random
from tabulate import tabulate
import ipywidgets as wdg
from IPython.display import display


# In[2]:


def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])


# In[13]:


def gauss_blur(image_1):
    im1 = np.array(image_1)
    gray = cv2.cvtColor(im1,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5),0)
    blr_img = filters.gaussian(blur, sigma=1, mode='constant', cval=0.0)
    return(blr_img)


# In[14]:


def contrast(image_2, parameter_2):
    im2 = ImageEnhance.Contrast(image_2)
    im2 = im2.enhance(parameter_2)
    return(im2)


# In[15]:


def colour(image_5,parameter_5):
    im5 = ImageEnhance.Colour(image_5)
    im5 = im5.enhance(parameter_5)
    return(im5)


# In[16]:


def sharpness(image_4,parameter_4):
    im4 = ImageEnhance.Sharpness(image_4)
    im4 = im4.enhance(parameter_4)
    return(im4)


# In[17]:


def sp_noise(image,parameter_6):
    image_6 = np.array(image)
    noise_img = np.zeros(image_6.shape,np.uint8)
    thres = 1 - parameter_6
    for i in range(image_6.shape[0]):
        for j in range(image_6.shape[1]):
            rdn = random.random()
            if rdn < parameter_6:
                noise_img[i][j] = 0
            elif rdn > thres:
                noise_img[i][j] = 255
            else:
                noise_img[i][j] = image_6[i][j]
    return noise_img


# In[18]:


def brightness(image_3,parameter_3):
    im3 = ImageEnhance.Brightness(image_3)
    im3 = im3.enhance(parameter_3)
    return(im3)


# In[43]:


def rain_drop_blur(image_7,parameter_7):
    image_cpy = image_7.copy()
    blurred_image = image_cpy.filter(ImageFilter.GaussianBlur(radius=10))
    rain_drop_img = image_7.copy()
    size = (image_7.size)

    for i in range(0,parameter_7):
        p1 = random.randint(0, size[0])
        p2 = random.randint(0, size[1])
        #print(p1, p2)

        mask_im = Image.new("L", image_cpy.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((p1, p2, p1+65, p2+65), fill=255)
        #mask_im.save('mask_circle.jpg', quality=95)
        
    
        rain_drop_img.paste(blurred_image, (0, 0), mask_im)
    #mask_im.show()
    #rain_drop_img.show()
    return(rain_drop_img)


# In[20]:


def weather(foreground, image_8, size_8):
    image_8 = image_8.resize(size,Image.ANTIALIAS)
    foreground = foreground.resize(size_8,Image.ANTIALIAS)
    #print(image_8.size)
    image_8.paste(foreground, (0, 0), foreground)
    return(image_8)


# In[4]:


img_car = Image.open(r"D:\Uni-Siegen\4th Sem (SS 2022)\Arbeit\Trust-E\Error code\Test image.jpg")
size = (img_car.size)

for_img_1  = Image.open(r"D:\Uni-Siegen\4th Sem (SS 2022)\Arbeit\Trust-E\Error code\Error Injection images\rain_2.png")
for_img_2  = Image.open(r"D:\Uni-Siegen\4th Sem (SS 2022)\Arbeit\Trust-E\Error code\Error Injection images\dirt.png")
for_img_3  = Image.open(r"D:\Uni-Siegen\4th Sem (SS 2022)\Arbeit\Trust-E\Error code\Error Injection images\rain_1.png")
for_img_4  = Image.open(r"D:\Uni-Siegen\4th Sem (SS 2022)\Arbeit\Trust-E\Error code\Error Injection images\crack_1.png")
for_img_5  = Image.open(r"D:\Uni-Siegen\4th Sem (SS 2022)\Arbeit\Trust-E\Error code\Error Injection images\crack_2.png")
for_img_6  = Image.open(r"D:\Uni-Siegen\4th Sem (SS 2022)\Arbeit\Trust-E\Error code\Error Injection images\fog.png")
for_img_7  = Image.open(r"D:\Uni-Siegen\4th Sem (SS 2022)\Arbeit\Trust-E\Error code\Error Injection images\dirt_2.png").convert("RGBA")
for_img_8  = Image.open(r"D:\Uni-Siegen\4th Sem (SS 2022)\Arbeit\Trust-E\Error code\Error Injection images\snow-jesuit-spiritual-center-milford-13.png").convert("RGBA")
for_img_9  = Image.open(r"D:\Uni-Siegen\4th Sem (SS 2022)\Arbeit\Trust-E\Error code\Error Injection images\dust-overlay-4.png")
for_img_10 = Image.open(r"D:\Uni-Siegen\4th Sem (SS 2022)\Arbeit\Trust-E\Error code\Error Injection images\804-8047958_fog-png-for-picsart.png")


# In[12]:


# print('The following Faults can be injected:\n')

# table = [[1,'Gaussian Blur'],[2, 'Contrast'],[3,'Brightness'],[4,'Sharpness'],[5,'Colour'],[6,'Salt Pepper Noise'],[7,'Rain Drop Blur']
#          ,[8,'Snow'],[9,'Mud splash'],[10,'Rain'],[11,'Shatterd Glass'],[12,'Glass crack'],[13,'Smog'],[14,'Dirt']
#          ,[15,'Dense Fog'],[16,'Dust'],[17,'Light Fog']]
# header = ["Sr Number", "Fault"]
# print(tabulate(table, header))


# In[5]:


print('Select the Fault to be injected: ')
display_fault = wdg.Dropdown(
    options=[('Gaussian Blur', 1), ('Contrast', 2), ('Brightness', 3), ('Sharpness', 4), ('Colour', 5), ('Salt Pepper Noise', 6),
             ('Rain Drop Blur', 7), ('Snow', 8), ('Mud splash', 9), ('Rain', 10), ('Shatterd Glass', 11), ('Glass crack', 12),
             ('Smog', 13), ('Dirt', 14), ('Dense Fog', 15), ('Dust', 16), ('Light Fog', 17)],
    value = 1,
    description='Fault:',
)
display(display_fault)


# In[6]:


number = display_fault.value


# In[7]:


#number = int(input('Enter the Sr Number of the Fault to be injected: '))
num_range = range(2, 7, 1)


# In[8]:


if number in num_range:
    print('Enter the level of intensity of fault to be injected: ')
    Intensity_level = wdg.IntSlider(value=0,
                              min=0,
                              max=10,
                              step=1,
                              description='Intensity:',
                              disabled=False,
                              continuous_update=False,
                              orientation='horizontal',
                              readout=True,
                            readout_format='d')
    
    display(Intensity_level)


# In[33]:


if number == 7:
    print('Enter the number of water droplets to be injected: ')
    Intensity_level = wdg.IntSlider(value=0,
                              min=0,
                              max=500,
                              step=1,
                              description='Number:',
                              disabled=False,
                              continuous_update=False,
                              orientation='horizontal',
                              readout=True,
                            readout_format='d')
    
    display(Intensity_level)


# In[44]:


intensity_val = int(Intensity_level.value)


# In[45]:


functions = [0,gauss_blur,contrast,brightness,sharpness,colour,sp_noise,rain_drop_blur,weather,weather,weather,weather,weather,weather,weather,weather,weather,weather]
img_idx = [0,0,0,0,0,0,0,0,for_img_1,for_img_2,for_img_3,for_img_4,for_img_5,for_img_6,for_img_7,for_img_8,for_img_9,for_img_10]

#func_dic = {1:[gauss_blur,img_car], 2:[contrast,img_car],3:[brightness,img_car], 4: }


# In[50]:


if number == 1:
    output = functions[number](img_car)
    cv2.imshow("Blurred Image", output)
    cv2.waitKey(0)   
elif number in num_range:
    output = functions[number](img_car,intensity_val)
    output.show()
elif number == 7:
    output = functions[number](img_car,intensity_val)
    output = output.save("test10.jpg")
    #output.show()
else:
    output = functions[number](img_idx[number], img_car, size)
    output.show()
    output = output.save("test5.jpg")


# In[51]:


pwd


# In[ ]:




