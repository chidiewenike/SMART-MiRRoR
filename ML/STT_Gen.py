from __future__ import division, print_function, absolute_import
import tflearn
import tensorflow as tf
import speech_data
import tensorflow as tf
import os
import librosa
import numpy as np
import wave
from random import shuffle
from enum import Enum

path = os.getcwd() + "\\data"
CHUNK = 4096

"""
ww_label = [wake_word , not_wake_word]
"""

wake_word     = [1,0]
not_wake_word = [0,1]

"""
functions = [weather, schedule, quote, music, rap, r_and_b, other, news, end, unknown]
"""
weather   =     [1,0,0,0,0,0,0,0,0,0]
schedule  =     [0,1,0,0,0,0,0,0,0,0]
quote     =     [0,0,1,0,0,0,0,0,0,0]
music     =     [0,0,0,1,0,0,0,0,0,0]
rap       =     [0,0,0,0,1,0,0,0,0,0]
r_and_b   =     [0,0,0,0,0,1,0,0,0,0]
other     =     [0,0,0,0,0,0,1,0,0,0]
news      =     [0,0,0,0,0,0,0,1,0,0]
end       =     [0,0,0,0,0,0,0,0,1,0]
unknown   =     [0,0,0,0,0,0,0,0,0,1]


def one_hot_from_item(item, items):
  # items=set(items) # assure uniqueness
  x=[0]*len(items)# numpy.zeros(len(items))
  i=items.index(item)
  x[i]=1
  return x

def mfcc_batch_generator(batch_size=10, target=Target.digits):
  batch_features = []
  labels = []
  files = os.listdir(path)
  while True:
    print("loaded batch of %d files" % len(files))
    shuffle(files)
    for wav in files:
      if not wav.endswith(".wav"): continue
      wave, sr = librosa.load(path+wav, mono=True)   
      label = label_gen(wav)  
      labels.append(label)
      mfcc = librosa.feature.mfcc(wave, sr)
      # print(np.array(mfcc).shape)
      mfcc=np.pad(mfcc,((0,0),(0,80-len(mfcc[0]))), mode='constant', constant_values=0)
      batch_features.append(np.array(mfcc))
      if len(batch_features) >= batch_size:
        # print(np.array(batch_features).shape)
        # yield np.array(batch_features), labels
        yield batch_features, labels  # basic_rnn_seq2seq inputs must be a sequence
        batch_features = []  # Reset for next batch
        labels = []

def load_wav_file(name):
  f = wave.open(name, "rb")
  # print("loading %s"%name)
  chunk = []
  data0 = f.readframes(CHUNK)
  while data0:  # f.getnframes()
    # data=numpy.fromstring(data0, dtype='float32')
    # data = numpy.fromstring(data0, dtype='uint16')
    data = np.fromstring(data0, dtype='uint8')
    data = (data + 128) / 255.  # 0-1 for Better convergence
    # chunks.append(data)
    chunk.extend(data)
    data0 = f.readframes(CHUNK)
  # finally trim:
  chunk = chunk[0:CHUNK * 2]  # should be enough for now -> cut
  chunk.extend(np.zeros(CHUNK * 2 - len(chunk)))  # fill with padding 0's
  # print("%s loaded"%name)
  return chunk

def label_gen(file):
  return 

learning_rate = 0.0001
training_iters = 300000  # steps
batch_size = 64

width = 20  # mfcc features
height = 80  # (max) length of utterance
classes = 10  # digits

batch = word_batch = mfcc_batch_generator(batch_size)
X, Y = next(batch)
trainX, trainY = X, Y
testX, testY = X, Y #overfit for now

# Network building
net = tflearn.input_data([None, width, height])
net = tflearn.lstm(net, 128, dropout=0.8)
net = tflearn.fully_connected(net, classes, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=learning_rate, loss='categorical_crossentropy')
# Training

### add this "fix" for tensorflow version errors
col = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
for x in col:
    tf.add_to_collection(tf.GraphKeys.VARIABLES, x ) 


model = tflearn.DNN(net, tensorboard_verbose=0)
while 1: #training_iters
  model.fit(trainX, trainY, n_epoch=10, validation_set=(testX, testY), show_metric=True,
          batch_size=batch_size)
  _y=model.predict(X)
model.save("tflearn.lstm.model")
print (_y)
print (Y)

