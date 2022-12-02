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

# Fault Injection Module (FIM)

Now faults are injected into camera image frames to simulate real-time errors in autonomous cars. As an input to the AI model of the autonomous car, the camera on the autonomous car provides image frames at a rate of 30 frames per second. We therefore need a Fault Injection Module (FIM) in order to inject the camera-based faults into the image frames. The Fault Injection Module (FIM) is a Python interface that allows selecting single or multiple faults to be injected, as well as selecting the intensity of the fault to be injected.

![FIM](https://user-images.githubusercontent.com/117833435/205360071-800a1b06-1a23-4ed7-b978-d95d9474409b.jpg)


