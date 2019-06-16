import tensorflow as tf
from tensorflow.keras import layers, models
import os
import json
import numpy as np
import random
from datetime import datetime

class Model:

    def __init__(self):

        self.NWW_PATH = os.getcwd() + "\\Data\\WW_Data\\Not_Wake_Word"
        self.JSON_PATH = os.getcwd() + "\\Data\\WW_Data\\WW_MFCC"

        # name of json data files
        self.WW_TRAIN = "Wake_Word_Train_data.json"
        self.NWW_TRAIN = "Not_Wake_Word_Train_data.json"
        self.WW_TEST = "Wake_Word_Test_data.json"
        self.NWW_TEST = "Not_Wake_Word_Test_data.json"

        self.CONFIDENCE = 0.6 # prediction confidence 
        self.GRU_UNITS = 64 # GRU unit size
        self.DROPOUT = 0.3 # dropout size
        self.ACTIVATIONS = 4 # number of activations for confident activation
        self.EPOCHS = 20 # number of fwd and bckwd props
        self.BATCH_SIZE = 8 # batch size

        self.ww_test_data = {}
        self.ww_test_data_keys = []
        self.ww_train_data = {}
        self.ww_train_data_keys = []

        # not wake word train & test data with shuffled list of keys
        self.nww_test_data = {}
        self.nww_test_data_keys = []
        self.nww_train_data = {}
        self.nww_train_data_keys = []

        # input list of training & test data and labels
        self.train_data = []
        self.train_labels = []
        self.test_data = []
        self.test_labels = []

    def build_model(self):

        # define a model as a sequence of layers
        self.model = models.Sequential()

        self.model.add(layers.Dense(units=16,activation='relu', input_shape=(36,13)))
        self.model.add(layers.Dense(units=16,activation='relu'))
        self.model.add(layers.Dense(units=16,activation='relu'))
        self.model.add(layers.Dense(units=16,activation='relu'))
        self.model.add(layers.Dense(units=16,activation='relu'))
        self.model.add(layers.Dense(units=16,activation='relu'))
        self.model.add(layers.Dense(units=16,activation='relu'))
        self.model.add(layers.Dense(units=16,activation='relu'))

        # add first layer which is the GRU
        self.model.add(layers.GRU(self.GRU_UNITS, activation='linear',dropout=self.DROPOUT))
        
        # add second layer which is a output for binary classification
        self.model.add(layers.Dense(1, activation='sigmoid'))

        # define loss and optimzer fns
        self.model.compile(optimizer='adam', loss = 'binary_crossentropy', metrics = ['acc'])
        
    def preprocess(self):  
        
        # open the JSON from the path containing the data JSON
        with open(os.path.join(self.JSON_PATH,self.WW_TRAIN)) as f_in:

            # load the data from the json into a dict
            self.ww_train_data = json.load(f_in)

            # obtain list of keys
            self.ww_train_data_keys = list(self.ww_train_data.keys())

            # shuffle the list
            random.shuffle(self.ww_train_data_keys)

        # open the JSON from the path containing the data JSON
        with open(os.path.join(self.JSON_PATH,self.NWW_TRAIN)) as f_in:
            
            # load the data from the json into a dict
            self.nww_train_data = json.load(f_in)

            # obtain list of keys
            self.nww_train_data_keys = list(self.nww_train_data.keys())

            # shuffle the list
            random.shuffle(self.nww_train_data_keys)


        # open the JSON from the path containing the data JSON
        with open(os.path.join(self.JSON_PATH,self.WW_TEST)) as f_in:

            # load the data from the json into a dict
            self.ww_test_data = json.load(f_in)

            # obtain list of keys
            self.ww_test_data_keys = list(self.ww_test_data.keys())

            # shuffle the list
            random.shuffle(self.ww_test_data_keys)

        # open the JSON from the path containing the data JSON
        with open(os.path.join(self.JSON_PATH,self.NWW_TEST)) as f_in:

            # load the data from the json into a dict
            self.nww_test_data = json.load(f_in)

            # obtain list of keys
            self.nww_test_data_keys = list(self.nww_test_data.keys())
    
            # shuffle the list
            random.shuffle(self.nww_test_data_keys)

        # iterate through the list of ww train keys
        for i in range(len(self.ww_train_data_keys)):

            # hash into the dict and store it in the input list
            self.train_data.append(self.ww_train_data[self.ww_train_data_keys[i]])
            
            # label the corresponding data
            self.train_labels.append(1)

        # iterate through the list of nww train keys
        for i in range(len(self.nww_train_data_keys)):

            # hash into the dict and store it in the input list
            self.train_data.append(self.nww_train_data[self.nww_train_data_keys[i]])
            
            # label the corresponding data
            self.train_labels.append(0)

        # iterate through the list of ww test keys
        for i in range(len(self.ww_test_data_keys)):

            # hash into the dict and store it in the input list
            self.test_data.append(self.ww_test_data[self.ww_test_data_keys[i]])
            
            # label the corresponding data
            self.test_labels.append(1)

        # iterate through the list of nww test keys
        for i in range(len(self.nww_test_data_keys)):

            # hash into the dict and store it in the input list
            self.test_data.append(self.nww_test_data[self.nww_test_data_keys[i]])

            # label the corresponding data
            self.test_labels.append(0)

        # convert the data lists to np arrays of type float
        self.test_data = np.array(self.test_data, dtype=float)
        self.train_data = np.array(self.train_data, dtype=float)
        self.test_labels = np.array(self.test_labels, dtype=float)
        self.train_labels = np.array(self.train_labels, dtype=float)

    def train_model(self):
        self.history = self.model.fit(self.train_data, self.train_labels, epochs=self.EPOCHS, batch_size=self.BATCH_SIZE, verbose=1, validation_data=(self.test_data,self.test_labels))
        print(self.model.evaluate(self.test_data,self.test_labels))
        self.model.save(os.getcwd() + "\\Models\\WW\\ww_model_" + datetime.now().strftime("%m%d%Y%H%M%S_") + str(int(((self.history.history['acc'])[self.EPOCHS-1])*100)) + ".h5")

    def load(self,model_name):
        self.model = models.load_model(os.getcwd() + "\\Models\\WW\\" + model_name)
