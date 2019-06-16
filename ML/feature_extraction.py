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

def Convert_To_MFCC(wf):
        return mfcc(Read_Audio_Data(wf),RATE,WINDOW,STRIDE,MFCC,FILTER_BANKS,FFT_NUM,0,None,True).tolist()

def Read_Audio_Data(wf):

        #get the packed bytes
        raw_sig = wf.readframes(wf.getnframes())

        #convert the packed bytes into integers
        audio_sig = (np.fromstring(raw_sig, 'Int16')).tolist()

        if (len(audio_sig) < 22528):
                for i in range(22528 - len(audio_sig)):
                        audio_sig.append(0)

        # close the file
        wf.close()

        return np.array(audio_sig)

def Obtain_Audio_Data():

        # desired dir for data extraction
        audio_dir = CURR_PATH + "Data\\"

        #words_files_list = os.listdir(audio_dir)
        words_files_list = sys.argv[1:]
        for dirs in words_files_list:
                
                # obtain files within the dir
                audio_list = os.listdir(audio_dir + dirs)

                data_dir = audio_dir + dirs + "\\"

                # name of the json file based on user input
                json_type = CURR_PATH + "MFCC\\" + dirs + "_data.json"

                # data dictionary
                curr_data = {}
                print(dirs)
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
                                        mfcc = Convert_To_MFCC(wf)
                                        curr_data[sample.replace(".wav","")] = mfcc
                                
                                else:
                                        print("<<" + sample + ">> is of invalid format.")

                # place contents into the json 
                with open(json_type, 'w') as outfile:
                        json.dump(curr_data, outfile)

                print("<<" + json_type + ">> has been stored in the directory: " + str(os.getcwd()))

if __name__ == '__main__':

        Obtain_Audio_Data()