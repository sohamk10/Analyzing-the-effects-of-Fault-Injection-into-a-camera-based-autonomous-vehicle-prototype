#!/usr/bin/env python
# coding: utf-8

# # Road Following Live (with camera)

# In[1]:


from adafruit_servokit import ServoKit
import time


kit=ServoKit(channels=16) # using the PCA9685 we can control up to 16-PWD devices
kit.frequency = 60 # frequency of all PCA9685 16-PWD channels
kit.servo[7].actuation_range = 1 #set the range of the selectable devices  0 or 1 according to our mux we have two
kit.servo[7].angle = 1


# In[1]:


from matplotlib import pyplot as plt
from skimage import filters
import random
import cv2
import traitlets
import numpy as np
from IPython.display import display
from jetcam.utils import bgr8_to_jpeg
from jupyter_clickable_image_widget import ClickableImageWidget
import ipywidgets.widgets as widgets
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
import torch
from torch2trt import TRTModule
import ipywidgets
from ipywidgets import Layout, Button, Box
#from jetcam.utils import bgr8_to_jpeg


# Load the optimized model (created with the [`optimize_model.ipynb` notebook](./optimize_model.ipynb)) executing the cell below

# In[3]:


model_trt = TRTModule()
model_trt.load_state_dict(torch.load('DD.pth'))


from jetracer.nvidia_racecar import NvidiaRacecar
car = NvidiaRacecar()


from jetcam.usb_camera import USBCamera
camera = USBCamera(width=224, height=224, capture_width=640, capture_height=480, capture_device=2)
camera.running = True


# In[4]:


steerings_ab = []


# In[5]:


import threading
state_widget = ipywidgets.ToggleButtons(options=['On', 'Off'], description='Camera', value='On')
prediction_widget = ipywidgets.Image(format='jpeg', width=camera.width, height=camera.height)
i_widget = ipywidgets.Image(description='Image' , width=camera.width, height=camera.height)


live_execution_widget = ipywidgets.HBox([
    prediction_widget,i_widget,
    state_widget
])

e1 = ipywidgets.Checkbox(
    value=False,
    description='Gaussian Blur',
    disabled=False
    , layout={'width': '300px'})
e2 = ipywidgets.Checkbox(
    value=False,
    description='Contrast',
    disabled=False
    , layout={'width': '300px'})
e3 = ipywidgets.Checkbox(
    value=False,
    description='Brightness',
    disabled=False
    , layout={'width': '300px'})
e4 = ipywidgets.Checkbox(
    value=False,
    description='Sharpness',
    disabled=False
, layout={'width': '300px'})
e5 = ipywidgets.Checkbox(
    value=False,
    description='Colour',
    disabled=False
, layout={'width': '300px'})
e6 = ipywidgets.Checkbox(
    value=False,
    description='Salt Pepper Noise',
    disabled=False
, layout={'width': '300px'})
e7 = ipywidgets.Checkbox(
    value=False,
    description='Rain Drop Blur',
    disabled=False
, layout={'width': '300px'})
e8 = ipywidgets.Checkbox(
    value=False,
    description='Mud splash',
    disabled=False
, layout={'width': '300px'})
e9 = ipywidgets.Checkbox(
    value=False,
    description='Shatterd Glass',
    disabled=False
    , layout={'width': '300px'})
e10 = ipywidgets.Checkbox(
    value=False,
    description='Glass crack',
    disabled=False
    , layout={'width': '300px'})
e11 = ipywidgets.Checkbox(
    value=False,
    description='Dirt',
    disabled=False
    , layout={'width': '300px'})
e12 = ipywidgets.Checkbox(
    value=False,
    description='Dust',
    disabled=False
, layout={'width': '300px'})
e13 = ipywidgets.Checkbox(
    value=False,
    description='Smog',
    disabled=False
, layout={'width': '300px'})
e14 = ipywidgets.Checkbox(
    value=False,
    description='Snow',
    disabled=False
, layout={'width': '300px'})
e15 = ipywidgets.Checkbox(
    value=False,
    description='Rain',
    disabled=False
, layout={'width': '300px'})
e16 = ipywidgets.Checkbox(
    value=False,
    description='Dense Fog',
    disabled=False
, layout={'width': '300px'})
e17 = ipywidgets.Checkbox(
    value=False,
    description='Light Fog',
    disabled=False
, layout={'width': '300px'})



slider1 = widgets.IntSlider(description='Intensity', min=-10, max=10, value=0, step=1, orientation='horizontal', layout={'width': '300px'})
slider2 = widgets.IntSlider(description='Intensity', min=-10, max=10, value=0, step=1, orientation='horizontal', layout={'width': '300px'})
slider3 = widgets.IntSlider(description='Intensity', min=-10, max=10, value=0, step=1, orientation='horizontal', layout={'width': '300px'})
slider4 = widgets.IntSlider(description='Intensity', min=-10, max=10, value=0, step=1, orientation='horizontal', layout={'width': '300px'})
slider5 = widgets.IntSlider(description='Intensity', min=-10, max=10, value=0, step=1, orientation='horizontal', layout={'width': '300px'})
slider6 = widgets.FloatSlider(description='Intensity', min=0, max=1, value=0, step=0.1, orientation='horizontal', layout={'width': '300px'})
slider7 = widgets.IntSlider(description='Intensity', min=0, max=500, value=0, step=10, orientation='horizontal', layout={'width': '300px'})

a = ipywidgets.VBox([e1,e2,e3,e4,e5,e6,e7])
b = ipywidgets.VBox([slider1,slider2,slider3,slider4,slider5,slider6,slider7])
c = ipywidgets.HBox([e8,e9,e10])
d = ipywidgets.HBox([e11,e12,e13])
e = ipywidgets.HBox([e14,e15,e16])
f = ipywidgets.HBox([e17])

steer = widgets.FloatText(
    value=0,
    description='Steering:',
    disabled=False,
    layout={'width': '200px'}
)

error_steer = widgets.FloatText(
    value=0,
    description='Steering Deviation:',
    disabled=False,
    layout={'width': '200px'}
)

network_output_slider = widgets.FloatSlider(description='Network Output', min=-1.0, max=1.0, value=0, step=0.01, orientation='vertical', disabled=False, layout={'width': '100px'})
steering_gain_slider  = widgets.FloatSlider(description='Steering Gain', min=-1.0, max=1.0, value=1.0, step=0.01, orientation='vertical', layout={'width': '100px'})
steering_bias_slider  = widgets.FloatSlider(description='Steering Bias', min=-0.5, max=0.5, value=0.0, step=0.01, orientation='vertical', layout={'width': '100px'})
steering_value_slider = widgets.FloatSlider(description='Steering', min=-1.0, max=1.0, value=0, step=0.01, orientation='vertical', disabled=False, layout={'width': '100px'})
throttle_slider = widgets.FloatSlider(description='Throttle', min=-1.0, max=1.0, value=0.0, step=0.01, orientation='vertical')

steering_gain_link   = traitlets.link((steering_gain_slider, 'value'), (car, 'steering_gain'))
steering_offset_link = traitlets.link((steering_bias_slider, 'value'), (car, 'steering_offset'))
steering_value_link  = traitlets.link((steering_value_slider, 'value'), (car, 'steering'))
throttle_slider_link = traitlets.link((throttle_slider, 'value'), (car, 'throttle'))

display(ipywidgets.HBox([a,b]))
display(c,d,e,f)

display(
    widgets.VBox(
        [widgets.HBox([network_output_slider,
                       widgets.Label(value="X"),
                       steering_gain_slider,
                       widgets.Label(value="+"),
                       steering_bias_slider,
                       widgets.Label(value="||"), 
                       steering_value_slider,throttle_slider], layout=Layout(
                                                    align_items='center'
                                                        )
                     ), 
         live_execution_widget]
    )
)
display(ipywidgets.HBox([steer,error_steer]))


# In[6]:


fi_list = [e1.value,e2.value,e3.value,e4.value,e5.value,e6.value,e7.value,e8.value,e9.value,e10.value,e11.value,e12.value,e13.value,e14.value,e15.value,e16.value,e17.value]
slider_list = [slider1.value,slider2.value,slider3.value,slider4.value,slider5.value,slider6.value,slider7.value]

#print(fi_list)
#print(slider_list)


# In[7]:


def ai(img):
    image = preprocess(img).half()
    output = model_trt(image).detach().cpu().numpy().flatten()
    x = float(output[0])
    y = float(output[1])
    return x,y


# In[8]:


global counter
counter = 0
steerings_ab = []
fault_list = []
actual_steer = []


# In[9]:


from utils import preprocess,fault_injection

def update(change):
    global counter
    counter = counter +1
    new_image = change['new']
    new_image = Image.fromarray(new_image)
    edited_image = fault_injection(new_image,fi_list,slider_list)
    '''
    if number in num_range:
        edited_image = functions[number](new_image, contrast_value_slider.value)
    else:
        edited_image = weather(img_idx[number], new_image, size,contrast_value_slider.value)
    '''
    new_image = np.array(new_image)

    x,y = ai(new_image)
    e_x,e_y = ai(edited_image)
    
    network_output_slider.value = x * steering_gain_slider.value + steering_bias_slider.value
    steering_value_slider.value = e_x * steering_gain_slider.value + steering_bias_slider.value
    
    steering = x * steering_gain_slider.value + steering_bias_slider.value
    e_steering = e_x * steering_gain_slider.value + steering_bias_slider.value
    if(steering<-1.0):
        steering_value_slider.value = -1.0
    elif(steering>1.0):
        steering_value_slider.value = 1.0
    else:
        steering_value_slider.value = steering 
    car.steering = steering
    steer.value = steering
    error_steer.value = e_steering
    
    #while counter < 500:
    #    #actual_steer.append(steering)
    #    #fault_list.append(e_steering)
    

    #steerings_ab.append([steering,e_steering])
    
    if(state_widget.value == 'On'):
        x = int(camera.width * (x / 2.0 + 0.5))
        y = int(camera.height * (y / 2.0 + 0.5))  
        prediction = new_image.copy()
        prediction = cv2.circle(prediction, (x, y), 8, (255, 0, 0), 3)
        e_x = int(camera.width * (e_x / 2.0 + 0.5))
        e_y = int(camera.height * (e_y / 2.0 + 0.5))  
        e_prediction = edited_image.copy()
        e_prediction = cv2.circle(e_prediction, (e_x, e_y), 8, (255, 0, 0), 3)
                
        prediction_widget.value = bgr8_to_jpeg(prediction)
        i_widget.value = bgr8_to_jpeg(e_prediction)

            
update({'new': camera.value})  # we call the function once to initialize
camera.observe(update, names='value')
camera.running = True


# In[10]:


camera.observe(update, names='value') 


# In[11]:


camera.running = True


# In[ ]:





# In[ ]:





# In[ ]:





# In[15]:


len(steerings_ab)


# In[16]:


data = pd.DataFrame({"Actual Steering":actual_steer,"Faulty Steering":fault_list})
data.to_excel('sample_data.xlsx', sheet_name='sheet1', index=False)


# In[13]:


import json

json_string = json.dumps(steerings_ab)
print(json_string)


# In[7]:


import ipywidgets

e1 = ipywidgets.Checkbox(
    value=False,
    description='Gaussian Blur',
    disabled=False
    , layout={'width': '300px'})
e2 = ipywidgets.Checkbox(
    value=False,
    description='Contrast',
    disabled=False
    , layout={'width': '300px'})
e3 = ipywidgets.Checkbox(
    value=False,
    description='Brightness',
    disabled=False
    , layout={'width': '300px'})
e4 = ipywidgets.Checkbox(
    value=False,
    description='Sharpness',
    disabled=False
, layout={'width': '300px'})
e5 = ipywidgets.Checkbox(
    value=False,
    description='Colour',
    disabled=False
, layout={'width': '300px'})
e6 = ipywidgets.Checkbox(
    value=False,
    description='Salt Pepper Noise',
    disabled=False
, layout={'width': '300px'})
e7 = ipywidgets.Checkbox(
    value=False,
    description='Rain Drop Blur',
    disabled=False
, layout={'width': '300px'})
e8 = ipywidgets.Checkbox(
    value=False,
    description='Mud splash',
    disabled=False
, layout={'width': '300px'})
e9 = ipywidgets.Checkbox(
    value=False,
    description='Shatterd Glass',
    disabled=False
    , layout={'width': '300px'})
e10 = ipywidgets.Checkbox(
    value=False,
    description='Glass crack',
    disabled=False
    , layout={'width': '300px'})
e11 = ipywidgets.Checkbox(
    value=False,
    description='Dirt',
    disabled=False
    , layout={'width': '300px'})
e12 = ipywidgets.Checkbox(
    value=False,
    description='Dust',
    disabled=False
, layout={'width': '300px'})
e13 = ipywidgets.Checkbox(
    value=False,
    description='Smog',
    disabled=False
, layout={'width': '300px'})
e14 = ipywidgets.Checkbox(
    value=False,
    description='Snow',
    disabled=False
, layout={'width': '300px'})
e15 = ipywidgets.Checkbox(
    value=False,
    description='Rain',
    disabled=False
, layout={'width': '300px'})
e16 = ipywidgets.Checkbox(
    value=False,
    description='Dense Fog',
    disabled=False
, layout={'width': '300px'})
e17 = ipywidgets.Checkbox(
    value=False,
    description='Light Fog',
    disabled=False
, layout={'width': '300px'})


a = ipywidgets.HBox([e1,e2,e3])
c = ipywidgets.HBox([e5,e6,e7])
c = ipywidgets.HBox([e8,e9,e10])
d = ipywidgets.HBox([e11,e12,e13])
e = ipywidgets.HBox([e14,e15,e16])
f = ipywidgets.HBox([e17,e4])


display(a,c,d,e,f)


# In[ ]:




