# lane_tracking
This application realizes the autonomous car using Convolutional Neural Network (CNN).

All programs are written in the Python3.

## Abstract
This application receives 176*176 grayscale lane image which is taken by iPhone in front of EV3 car and predicts appropriate steering angle to track lane.

Steering angles are classified into 5 classes: large left (LEFT), small left (left), center, small right (right), and large right(RIGHT).

When running EV3 car after training our CNN, it predicts classes for unknown images.

![Abstract_running](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_tracking/tracking_abstract.png)

## Getting Started
1. Install dependencies.  
    ```
    pip install -r requirements.txt
    ```  
1. Prepare EV3 car and EV3Control App.  
  See an appropriate directory and its README.

1. Collect data for training.
  In this step, python script receives both an image from EV3 car and expected action from EV3Control app.
  Run the following command to start getting your training dataset.
    ```  
    python getting_data.py
    ```  
  While you getting your dataset, "Image Saving Flag", which appears on the following figure, will send when you tapped any buttons except direction buttons on the EV3Control app.  
  In other words, set expected actions by tapping direction buttons and save it with an image by tapping any other buttons.  
  ![Abstract_getting_data](https://raw.githubusercontent.com/utagoeinc/AutonomousEV3Car/images/lane_tracking/data_collecting_abstract.png)  

  Dataset will be saved in the (YOUR_PROJECT_ROOT)/lane_tracking/data directory.  

  After saving the images and their expected actions, run the following command to reshape them.  
    ```
    python preprocess.py
    ```  
1. Training CNN.
    ```
    python train.py train -s STEP
    ```  
  Training CNN with the dataset you got in the previous step.  
  STEP means the number of step you want to start training from.  
  Trained weights will be saved in the (YOUR_PROJECT_ROOT)/lane_tracking/backup directory.  

  For more information, run the script with -h option.  

1. Run EV3 car with trained model.
  Finally, you can run your EV3 car with trained model by run.py.  
    ```
    python run.py -s STEP
    ```  
