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

1. Modify the bottom of lane.py as you want.  

    For example, both simple_lane() and advanced_lane() have the argument of path to the input image.  

    You can also comment/uncomment calling these functions to change the approach.

1. Run the script.

      ```
      python lane.py
      ```

## Approaches
### simple_lane() function
1. Extract edges
    ![canny](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_detection/canny.png)

1. Detect Lines
    ![hough](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_detection/hough.png)

    ![lines](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_detection/averaged_line.png)

    ![result](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_detection/combo_image.jpg)

### advanced_lane() function
1. Perspective transform

    This step takes perspective transformation.
    We give our test images as inputs, and transform them to get birds-eye view images.

    There is a parameter in the transforming algorithm.
    They represent corresponding pixels in both input and output images.
    In our case, we used following values as this parameter.

    |Original Image |Transformed Image |
    |---|---|
    |(10, 176) |(35, 176) |
    |(140, 176) |(140, 176) |
    |(110, 140) |(140, 0) |
    |(48, 140) |(35, 0) |

    ![perspective transform](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_detection/transform.png)

    Function warp() gives us this transformation.

1. Convert into binary images

    After transforming, converting them into binary images using thresholds.

    Threshold is:

    |Lower Threshold |Higher Threshold |
    |---|---|
    |200 |255 |

    If a pixel has a value between lower and higher thresholds, it becomes white in the output image.
    Otherwise, it becomes black in the output.

    After thresholding the image, output is blurred by gaussian filter.

    ![binary conversion](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_detection/white_line_detection.png)

1. Find lines

    Using moving averages to find lines that represent us the lane.

    ![find lines](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_detection/masks.png)

1. Output the result

    ![result](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_detection/warp_inv.png)
