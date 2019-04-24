# coding:utf-8
from threading import Thread

import numpy as np
from PIL import Image

import json
import io
import math
import sys

from irl import Train, Test
from depthPrediction import DepthPredictor
from simulator import Simulator

class EV3Trainer:
    def __init__(self, episode=0):
        self.depth_predictor = DepthPredictor(model_data_path='NYU_FCRN.ckpt')
        self.reinforcement_trainer = Train(episode=episode)
        self.reinforcement_tester = Test()
        self.reinforcement_tester.mainQN.model.set_weights(self.reinforcement_trainer.mainQN.model.get_weights())

    def train(self):
        img_bin = Simulator.simulator.getState() # 176*176
        depth_map = self.depth_predictor.predict(image_bin=img_bin)

        ## Uncomment if save img_bin.
        # raw_image = Image.open(img_bin)
        # raw_image.save('images/raw_image.jpg')

        ## Uncomment if save depth_map.
        # max = depth_map.max()
        # depth_for_save = depth_map*255/max
        # depth_for_save = np.array(depth_for_save, dtype=np.int32)
        # Image.fromarray(depth_for_save.astype(np.uint8)).save('images/depth.jpg')

        # Steering by hand
        while True:
            action = input('L ... R\n1 ... 5 >> ')
            if action.isdigit() and int(action) in range(1,6,1):
                action = int(action) - 1
                break
            else:
                print('action must be in the range between 1 to 5.')

        # Training
        state = depth_map.reshape((1,96,96,1))
        done = self.reinforcement_trainer.train(state, action)

        # Update state
        if Simulator.simulator.simulate(action = action) or done:
            Simulator.simulator.resetEnv()
            if not done:
                self.reinforcement_trainer.done = 1
                print('collsion!!!!!')
                self.reinforcement_trainer.train(state, action)

    def test(self):
        img_bin = Simulator.simulator.getState()
        depth_map = self.depth_predictor.predict(image_bin=img_bin)

        ## Uncomment if save img_bin.
        # raw_image = Image.open(img_bin)
        # raw_image.save('images/raw_image.jpg')

        ## Uncomment if save depth_map.
        # max = depth_map.max()
        # depth_for_save = depth_map*255/max
        # depth_for_save = np.array(depth_for_save, dtype=np.int32)
        # Image.fromarray(depth_for_save.astype(np.uint8)).save('images/depth.jpg')

        # Select action
        state = depth_map.reshape((1,96,96,1))
        action = self.reinforcement_tester.run(state)

        if Simulator.simulator.simulate(action = action):
            Simulator.simulator.resetEnv()
            print('collsion!!!!!')


class main:
    def __init__(self):
        trainer = EV3Trainer(episode=0) # start training from episode / testing model of (episode-1)
        Simulator(trainer.train) # Training
        Simulator(trainer.test) # Testing

if __name__ == '__main__':
    m = main()
