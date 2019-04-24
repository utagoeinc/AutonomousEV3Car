# AutonomousEV3Car
Demo applications of autonomous, or self-driving, car by LEGO Mindstorms EV3.
First of all, please watch the video on the YouTube.

[![YouTube Link](https://img.youtube.com/vi/nMtCHrGf0yg/0.jpg)](https://www.youtube.com/watch?v=nMtCHrGf0yg&feature=youtu.be)

As you can see on the video, we have implemented the autonomous car as a internal research project.
<!-- EV3の全体画像 -->

This repo includes following demo applications.
- EV3Control: iOS App of remote controller of EV3 car
- ev3rt-utagoe: C++ program which controls EV3 directly
- inverse_reinforcement_learning: Demo application of Inverse Reinforcement Learning (IRL) with simple simulator using OpenGL
- lane_detection: Detecting lane using OpenCV
- lane_tracking: Tracking lane using Convolutional Neural Network (CNN)

For more informations, please check the README.md on each directory.


## Getting Started
1. Building EV3 car  
We used the [RAC3 Truck](https://www.lego.com/en-us/mindstorms/build-a-robot/rac3-truck) and remodeled a bit as follows.
    1. Put away the steering wheel.
    1. Add a vertical bar in the front of the truck to keep the iPhone in the right place.
    <!-- 追加パーツの写真 -->

1. Prepare SD card for inserting into the EV3  
There are two ways for preparing the SD card. The easiest way is to copy ev3rt-utagoe/sdcard/* on the SD card.

1. Run any application you like!


## References
1. References will come here
