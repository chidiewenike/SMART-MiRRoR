import pyaudio
import wave
import numpy as np
import os
from speechpy.feature import mfcc
import json
import sys

# CONSTANTS
RATE = 16000 # sample rate
WINDOW = 0.128 # size of window
STRIDE = 0.064 # time between each window
MFCC = 13 # number of desired MFCCs
FILTER_BANKS = 20 # number of filter banks to compute
FFT_NUM = 512 # length of fast fourier transform window
CURR_PATH = os.getcwd() + "\\" # current path

class Feature_Extraction:
        def __init__(self):
                self.words = {'background_noise':0, 'rap':1, 'rnb':2, 'other':3, 'weather':4, 'home':5, 'work':6, 'school':7, 'sleep':8, 'news':9, 'main':10}


        def Convert_To_MFCC(self, wf):
                return mfcc(self.Read_Audio_Data(wf),RATE,WINDOW,STRIDE,MFCC,FILTER_BANKS,FFT_NUM,0,None,True).tolist()

        def Read_Audio_Data(self, wf):

                #get the packed bytes
                raw_sig = wf.readframes(wf.getnframes())

                #convert the packed bytes into integers
                audio_sig = np.fromstring(raw_sig, 'Int16')

                # close the file
                wf.close()

                return audio_sig

        def Obtain_WW_Audio_Data(self):
                data_dirs = ['Data\\WW_Data\\Not_Wake_Word\\Train','Data\\WW_Data\\Not_Wake_Word\\Test','Data\\WW_Data\\Wake_Word\\Train','Data\\WW_Data\\Wake_Word\\Test']

                for data_inp in data_dirs:
                        # desired dir for data extraction
                        audio_dir = CURR_PATH + data_inp + "\\"

                        # obtain files within the dir
                        audio_list = os.listdir(audio_dir)

                        word = data_inp.split("\\")[2]

                        type_of_data = data_inp.split("\\")[3]

                        # name of the json file based on user input
                        json_type = word + "_" + type_of_data + "_data.json"

                        # data dictionary
                        curr_data = {}

                        # if the file is not within the directory
                        if not(os.path.isfile(json_type)):

                                # create the file
                                inp_file = open(json_type,'w')
                                inp_file.close()

                                # add the dict to the json
                                with open(json_type, 'a') as outfile:
                                        json.dump(curr_data, outfile)

                        # load the contents of the data json
                        with open(json_type) as f_in:
                                curr_data = json.load(f_in)

                        # obtain each audio sample from the desired dir
                        for sample in audio_list:

                                # process the sample if it is not processed yet
                                if (sample not in curr_data):
                                        wf = wave.open(audio_dir + sample, 'rb')

                                        if (wf.getnchannels() == 1 and wf.getsampwidth() == 2 and wf.getframerate() == 16000):
                                                mfcc = self.Convert_To_MFCC(wf)
                                                curr_data[sample.replace(".wav","")] = mfcc

                        # place contents into the json 
                        with open(os.getcwd() + "\\Data\\WW_Data\\WW_MFCC\\" + json_type, 'w') as outfile:
                                json.dump(curr_data, outfile)

                        print("<<" + json_type + ">> has been stored in the directory: " + str(os.getcwd()))

        def Obtain_STT_Audio_Data(self):

                # desired dir for data extraction
                audio_dir = CURR_PATH + "Data\\STT_Data\\Audio\\"

                words_files_list = os.listdir(audio_dir)

                for dirs in words_files_list:
                        print(dirs)
                        if dirs in self.words:  

                                # obtain files within the dir
                                audio_list = os.listdir(audio_dir + dirs)

                                data_dir = audio_dir + dirs + "\\"

                                # name of the json file based on user input
                                json_type = CURR_PATH + "Data\\STT_Data\\STT_MFCC\\" + dirs + "_data.json"

                                # data dictionary
                                curr_data = {}

                                # if the file is not within the directory
                                if not(os.path.isfile(json_type)):

                                        # create the file
                                        inp_file = open(json_type,'w')
                                        inp_file.close()

                                        # add the dict to the json
                                        with open(json_type, 'a') as outfile:
                                                json.dump(curr_data, outfile)

                                # load the contents of the data json
                                with open(json_type) as f_in:
                                        curr_data = json.load(f_in)

                                # obtain each audio sample from the desired dir
                                for sample in audio_list:

                                        # process the sample if it is not processed yet
                                        if (sample not in curr_data):
                                                
                                                # open a wav file
                                                wf = wave.open(data_dir + sample, 'rb')

                                                # ensures data is of the correct format
                                                if (wf.getnchannels() == 1 and wf.getsampwidth() == 2 and wf.getframerate() == 16000):
                                                        mfcc = self.Convert_To_MFCC(wf)
                                                        curr_data[sample.replace(".wav","")] = mfcc
                                                
                                                else:
                                                        print("<<" + sample + ">> is of invalid format.")

                        # place contents into the json 
                        with open(json_type, 'w') as outfile:
                                json.dump(curr_data, outfile)

                        print("<<" + json_type + ">> has been stored in the directory: " + str(os.getcwd()))
