# coding:utf-8
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
import cv2
import os

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    'mode',
    help='train or test')
parser.add_argument(
    '-s',
    '--step',
    help='The number of step which the model you want to load.',
    default=0)
parser.add_argument(
    '-t',
    '--test_image',
    help='Path to the image for test.',
    default=None)
parser.add_argument(
    '-a',
    '--expected_action',
    help='Expected action for test_image',
    default=0)

class Model:
    def __init__(self, learning_rate=0.001, step=0):
        os.makedirs('./backup', exist_ok=True)
        self.step = step

        self.model = Sequential()
        self.model.add(Conv2D(8, (5,5), strides=(1,1), padding='same', activation='relu', input_shape=(176,176,3)))
        self.model.add(BatchNormalization(axis=-1))
        self.model.add(Conv2D(8, (5,5), strides=(1,1), padding='same', activation='relu'))
        self.model.add(BatchNormalization(axis=-1))
        self.model.add(Conv2D(8, (5,5), strides=(1,1), padding='same', activation='relu'))
        self.model.add(BatchNormalization(axis=-1))
        self.model.add(Conv2D(8, (5,5), strides=(1,1), padding='same', activation='relu'))
        self.model.add(BatchNormalization(axis=-1))
        self.model.add(MaxPooling2D(pool_size=(2,2), strides=None, padding='valid'))
        self.model.add(Conv2D(4, (5,5), strides=(1,1), padding='same', activation='relu'))
        self.model.add(BatchNormalization(axis=-1))
        self.model.add(MaxPooling2D(pool_size=(2,2), strides=None, padding='valid'))
        self.model.add(Conv2D(1, (5,5), strides=(1,1), padding='same', activation='relu'))
        self.model.add(BatchNormalization(axis=-1))
        self.model.add(MaxPooling2D(pool_size=(2,2), strides=None, padding='valid'))
        self.model.add(Flatten())
        self.model.add(Dense(256, activation='relu'))
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(5, activation='softmax'))

        self.optimizer = Adam(lr=learning_rate)
        self.model.compile(loss='sparse_categorical_crossentropy', optimizer=self.optimizer)

        self.weights_file = './backup/lane_tracking_{}.h5'

        # Load existing model
        if os.path.exists(self.weights_file.format(step)):
            print('Loading the model "{}"'.format(self.weights_file.format(step)))
            self.model.load_weights(self.weights_file.format(step), by_name=True)

    def train(self, inputs, targets):
        assert len(inputs) == len(targets)

        for step in range(self.step + 1, 100000 + 1):
            indices = np.random.choice(np.arange(len(inputs)), size=32, replace=False)
            inputs_batch = np.array([cv2.imread(inputs[index]) for index in indices])
            targets_batch = np.array([targets[index] for index in indices])

            print('step:', step)
            self.model.fit(inputs_batch, targets_batch, batch_size=8, epochs=4, verbose=1, validation_split=0.2)
            if (step < 1000 and step%100 == 0) or (step < 10000 and step%1000 == 0) or step%5000 == 0:
                self.model.save_weights(self.weights_file.format(step))

    def predict(self, input):
        return self.model.predict_classes(input)[0]


def main(step=0):
    model = Model(step=step)

    inputs = []
    targets = []

    data_dir = os.path.join(os.getcwd(), 'data')
    with open(os.path.join(data_dir, 'train.txt'), 'r') as train_txt:
        for line in train_txt:
            image, action = line.replace('\n', '').split(',')
            inputs.append(os.path.join(data_dir, image))
            targets.append(int(action))

    targets_np = np.array(targets)

    model.train(inputs, targets_np)


def test(image_path, expected_action, step=0):
    model = Model(step=step)

    input = np.array([cv2.imread(image_path)])

    predicted_action = model.predict(input)
    print('predicted_action {}, expected_action {}'.format(predicted_action, expected_action))


if __name__ == '__main__':
    args = parser.parse_args()

    if args.mode == 'train':
        main(step=args.step)
    elif args.mode == 'test':
        test(args.test_image, args.expected_action, step=args.step)
