The emergence of autonomous vehicles and smart mobility is transforming transportation and road travel. The advent of new technologies is paving the way for easier, more efficient journeys and the goal of zero traffic fatalities. With the increasing reliance on machines and vehicles for critical tasks, it is vital to have confidence that they will operate safely and reliably at all times. To be truly 'trustworthy', the electronic components and systems in these vehicles and machines need to be totally reliable. Safety and reliability are non-negotiable requirements. Through the TRUST-E project, methodologies and processes are being developed for the development of trustworthy electronic components, modules, and systems in automotive and aviation applications and in industrial settings. The University of Siegen is a partner university for this project, which falls under the [TRUST-E](https://penta-eureka.eu/project-overview/penta-call-5/trust-e/) program.  

# Fault-Injection-In-Autonomous-Vehicle.
Identifying failure modes of vehicle cameras in the domain of autonomous driving (ADAS) and, designing a Fault Injection Module (FIM) to inject these faults through image processing into the autonomous vehicle system.  

This task consists of identifying various failure modes associated with vehicle cameras. The following faults were selected for further study based on literature review and research: Pixel manipulation faults, image superimposition faults, and new filters to simulate rainy weather. As a result, the following faults have been implemented:

1. Contrast  
2. Brightness  
3. Blur Colour  
4. Sharpness  
5. Raindrop  
6. Blur  
7. Salt and Pepper noise  
8. Snow  
9. Dust  
10. Rain  
11. Dense fog  
12. Light fog  
13. Mud splash  
14. Glass crack  
15. Shattered glass  
16. Smog  
17. Dust  


# Fault Implementation

1. Pixel manipulation Filters  
Digitally, images are saved as a matrix of pixels. The pixel is the fundamental element of
an image. The way colours are specified is known as the colour space, and each pixel has a
distinct colour.
The RGB colour space is the most used. Three values, one each for red, green, and blue,
are used in this paradigm to define each colour. The term "colour depth" refers to the fact
that these values are typically 8-bit unsigned integers with a range of 0 to 255. Black and
white are the colours (255, 255, 255) and (0, 0, 0) respectively.
Filters are mathematical functions which perform mathematical computations of the pixel
values of the input image to produce a new image.The filters to manipulate the Brightness,
Sharpness, Colour and Contrast were created using the PIL module ImageEnhance using
separate functions.  

![blur](https://user-images.githubusercontent.com/117833435/205460743-80f1fc80-e115-4ebb-9201-1b26f4797760.png)


2. Image superimposition filters  
Image superimposition is a image processing technique for coping the image data from
one image over the other. This technique is used to implement faults related to changes
in weather and damage to the camera glass protecting the lens. The image frames from
the camera are superimposed with a mask of the fault to be injected. These masks are
transparent images collected from public domain images on Google. Transparent images
of dirt, snow, fog, glass crack, rain are used as masking images. These transparent images
contain opaque regions representing the faults. Only the opaque regions of the transparent
images are overlayed on the camera image frames.
Python Imaging Library (PIL) is a python package used for implementing these faults.  

![dirt](https://user-images.githubusercontent.com/117833435/205362210-a3b7a0fe-86b0-4727-8b7b-8a259282cfc9.png)  

3. Rain Drop Blur  
Drops of water during the rainy season create a blurring effect on the surface of the glass.
This blurring effect is caused only on the portion where the drop lies on the glass surface.
Such an effect is created using the pillow library in python.  


■ An image is created in the ’L’ (luminous) mode with the same size as that of the
camera frame image.  
■ Small white circles are drawn on the luminous image at random using the draw.ellipse
method.  
■ This luminous image is converted into an array.  
■ The image frame from the camera is blurred and then converted into an array.  
■ The blurred camera image is stacked on the luminous image to get the blurred effect
at random locations.  
■ The function is created which allows the user to set the number of blurred circles
depending on the desired effect to be generated. If the desired effect is slight rainfall,
the number of blurred circles to be drawn is small and for heavy rainfall the number
is large.  


![rain](https://user-images.githubusercontent.com/117833435/205361754-0d0af39f-102c-446a-8532-f08a65a03850.png)  


# Fault Injection Module (FIM)

Now faults are injected into camera image frames to simulate real-time errors in autonomous cars. As an input to the AI model of the autonomous car, the camera on the autonomous car provides image frames at a rate of 30 frames per second. We therefore need a Fault Injection Module (FIM) in order to inject the camera-based faults into the image frames. The Fault Injection Module (FIM) is a Python interface that allows selecting single or multiple faults to be injected, as well as selecting the intensity of the fault to be injected.  

![FIM](https://user-images.githubusercontent.com/117833435/205360071-800a1b06-1a23-4ed7-b978-d95d9474409b.jpg)  


# Plotting the deviations

We have 17 faults in total in the Fault Injection Module (FIM). These faults are further
divided into Pixel manipulation faults, Image superimposing faults, rain drop blur, Salt
and Pepper etc. Each of these faults have different levels of intensity variations possible.
In case of pixel manipulation faults, the intensity can be varied in a range from 1 to 10
with an increment of 1. For Rain drop blur, the intensity here refers to how heavy the
rainfall is, which in turn reflects upon the number of raindrops on the surface of the camera.
The range in this case ranges from 1 to 500.In case of Salt and Pepper, the intensity is a
probability and hence it ranges between 0 and 1. Likewise, we have carried out the testing
for 5 levels of intensity variations ranging from the lowest to the highest level for all the
faults.
In the figures below, we observe two graphs. The graph to the left is a plot of steering
values with and without fault injection. The green curve represents the steering values
without faults, and the red curve represents the steering values with fault injection.
The graph to the right represents the curve for the deviation of true steering value with
respect to the steering value with fault injection. The orange curve indicates the mean
deviation of the 200 observations.

The figures below show the plots for the fault Blur when injected into the AI system.  

![r1](https://user-images.githubusercontent.com/117833435/205456857-0af8faaf-ed9d-44d5-af41-bfd6bf755965.png)

![r2](https://user-images.githubusercontent.com/117833435/205456873-3196b307-efed-4eb3-a72d-75ce4fda5a03.png)

![r3](https://user-images.githubusercontent.com/117833435/205456905-9271ab44-3dc2-4fea-8ac1-a174ad8785bb.png)

![r4](https://user-images.githubusercontent.com/117833435/205456939-1ebe1a4e-9a51-4518-969d-5f1850e8ae7a.png)

![r5](https://user-images.githubusercontent.com/117833435/205456955-972c6d4c-ce13-4e47-bba7-7bc805f2990b.png)

# Conclusion

Autonomous Cars are attracting a growing attention in recent years, with new cutting edge
technologies implemented in the vehicles. The desire and need for autonomous capabilities will keep increasing in the near future. Sensor technology, data-fusion, Artificial Intelligence and Machine Learning applications are t play a huge role in autonomous
driving systems. Amongst sensors, the RGB (red, green, and blue) camera is acknowledged to be most commonly used. Degraded images from the camera may lead to wrong
decision-making by the AI system, which may lead to fatal accidents.    
Likewise, In our Studienarbeit we have worked on the following. First, we identified
faults of vehicle cameras in the domain of autonomous driving, by analysing the different
faults and their causes. Secondly, we injected these faults into our AI system using python
libraries that allowed simulating these camera failures. Thirdly, we integrated all these
faults into a user-friendly interface called Fault Injection Module.Each of the faults was
implemented by varying the intensity and using different filters. The respective deviation
in the steering value with respect to the true steering value was recorded. These deviations
were plotted, and the mean deviation was used for comparison between different faults.  After comparison of the results obtained, the faults with higher intensities namely Blur,
Brightness, Salt and Pepper, Rain Drop Blur and specific filters of Image superposition
faults cause a significant deviation greater than 60 percent. Such a high percentage
deviation is very dangerous and the abnormal behaviour of the vehicle can be easily
noticed. On the other hand, the faults at lower intensities can still cause a disruption in
the normal functioning of the AI system can still behave similarly to the normal operation
mode.
