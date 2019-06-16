import tensorflow as tf
from tensorflow.keras import models, layers 
from feature_extraction_final_code import Feature_Extraction
import json
import numpy as np
import os
import pyaudio
from speechpy.feature import mfcc
from datetime import datetime 
import wave
import random 
from ww_model import Model
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', nargs='+')
parser.add_argument('-f', nargs='+')
parser.add_argument('-p', action="store_true")
args = parser.parse_args()

NWW_PATH = os.getcwd() + "\\Data\\Not_Wake_Word"

CONFIDENCE = 0.6 # prediction confidence 
ACTIVATIONS = 4 # number of activations for confident activation

FALSE_COUNT = 4

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

WINDOW = 0.128 # size of window
STRIDE = 0.064 # time between each window
MFCC = 13 # number of desired MFCCs
FILTER_BANKS = 20 # number of filter banks to compute
FFT_NUM = 512 # length of fast fourier transform window

p = pyaudio.PyAudio()
ww_model = Model()
ext_feat = Feature_Extraction()

read = args.t[0]

if read == "y":
    extract_features = 0

    extract_features = args.t[1]

    if (extract_features == "y"):
        ext_feat.Obtain_WW_Audio_Data()

    ww_model.build_model()
    ww_model.preprocess()
    ww_model.train_model()

else:

    model = 0

    model = args.t[1]

    # load the desired model
    ww_model.load(model)

# print the summary of the model
print(ww_model.model.summary())

# open an audio data stream
stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)

# contains the chunks of streamed data
frames = []

# false activation mode indicator
false_act = 0

false_counts = 0
false_files = []

# counts for confident activations
act_count = 0

false_act = args.f[0]

if (false_act == "y"):
    location = args.f[1]
    description = args.f[2]

print()
while True:

    # reads chunk of audio
    data = stream.read(CHUNK)
    
    # appends chunk to frame list
    frames.append(data)

    # begins making predictions after the first 2.5 seconds of audio is read
    if (len(frames) > 19):

        # converts first 19 chunks of audio bytes into 16 bit int values
        in_data = np.fromstring(np.array(frames[:19]),'Int16')
        
        # extract MFCCs from the 19 chunks of audio
        audio_sig = np.array([mfcc(in_data,RATE,WINDOW,STRIDE,MFCC,FILTER_BANKS,FFT_NUM,0,None,True)])
        
        # makes predictions
        prediction = ww_model.model.predict(audio_sig)

        if(args.p):
            print(prediction)

        # if the predictions is larger than the defined confidence
        if (prediction > CONFIDENCE):

            # increment the activation counter
            act_count+=1

            # if the number of consecutive activations exceeds the activation value
            if(act_count >= ACTIVATIONS):

                # print out "NIMBUS"
                print(" << NIKOLA >> ",end=" ",flush=True)
                
                # reset activation count
                act_count = 0

                # if false activation occurs in false activation mode
                if(false_act == "y"):
                    false_counts += 1

                    # store the wav
                    file_name = "notww_" + description + "-false_"+ location + "_" + datetime.now().strftime("%m%d%Y%H%M%S%f") + "_ewenike.wav" 
                    wf = wave.open(os.path.join(NWW_PATH,file_name), 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames[:19]))
                    wf.close()
                    print("\n<<" + file_name + ">> has been saved\n")

                    false_files.append(file_name)

                frames = frames[19:]

            if (false_counts >= FALSE_COUNT):
                stream.close()

                random.shuffle(false_files)

                for files in false_files[:3]:
                    os.rename(os.getcwd() + "\\Data\\WW_Data\\Not_Wake_Word\\" + files, os.getcwd() + "\\Data\\WW_Data\\Not_Wake_Word\\Train\\" + files)

                os.rename(os.getcwd() + "\\Data\\WW_Data\\Not_Wake_Word\\" + false_files[3], os.getcwd() + "\\Data\\WW_Data\\Not_Wake_Word\\Test\\" + false_files[3])

                false_counts = 0
                false_files = []
                ext_feat.Obtain_WW_Audio_Data()
                ww_model = Model()
                ww_model.build_model()
                ww_model.preprocess()
                ww_model.train_model()

                stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)

        # if prediction falls below the confidence level                
        else:

            # reset the activation count
            act_count = 0

            if not(args.p):
                # output nothing to the stream
                print(".", end = "", flush=True)

        # window the data stream
        frames = frames[1:]
