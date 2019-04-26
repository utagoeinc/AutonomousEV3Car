# AutonomousEV3Car
Demo applications of autonomous, or self-driving, car by LEGO Mindstorms EV3.

If you wanted to see our car running, please watch the video on the [YouTube](https://www.youtube.com/watch?v=nMtCHrGf0yg&feature=youtu.be).

We also have [our website](http://www.utagoe.com/jp/legoev3.html).

[![YouTube Link](https://img.youtube.com/vi/nMtCHrGf0yg/0.jpg)](https://www.youtube.com/watch?v=nMtCHrGf0yg&feature=youtu.be)

As you can see on the video, we have implemented the autonomous car as a internal research project.

Our car only uses an image (176*176, grayscale jpeg format) which is sent from iPhone set in front of the car.

![EV3 car](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/EV3car_image.jpg)

This repo includes following demo applications.
- [EV3Control](https://github.com/utagoeinc/AutonomousEV3Car/tree/master/EV3Control): iOS App of remote controller of EV3 car
- [ev3rt-utagoe](https://github.com/utagoeinc/AutonomousEV3Car/tree/master/ev3rt-utagoe): C++ program which controls EV3 directly
- [inverse_reinforcement_learning](https://github.com/utagoeinc/AutonomousEV3Car/tree/master/inverse_reinforcement_learning): Demo application of Inverse Reinforcement Learning (IRL) with simple simulator using OpenGL
- [lane_detection](https://github.com/utagoeinc/AutonomousEV3Car/tree/master/lane_detection): Detecting lane using OpenCV
- [lane_tracking](https://github.com/utagoeinc/AutonomousEV3Car/tree/master/lane_tracking): Tracking lane using Convolutional Neural Network (CNN)

For more informations, please check the README.md on each directory.


## Getting Started
1. Building EV3 car  
  We used the [RAC3 Truck](https://www.lego.com/en-us/mindstorms/build-a-robot/rac3-truck) and remodeled a bit as follows.
    1. Put away the steering wheel.
    1. Add a vertical bar in the front of the truck to keep the iPhone in the right place.
    ![Parts added](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/added_parts.jpg)
    ![customized EV3](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/customized_EV3_image.jpg)

1. Prepare SD card for inserting into the EV3  
  There are two ways for preparing the SD card. The easiest way is to copy ev3rt-utagoe/sdcard/* on the SD card.

1. Run any application you like!


## References
1. [OpenCV Python Tutorial - Find Lanes for Self-Driving Cars (Computer Vision Basics Tutorial)](https://www.youtube.com/watch?v=eLTLtUVuuy4)
1. [RyosukeHonda/Advanced_Lane_Lines](https://github.com/RyosukeHonda/Advanced_Lane_Lines)
1. [Canny法によるエッジ検出](http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_canny/py_canny.html)
