import tensorflow as tf
from tensorflow.keras import models, layers 
import numpy as np
import os
import pyaudio
from speechpy.feature import mfcc
from datetime import datetime 
import wave
import matplotlib.pyplot as plt
from stt_model import Model
from feature_extraction_final_code import Feature_Extraction
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', action='store', dest='simple_value', default='')
parser.add_argument('-e', action='store', dest='epochs', default='25')
parser.add_argument('-f',nargs="+", dest='list', default=[])
parser.add_argument('-p', action="store_true")
parser.add_argument('-v', action="store_true")
args = parser.parse_args()


BCKRD_PATH = os.getcwd() + "\\Data\\STT_Data\\Audio\\background_noise\\"
MFCC_PATH = os.getcwd() + "\\Data\\STT_Data\\STT_MFCC\\"

ACTIVATIONS = 2
CONFIDENCE = 0.45

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

read = 0
label_name = []

ext_feat = Feature_Extraction()
stt = Model(int(args.epochs))
p = pyaudio.PyAudio()

if args.simple_value=='':
    # load the desired model
    ext_feat.Obtain_STT_Audio_Data()
    stt.read_data()
    stt.shuffle_data()

    if(args.v):
        stt.validation_set()

    stt.npify()
    stt.build_model()
    stt.train_model(args.v)

    if (args.v):

        plt.plot(stt.history.history['accuracy'])
        plt.plot(stt.history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        # summarize history for loss
        plt.plot(stt.history.history['loss'])
        plt.plot(stt.history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

else:
    stt.load_model(args.simple_value)


# open an audio data stream
stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)

# contains the chunks of streamed data
frames = []

# false activation mode indicator
false_act = 0

# counts for confident activations
act_count = 0

false_counts = 0

false_files = []

if (args.list != []):
        print("\n||| FALSE ACTIVATION MODE |||")
        location = args.list[0]
        description = args.list[1]
        noise = args.list[2]
print()
while True:

    # reads chunk of audio
    data = stream.read(CHUNK)
    
    # appends chunk to frame list
    frames.append(data)

    # begins making predictions after the first 2.5 seconds of audio is read
    if (len(frames) > 11):

        # converts first 19 chunks of audio bytes into 16 bit int values
        in_data = np.fromstring(np.array(frames[:11]),'Int16')
        
        # extract MFCCs from the 19 chunks of audio
        audio_sig = mfcc(in_data,RATE,WINDOW,STRIDE,MFCC,FILTER_BANKS,FFT_NUM,0,None,True)
              
        audio_sig = np.array([audio_sig])

        pred = stt.model.predict(audio_sig)
        # makes predictions
        prediction = np.argmax(pred)

        if(args.p):
            print(pred)


        # if the predictions is larger than the defined confidence
        # if (prediction > CONFIDENCE):
        if ((pred[0][prediction] > CONFIDENCE) and (prediction != 0)):

            # increment the activation counter
            act_count+=1

            # if the number of consecutive activations exceeds the activation value
            if(act_count >= ACTIVATIONS):

                print( "|||" + (stt.words_to_labels[str(prediction)]).upper() + "|||",end=" ",flush=True)

                if(args.list != []):
                    false_counts += 1
                    # store the wav
                    file_name = "false" + "_" + location + "_" + noise + "_" + datetime.now().strftime("%m%d%Y%H%M%S%f") + "_ewenike.wav" 
                    wf = wave.open(os.path.join(BCKRD_PATH,file_name), 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames[:11]))
                    wf.close()
                    print("\n<<" + file_name + ">> has been saved\n")
                

                    if (false_counts >= FALSE_COUNT):
                        stream.close()
                        false_counts = 0
                        false_files = []
                        ext_feat.Obtain_STT_Audio_Data()
                        stt = Model(int(args.epochs))
                        stt.read_data()
                        stt.shuffle_data()
                        if(args.v):
                            stt.validation_set()
                        stt.npify()
                        stt.build_model()
                        stt.train_model(args.v)

                        stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
                frames = frames[11:]

                # reset activation count
                act_count = 0


        # if prediction falls below the confidence level                
        else:

            # reset the activation count
            act_count = 0

            # output nothing to the stream
            print(".", end = "", flush=True)
        
        # window the data stream
        frames = frames[1:]
