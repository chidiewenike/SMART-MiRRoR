import wave
import pyaudio
import os
import time

CHUNK = 2048
FORMAT = pyaudio.paInt16 # 16 bit int sample size
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 1.5

LOOPS = 1

quit_inp = 0 # var for quitting out of program

# list of words
words = {'background_noise', 'rap', 'rnb', 'other', 'weather', 'home', 'work', 'school', 'sleep', 'news', 'main'}
print("\nData Count\n============================================================================")
for files in os.listdir(os.getcwd() + "\\Data\\STT_Data\\Audio\\"):
        print(files, end=': ', flush=True)
        print(len(os.listdir(os.getcwd() + "\\Data\\STT_Data\\Audio\\" + files)))
print("============================================================================\n")

# program loop
while (quit_inp != 'q'):    

        word = 0 # word label
        gender = 0 # gender label
        end_desc_sess = 0 # ends the current description session

        # ensures proper word input
        while not(word in words): 
                word = input("Enter the name of the desired word: ").lower()

        noise_level = 0

        added_features = (input("Enter the additional feature descriptions: ").lower()).replace(" ","-") # labeling brief description
        rec_location = (input("Location: ").lower()).replace(" ","-") # labeling the recording location

        while not(noise_level == 'q' or noise_level == 'm' or noise_level == 'l'):
                noise_level = input("Noise Level - Quiet (Q) Moderate (M) Loud (L): ").lower()

                # description session loop
                while (True):
        
                        # instantiate a PyAudio 
                        p = pyaudio.PyAudio()

                        # arrays of audio byte streams
                        frames = []

                        print("Recording in\n")
                        for i in range(LOOPS):
                                print(str(LOOPS-i) + "\n")
                                time.sleep(1)
                        print("**RECORDING**")

                        # start audio stream
                        stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, output = True, frames_per_buffer = CHUNK)
                        # read audio and add to the frames
                        for i in range(0,int(RATE/CHUNK * RECORD_SECONDS)):
                                print("Time remaining: " + str(RECORD_SECONDS - (0.128 * (i+1))))
                                data = stream.read(CHUNK)
                                frames.append(data)

                        count = 0

                        print("**RECORDING ENDED**")

                        # playback the audio
                        for values in frames:
                                stream.write(values)

                        # stop the stream
                        stream.stop_stream()
                        stream.close()

                        # end PyAudio instantiation
                        p.terminate()

                        print("Number of %s samples: " % word, end = '', flush = True )
                        print(len(os.listdir(os.getcwd() + "\\Data\\STT_Data\\Audio\\" + word))+1)
                        if (input("To delete, type (d): ").lower() == 'd'):
                                pass

                        else:
                                curr_time = time.strftime("%m%d%Y%H%M%S", time.localtime())

                                #### CHANGE YOUR LASTNAME HERE ####
                                file_name = word + "_" + rec_location + "_" + noise_level + "_" + curr_time + "_ewenike.wav" # last name format "_ewenike.wav"

                                print(file_name + " has been saved.")

                                wf = wave.open(os.getcwd() + "\\Data\\STT_Data\\Audio\\" + word + "\\" + file_name, 'wb')
                                wf.setnchannels(CHANNELS)
                                wf.setsampwidth(p.get_sample_size(FORMAT))
                                wf.setframerate(RATE)
                                wf.writeframes(b''.join(frames))
                                wf.close()

        quit_inp = input("If finished recording, type (q). Otherwise, type anything else: ").lower()