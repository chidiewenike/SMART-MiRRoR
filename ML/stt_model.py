import tensorflow as tf
from tensorflow.keras import layers, models
import os
import json
import numpy as np
import random
from datetime import datetime

class Model:

    def __init__(self, EPOCHS=20):

        self.words = {'background_noise':0, 'rap':1, 'rnb':2, 'other':3, 'weather':4, 'home':5, 'work':6, 'school':7, 'sleep':8, 'news':9, 'main':10}
        self.words_to_label()
        
        self.NUM_CLASSES = 11

        self.BCKRD_PATH = os.getcwd() + "\\Data\\STT_Data\\Audio\\background_noise\\"
        self.MFCC_PATH = os.getcwd() + "\\Data\\STT_Data\\STT_MFCC\\"

        self.GRU_UNITS = 64 # GRU unit size
        self.DROPOUT = 0.3 # dropout size
        self.EPOCHS = EPOCHS # number of fwd and bckwd props
        self.BATCH_SIZE = 8 # batch size

        self.json_data = {}
        self.data_keys = []
        self.shuf_indices = np.array([])
        self.input_label = []
        self.input_data = []
        self.word = ""        
        self.label_name = []

    def read_data(self):

        for files in os.listdir(self.MFCC_PATH):

            if (files.replace("_data.json","") in self.words):
                # open the JSON from the path containing the data JSON
                with open(os.path.join(self.MFCC_PATH,files)) as f_in:
                
                    new_data = json.load(f_in)

                    # load the data from the json into a dict
                    self.json_data.update(new_data)

                    # obtain list of keys
                    self.data_keys += new_data.keys()
                    
                    self.label_name += ([files.replace("_data.json","")] * len(new_data.keys()))

        # iterate through the list of ww train keys
        for i in range(len(self.data_keys)):
            
            # hash into the dict and store it in the input list
            self.input_data.append(self.json_data[self.data_keys[i]])

            # label the corresponding data
            self.input_label.append(self.one_hot_label(self.words[self.label_name[i]]))
            # stt.input_label.append(words[label_name[i]])


    def words_to_label(self):
        self.words_to_labels = {}

        for key in self.words.keys():
            self.words_to_labels[str(self.words[key])] = key

    def validation_set(self):
        inp = int(len(self.input_label) * 0.8)
        val = len(self.input_label) - inp

        print('inp', inp)
        print('val', val)
        self.valid_input = self.input_data[:val]
        self.valid_label = self.input_label[:val]
        self.input_data = self.input_data[val:]
        self.input_label = self.input_label[val:]

        print('val_inp',len(self.valid_input))
        print('val_label',len(self.valid_label))

        self.valid_input = np.array(self.valid_input, dtype=float)
        self.valid_label = np.array(self.valid_label, dtype=float)
    
    def npify(self):
        self.input_data = np.array(self.input_data, dtype=float)
        self.input_label = np.array(self.input_label, dtype=float)

    def one_hot_label(self, one_label):
        arr = [0] * self.NUM_CLASSES
        arr[one_label] = 1

        return np.array(arr)

    def shuffle_data(self):
        temp_data = [0]*len(self.input_label)
        temp_labels = [0]*len(self.input_label)
        self.shuf_indices = np.arange(len(self.input_label))
        np.random.shuffle(self.shuf_indices)
        
        for i in range(len(self.input_label)):
            temp_data[i] = self.input_data[self.shuf_indices[i]] 
            temp_labels[i] = self.input_label[self.shuf_indices[i]] 
                
        self.input_data = temp_data
        self.input_label = temp_labels

    def build_model(self):

        # define a model as a sequence of layers
        self.model = models.Sequential()

        self.model.add(layers.Dense(128, input_shape=(20,13), activation='relu'))
        self.model.add(layers.Dense(128, activation='relu'))
        self.model.add(layers.Dense(64, activation='relu'))
        self.model.add(layers.Dense(64, activation='relu'))

        # add first layer which is the GRU
        self.model.add(layers.GRU(self.GRU_UNITS, dropout=self.DROPOUT, name='net', input_shape=(20,13)))
        
        # add second layer which is a output for binary classification
        self.model.add(layers.Dense(self.NUM_CLASSES, activation='softmax'))

        # define loss and optimzer fns
        self.model.compile(optimizer='adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

    def train_model(self, val_bool):
        if not(val_bool):
            self.history = self.model.fit(self.input_data, self.input_label, epochs=self.EPOCHS, batch_size=self.BATCH_SIZE, verbose=1)
        else:
            self.history = self.model.fit(self.input_data, self.input_label, epochs=self.EPOCHS, validation_data=(self.valid_input, self.valid_label), batch_size=self.BATCH_SIZE, verbose=1)
        
        self.model.save(os.getcwd() + "\\Models\\STT\\stt_model_" + datetime.now().strftime("%m%d%Y%H%M%S%f") + ".h5")
        self.print_model()

    def load_model(self,model):
        self.model = models.load_model(os.getcwd() + "\\Models\\STT\\" + model)
        self.print_model()
        
    def print_model(self):
        print(self.model.summary())
