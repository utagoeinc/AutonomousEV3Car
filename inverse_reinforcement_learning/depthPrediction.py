import argparse
import os
import numpy as np
import tensorflow as tf
from PIL import Image

import models

class DepthPredictor:
    def __init__(self, model_data_path='NYU_FCRN.ckpt'):
        # Default input size
        self.height = 176
        self.width = 176
        self.channels = 3
        self.batch_size = 1

        # Create a placeholder for the input image
        self.input_node = tf.placeholder(tf.float32, shape=(None, self.height, self.width, self.channels))

        # Construct the network
        self.net = models.ResNet50UpProj({'data': self.input_node}, self.batch_size, 1, False)

        # Use to load from ckpt file
        print('DepthPredictor: Loading the model')
        self.sess = tf.Session()
        saver = tf.train.Saver()
        saver.restore(self.sess, model_data_path)


    def predict(self, image_bin):
        # Read image
        img = Image.open(image_bin)
        img = img.resize([self.width,self.height], Image.ANTIALIAS)
        img = np.array(img).astype('float32')
        img = np.expand_dims(np.asarray(img), axis = 0)

        # Evalute the network for the given image
        pred = self.sess.run(self.net.get_output(), feed_dict={self.input_node: img})

        return pred[0,:,:,0]
