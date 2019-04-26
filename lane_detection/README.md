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

    You can also comment/uncomment callings of these functions to change the approach.

1. Run the script.

      ```
      python lane.py
      ```

## Approaches
### simple_lane() function
1. Extract edges
    ![canny](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_detection/canny.png)

    This step takes edge extraction using Canny algorithm.

    First, applying a gaussian filter to get blurred input image.
    By doing this, we can reduce the noises of input images.

    Then, extracting edges using Canny edge detector.
    In our case, applying the function called Canny() in the OpenCV to doing this.

    There are two thresholds: lower and higher.
    In the Canny algorithm, candidates of edges are detected using gradients of the pixels.
    If the gradient has the value larger than higher threshold, it might be a true edge.
    Otherwise, if it has the value smaller than lower threshold, it might be a false edge.
    We used the thresholds as below.

    |Lower Threshold |Higher Threshold |
    |---|---|
    |50 |100 |

    [![Canny thresholds](http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/_images/hysteresis.jpg)](http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_canny/py_canny.html)

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
    First we calculate the peaks of moving averages for width direction.
    Wavelet transformation method was used at this time so that it will be robust for noise.
    In the most cases two peaks were found, and we used them as a initial value of candidates of peaks in the next step.

    After initializing, we divided an image into 11 pieces along to height direction then applied the moving average and wavelet transformation method again for each ones from a piece with larger height to that with smaller height.
    If we could find appropriate peaks, then we regarded them as lines.
    Otherwise, we used the previous values of peaks.

    As a result, we could get both left and right line predictions like below.

    ![find lines](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_detection/masks.png)

1. Output the result

    With the result of previous step, we can draw a polygon which represents the area of predicted lane.
    Final step takes perspective transformation which is opposite with the first step and combine the output polygon and the original input.

    ![result](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_detection/warp_inv.png)
