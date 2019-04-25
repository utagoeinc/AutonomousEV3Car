# Lane Detection
This application detects the lines on the lane using OpenCV.

We have two approaches.
1. Detecting two straight lines using Canny Edge Detection.
1. Using moving average of binary image and find peaks to detect lines.

All programs are written in the Python3.

## How to run
1. Install dependencies.  

      ```
      pip install -r requirements.txt
      ```  

1. Modify the bottom of advanced_lane.py as you want.  

    For example, both simple_lane() and advanced_lane() have the argument of path to the input image.  

    You can also comment/uncomment calling these functions to change the approach.

1. Run the script.

      ```
      python lane.py
      ```

## Approaches
### simple_lane() function
1.

### advanced_lane() function
1. Perspective transform
    This step takes perspective transformation.
    We give our test images as inputs, and transform them to get birds-eye view images.
    ![perspective transform](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_detection/transform.png)
