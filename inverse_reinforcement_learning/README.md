# Inverse Reinforcement Learning
Demo application of Inverse Reinforcement Learning (IRL) with a simple simulator.

All programs are written in the Python3.

## How to run
1. Install dependencies.  

      ```
      pip install -r requirements.txt
      ```

1. Download NYU Depth v2 model for [FCRN-DepthPrediction](https://github.com/iro-cp/FCRN-DepthPrediction) and place them on this directory.

1. Modify the bottom of train.py if you need.

1. Run the script.

      ```
      python train.py
      ```

## Methodology
Reinforcement Learning (RL) and Inverse Reinforcement Learning (IRL) are often applied to solve problems such as Go and Atari Games.
Well-trained model predicts the best actions for the states on an arbitrary environment.
Strategies of selecting such actions maximize the entire rewards.
