# coding:utf-8
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from collections import deque
from keras import backend as K
import tensorflow as tf

import os

# [1]損失関数の定義
# 損失関数にhuber関数を使用します 参考https://github.com/jaara/AI-blog/blob/master/CartPole-DQN.py
def huberloss(y_true, y_pred):
    err = y_true - y_pred
    cond = K.abs(err) < 1.0
    L2 = 0.5 * K.square(err)
    L1 = (K.abs(err) - 0.5)
    loss = tf.where(cond, L2, L1)  # Keras does not cover where function in tensorflow :-(
    return K.mean(loss)


# [2]Q関数をディープラーニングのネットワークをクラスとして定義
class QNetwork:
    def __init__(self, learning_rate=0.01, action_size=5, episode=0):
        self.action_size = action_size
        dense_units = action_size ** 4

        self.model = Sequential()
        self.model.add(Conv2D(8, (5,5), strides=(1,1), padding='same', activation='relu', input_shape=(96,96,3)))
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
        self.model.add(Dense(dense_units, activation='relu'))
        self.model.add(Dense(dense_units, activation='relu'))
        self.model.add(Dense(dense_units, activation='relu'))
        self.model.add(Dense(dense_units, activation='relu'))
        self.model.add(Dense(action_size, activation='linear'))

        self.optimizer = Adam(lr=learning_rate)
        self.model.compile(loss=huberloss, optimizer=self.optimizer)

        self.weights_file = './qnet_{}.h5'

        # 既に学習済みの重みデータがある場合はロードする
        if os.path.exists(self.weights_file.format(episode-1)):
            print('QNetwork: Loading the model')
            self.model.load_weights(self.weights_file.format(episode-1), by_name=True)

    # 重みの学習
    def replay(self, memory, batch_size, gamma, targetQN):
        inputs = np.zeros((batch_size, 96, 96, 3))
        targets = np.zeros((batch_size, self.action_size))
        mini_batch = memory.sample(batch_size)

        for i, (state_b, expertQs_b) in enumerate(mini_batch):
            inputs[i:i + 1] = state_b

            # 勾配を計算してtargetsを計算
            retmainQs_b = targetQN.model.predict(state_b)[0] # Qネットワークの出力
            gradient_b = expertQs_b - retmainQs_b
            targets[i:i + 1] = retmainQs_b + gamma * gradient_b # もとのモデル出力をエキスパートの報酬方向へgamma分だけ近づける

        self.model.fit(inputs, targets, epochs=1, verbose=1)  # epochsは訓練データの反復回数、verbose=1はプログレスバー表示設定

    # 重みの保存
    def save(self, episode):
        self.model.save_weights(self.weights_file.format(episode))


# [3]Experience ReplayとFixed Target Q-Networkを実現するメモリクラス
# 一旦行動と報酬のペアを保存しておき、モデル学習時にそこからランダムサンプリングして時系列の相関を消すのが目的
class Memory:
    def __init__(self, max_size=1000):
        self.buffer = deque(maxlen=max_size)

    def add(self, experience): #experience = (state, expertQs)
        self.buffer.append(experience)

    def sample(self, batch_size):
        idx = np.random.choice(np.arange(len(self.buffer)), size=batch_size, replace=False)
        return [self.buffer[ii] for ii in idx]

    def len(self):
        return len(self.buffer)


# 入力画像に応じて、行動を決定するクラス
class Actor:
    def __init__(self, action_size=5):
        pass

    def get_action(self, state, mainQN):   # [C]ｔ＋１での行動を返す
        retTargetQs = mainQN.model.predict(state)[0]
        action = np.argmax(retTargetQs)  # 最大の報酬を返す行動を選択する

        return action


# 学習の主体クラス
class Train:
    def __init__(self, episode=0):
        self.DQN_MODE = 1    # 1がDQN、0がDDQNです

        self.current_episode = episode # 現在の試行回数
        self.current_step = 0    # 現在のstep数
        self.num_episodes = 100  # 総試行回数
        self.max_number_of_steps = 100  # 1試行のstep数
        self.goal_average_reward = 195  # この報酬を超えると学習終了
        self.num_consecutive_iterations = 10  # 学習完了評価の平均計算を行う試行回数
        self.total_reward_vec = np.zeros(self.num_consecutive_iterations)  # 各試行の報酬を格納
        self.gamma = 0.1    # 勾配の反映係数
        self.islearned = 0  # 学習が終わったフラグ
        self.done = 0  # 試行終了フラグ
        self.updating = 0 # モデル更新中フラグ
        # ---
        self.action_size = 5
        self.learning_rate = 0.00001         # Q-networkの学習係数
        self.memory_size = 10000            # バッファーメモリの大きさ
        self.batch_size = 32                # Q-networkを更新するバッチの大記載
        # ---
        self.current_state = None
        self.prev_state = None
        self.prev_prev_state = None

        # [5.2]Qネットワークとメモリ、Actorの生成--------------------------------------------------------
        self.mainQN = QNetwork(learning_rate=self.learning_rate, action_size=self.action_size, episode=episode)     # メインのQネットワーク
        self.targetQN = QNetwork(learning_rate=self.learning_rate, action_size=self.action_size, episode=episode)   # 価値を計算するQネットワーク
        self.memory = Memory(max_size=self.memory_size)
        self.actor = Actor(self.action_size)

        self.targetQN.model.set_weights(self.mainQN.model.get_weights())

    def train(self, state, action):
        # Stateの記憶更新
        self.prev_prev_state = self.prev_state
        self.prev_state = self.current_state
        self.current_state = state

        if self.prev_state is None:
            self.prev_state = state
        if self.prev_prev_state is None:
            self.prev_prev_state = state

        integrated_states = np.concatenate([self.current_state, self.prev_state, self.prev_prev_state], 3)
        assert integrated_states.shape is not (1, 96, 96, 3)

        # 前エピソード終了後、次エピソード開始まで
        if self.islearned == 1:
            self.prev_prev_state = None
            self.prev_state = None
            self.current_state = None
            return True

        # エピソード中
        elif self.current_step < self.max_number_of_steps and self.done == 0:
            # アクション推定
            predicted_action = self.actor.get_action(integrated_states, self.mainQN)
            print('Step {}: DQN predicted "{}"'.format(self.current_step, predicted_action+1))

            # 引数で与えられたエキスパートの選択アクションによる報酬計算
            expertQs = np.zeros(self.action_size)
            expertQs[action] = 0.1

            # モデルの更新
            self.memory.add((integrated_states, expertQs))

            # Qネットワークの重みを学習・更新する replay
            if (self.memory.len() > self.batch_size):
                self.mainQN.replay(self.memory, self.batch_size, self.gamma, self.targetQN)

            if self.DQN_MODE:
                self.targetQN.model.set_weights(self.mainQN.model.get_weights())

            self.current_step += 1
            return False

        # エビソード終了時
        else:
            if self.current_step >= self.max_number_of_steps or self.done == 1:
                self.updating = 1

                # 引数で与えられたエキスパートの選択アクションによる報酬計算
                expertQs = np.zeros(self.action_size)

                #報酬確定
                if self.current_step < self.goal_average_reward:
                    #衝突して試行を中断した場合
                    expertQs[action] = -1.0
                else:
                    #衝突せずに規定のstepを完走した場合
                    expertQs[action] = 0.1

                self.memory.add((integrated_states, expertQs))

                # Qネットワークの重みを学習・更新する replay
                if (self.memory.len() > self.batch_size):
                    self.mainQN.replay(self.memory, self.batch_size, self.gamma, self.targetQN)

                self.targetQN.model.set_weights(self.mainQN.model.get_weights())

                print('%d Episode finished after %f time steps' % (self.current_episode, self.current_step))
                self.mainQN.save(self.current_episode)

                self.prev_prev_state = None
                self.prev_state = None
                self.current_state = None

                self.current_step = 0
                self.current_episode += 1
                self.done = 0
                self.updating = 0
            else:
                #上限回数到達により学習中断
                pass

            if self.current_episode >= self.num_episodes:
                print('Train agent done!')
                self.mainQN.save()
                self.islearned = 1

            return True # 終了

class Test:
    def __init__(self, episode=0):
        self.current_state = None
        self.prev_state = None
        self.prev_prev_state = None

        self.action_size = 5
        self.learning_rate = 0.00001         # Q-networkの学習係数

        self.stop = False

        self.mainQN = QNetwork(learning_rate=self.learning_rate, action_size=self.action_size, episode=episode+1)     # メインのQネットワーク
        self.actor = Actor(self.action_size)

    def run(self, state):
        # Stateの記憶更新
        self.prev_prev_state = self.prev_state
        self.prev_state = self.current_state
        self.current_state = state

        if self.prev_state is None:
            self.prev_state = state
        if self.prev_prev_state is None:
            self.prev_prev_state = state

        integrated_states = np.concatenate([self.current_state, self.prev_state, self.prev_prev_state], 3)
        assert integrated_states.shape is not (1, 96, 96, 3)

        if self.stop:
            return -1

        action = self.actor.get_action(integrated_states, self.mainQN)
        return action
