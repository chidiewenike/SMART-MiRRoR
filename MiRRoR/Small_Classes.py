from __future__ import print_function
import math
import time
import requests
import json
import os
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
#import cv2

json_dir = "/home/pi/API_Keys/"
with open(json_dir + 'api_keys.json') as f:
    api_keys = json.load(f)
    
class Email:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(json_dir + 'token_email.pickle'):
            with open(json_dir + 'token_email.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    json_dir + 'credentials_email.json', SCOPES)
                self.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(json_dir + 'token_email.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def check_email(self):
        ret_str = ""
        messages = []
       
        try:
            service = build('gmail', 'v1', credentials=self.creds)
            
            response = service.users().messages().list(userId='me',
                                                    labelIds='UNREAD').execute()
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId='me',
                                                        labelIds='UNREAD',
                                                        pageToken=page_token).execute()
            ret_str = "               NEW EMAIL (" + str(len(messages)) + ")\n\n"
            subject = ""
            from_val = ""
            email_list = []
            for i in range(len(messages)):
                curr_msg = service.users().messages().get(userId='me', id=messages[i]['id']).execute()
                for vals in curr_msg['payload']['headers']:
                    if vals['name'] == 'Subject':
                        subject = vals['value']
                    elif vals['name'] == 'From':
                        from_val = vals['value']
                        
                ret_str += str(i+1) + ". " + subject + "\n   " + from_val + "\n\n" #+ summary[:50] + "\n\n"
                        
                if (((i % 1 == 0) or (i == len(messages)-1)) or ((len(messages) < 1) and (i == len(messages)-1))):
                    email_list.append(ret_str)
                    ret_str = "             NEW EMAIL (" + str(len(messages)) + ")\n\n"
                
        except:
            pass
        
        if(len(messages) == 0):
            return ["                          EMAIL\n\n                   No New Emails  "]
            
        return email_list

class Tasks:
    def __init__(self):
        self.tasks = {}
        self.creds = None
        self.task_list = ""
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']        
        if os.path.exists(json_dir + 'token_task.pickle'):
            with open(json_dir + 'token_task.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    json_dir + 'credentials_task.json', SCOPES)
                self.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(json_dir + 'token_task.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def check_tasks(self):
        try:
            task_dict = {}
            service = build('tasks', 'v1', credentials=self.creds)
            tasks = service.tasks().list(tasklist='MTIyODQxNjE5ODU0MTUyMzc1MjM6MDow').execute()
            
            #print(tasks)
            for i in range(0,len(tasks['items'])):
                task_dict[tasks['items'][i]['position']] = tasks['items'][i]['title']

        except:
            pass 
        return task_dict

    def Return_Tasks(self):
        tasks_dict = self.check_tasks()
        ret_tasks = []
        task_list = "              TO-DO LIST\n\n"
        task_count = 0
        task_num = 1
        if not(tasks_dict):
            return ["              TO-DO LIST\n\n"]

        for key in sorted(tasks_dict):
            task_count+=1
            task_list += str(task_num) + ". " + tasks_dict[key] + "\n\n"
            task_num += 1
            
            if (task_count == 5):
                ret_tasks.append(task_list)
                task_list = "              TO-DO LIST\n\n"
                task_count = 0
                
        ret_tasks.append(task_list)
        return ret_tasks
    
class Alarm:
    def __init__(self):
        self.alarm1 = ["07","00"]
        self.alarm2 = ["",""]
        self.alarm3 = ["",""]
        self.alarm4 = ["",""]
        self.alarm5 = ["",""]
        self.snooze = "10"
        self.person = Facial_Recognition()

    def trigger_alarm(self, hour, minute):    
        if int(time.strftime("%H"))==int(self.alarm1[0]) and int(time.strftime("%M"))==int(self.alarm1[1]):
            import threading

            self.shut_off_sequence = False
            t1 = threading.Thread(target=self.play_sound, args=(10,)) 
            t2 = threading.Thread(target=self.rec_interrupt, args=(10,))            
            t1.start()
            t2.start()

        else:
            pass
            
    def play_sound(self):
        while not(self.shut_off_sequence):
            winsound.PlaySound(r'SMART-MiRRoR\\Random\\Alarm.wav', winsound.SND_ASYNC)

    def rec_interrupt(self):
        if (): # face recognized
            winsound.PlaySound(None, winsound.SND_PURGE)
            self.shut_off_sequence = True

        else:
            pass

class Weather:
    def __init__(self):

        self.weather_url = "https://api.darksky.net/forecast/" + api_keys["weather"] + "/35.28552,-120.6625"
        self.current_temp = ""
        self.curr_temp_high = ""
        self.curr_temp_lows = ""   
        self.current_image = ""
        self.image_dict = {"cloudy":["cloud.png","Cloudy"],"clear-night":["moon.png","Clear"], "clear-day":["sun.png","Clear"], "rain":["rain.png","Rain"],"snow":["snow.png","Snow"],"partly-cloudy-day":["partlycloudy.png","Partly Cloudy"],"partly-cloudy-night":["partly_cloudy_night.png","Partly Cloudy"],"fog":["fog.png","Foggy"],"wind":["wind.png","Windy"]}
        # [temp,high,low,icon]
        self.five_day_forecast = {"0":[],"1":[],"2":[],"3":[],"4":[],"5":[]}
        self.five_day_forecast = {"0":[],"1":[],"2":[],"3":[],"4":[],"5":[]}


    def Obtain_Current_Weather(self):
        import requests
        import json

        weather_respone = requests.get(self.weather_url)
        weather_data = json.loads(weather_respone.content.decode('utf-8'))
        self.current_temp = str(int(weather_data["hourly"]["data"][0]["temperature"]))
        self.curr_temp_high = str(int(weather_data["daily"]["data"][0]["temperatureHigh"]))
        self.curr_temp_lows = str(int(weather_data["daily"]["data"][0]["temperatureLow"]))
        self.current_image = str(weather_data["hourly"]["data"][0]["icon"])
        self.current_text = str(weather_data["hourly"]["data"][0]["icon"])

    def Obtain_Five_Day_Forecast(self):
        import requests
        import json

        curr_date_inc = datetime.datetime.today()
        #"°F (" + str(int((float(self.curr_temp_high)-32)*(5/9))) + "°C) - " + self.curr_temp_lows + "°F (" + str(int((float(self.curr_temp_lows)-32)*(5/9))) + "°C)"

        for i in range(0,5):
            curr_weather = []
            curr_date = curr_date_inc.strftime('%Y-%m-%d')
            weather_response = requests.get(self.weather_url+ "," + curr_date + "T12:00:00")
            weather_data = json.loads(weather_response.content.decode('utf-8'))

            curr_weather.append(str(int(weather_data["daily"]["data"][0]["temperatureHigh"])))
            curr_weather.append(str(int(weather_data["daily"]["data"][0]["temperatureLow"])))
            curr_weather.append(str(weather_data["daily"]["data"][0]["icon"]))
            curr_weather.append("  " + curr_date_inc.strftime('%a'))
            self.five_day_forecast[str(i)] = curr_weather

            curr_date_inc += datetime.timedelta(days=1)

        
    def Get_Weather_Curr_Image(self):
        return "/home/pi/Smart Mirror/MiRRoR/Images/Weather/" + self.image_dict[self.current_image][0] 

    def Get_Weather_Curr_Text(self):
        return self.current_temp + "°"
        
    def Get_Weather_Forecast_Image(self,day):
        return "/home/pi/Smart Mirror/MiRRoR/Images/Weather/" + self.image_dict[self.five_day_forecast[(day)][2]][0]

    def Get_Weather_Forecast_Text(self,day):
        if(day == "0"):
            return "Today" + "\n" + self.five_day_forecast[(day)][0] + " " + self.five_day_forecast[(day)][1]
        
        return self.five_day_forecast[(day)][3] + "\n" + self.five_day_forecast[(day)][0] + " " + self.five_day_forecast[(day)][1]


class Time:
    def __init__(self):
        self.time = ""
        self.date = ""

    def Get_Time(self):
        return self.time

    def Get_Date(self):
        return self.date
        
    def Find_Time(self):
        self.date = time.strftime("%a, %d %b %Y", time.localtime())
        self.time = time.strftime("%H:%M", time.localtime())
        return [self.date, self.time]    


class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.curr_time = ""
        self.timer = ""
    
    def Calc_Timer(self):
        self.curr_time = time.time()
        self.timer = (float(self.curr_time) - float(self.start_time))
        return self.timer

    def Reset_Timer(self):
        self.start_time = time.time()

class Quotes:
    def __init__(self):
        import json

        with open('quotes.json') as f:
            self.quote_data = json.load(f)

        self.quote = ""
        self.author = ""

    def Reload_Quotes(self):
        with open('quotes.json') as f:
            self.quote_data = json.load(f)
            
    def New_Quote(self):
        import random

        random_quote = random.choice(self.quote_data)
        self.quote = random_quote['quoteText']
        self.author = random_quote['quoteAuthor']

    def Get_Quote(self):
        return self.quote

    def Get_Author(self):
        return self.author

class Word_of_the_Day:

    def __init__(self):

        self.time = Time()
        self.month_map = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06"}
        self.time.Find_Time()
        date = self.time.Get_Date().split()
        self.api_call = "https://api.wordnik.com/v4/words.json/wordOfTheDay?date=" + date[3] + "-" + self.month_map[date[2]] + "-" + date[3] + "&api_key=" + api_keys["word"]
        self.word = ""
        self.definition = ""
        self.type = ""
        try:
            word_response = requests.get(self.api_call)
            word_data = json.loads(word_response.content.decode('utf-8'))
            self.word = word_data['word']
            self.definition = word_data['definitions'][0]['text']
            self.type = word_data['definitions'][0]['partOfSpeech']
        except:
            pass            
        
    def New_Word(self):

        self.time.Find_Time()
        date = self.time.Get_Date().split()
        word_response = requests.get(self.api_call)
        try:
            word_data = json.loads(word_response.content.decode('utf-8'))
            self.word = word_data["word"]
            self.definition = word_data["definitions"][0]["text"]
            self.type = word_data["definitions"][0]["partOfSpeech"]
        except:
            pass

class News:
    def __init__(self):
        self.bbc_news = {}
        self.ny_times = {}
        self.scientist = {}
        self.engadget = {}
        self.fft = {}
        self.bbc_news_title = ""
        self.bbc_news_description = ""
        self.ny_times_title = ""
        self.ny_times_description = ""
        self.scientist_title = ""
        self.scientist_description = ""
        self.engadget_title = ""
        self.engadget_description = ""
        self.fft_title = ""
        self.fft_description = ""

    def Reload_News(self):
        from newsapi import NewsApiClient

        newsapi = NewsApiClient(api_key=api_keys["news"])

        self.bbc_news = newsapi.get_top_headlines(sources='bbc-news')
        self.ny_times = newsapi.get_top_headlines(sources='the-new-york-times')
        self.scientist = newsapi.get_top_headlines(sources='new-scientist')
        self.engadget = newsapi.get_top_headlines(sources='engadget')
        self.fft = newsapi.get_top_headlines(sources='four-four-two')


    def Cycle_News(self,count):
        title = self.bbc_news['articles'][count]['title']
        description = self.bbc_news['articles'][count]['description']

        if not(title == None) and not (description == None):
            self.bbc_news_title = title
            self.bbc_news_description = description 
        
        title = self.ny_times['articles'][count]['title']
        description = self.ny_times['articles'][count]['description']

        if not(title == None) and not (description == None):        
            self.ny_times_title = title
            self.ny_times_description = description

        title = self.scientist['articles'][count]['title']
        description = self.scientist['articles'][count]['description']  

        if not(title == None) and not (description == None):
            self.scientist_title = self.scientist['articles'][count]['title']
            self.scientist_description = self.scientist['articles'][count]['description']  

        title = self.engadget['articles'][count]['title']
        description = self.engadget['articles'][count]['description']    

        if not(title == None) and not (description == None):
            self.engadget_title = title
            self.engadget_description = description

        title = self.fft['articles'][count]['title']
        description = self.fft['articles'][count]['description']

        if not(title == None) and not (description == None):
            self.fft_title = title
            self.fft_description = description


class Personal_Schedule:
    def __init__(self):
        self.events = {}
        self.sched_list = []
        import pickle
        import os.path
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import datetime

        
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

        self.creds = None
        if os.path.exists(json_dir + 'token_cal.pickle'):
            with open(json_dir + 'token_cal.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    json_dir + 'credentials_cal.json', SCOPES)
                self.creds = flow.run_local_server()

            with open(json_dir + 'token_cal.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def check_calendar(self):
        service = build('calendar', 'v3', credentials=self.creds)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=16, singleEvents=True,
                                            orderBy='startTime').execute()

        events = events_result.get('items', [])
        print(events)
        if not events:
            print('No upcoming events found.')
        count = 1
        for event in events:
            self.events[str(count)] = event
            start = event['start'].get('dateTime', event['start'].get('date'))
            count += 1
    
    def List_Events(self):
        sched_list = "                      Schedule\n\n"
        
                
        self.check_calendar()
        self.sched_list = []
        for i in range(1,17):
                if ('location' in self.events[str(i)]):
                    event = "• " + self.events[str(i)]['start']['dateTime'][5:10] + " | " + self.events[str(i)]['start']['dateTime'][11:16] + " | " + self.events[str(i)]['summary'] + "\n   " + self.events[str(i)]['location'] + "\n\n"
                else:
                    event = "• " + self.events[str(i)]['start']['dateTime'][5:10] + " | " + self.events[str(i)]['start']['dateTime'][11:16] + " | " + self.events[str(i)]['summary'] + "\n\n"
                print("e", event)
                sched_list += event
                print("sl", sched_list)
                if i == 8 or i == 16:
                    self.sched_list.append(sched_list)
                    sched_list = "                      Schedule\n\n"


        '''
        try:
            self.check_calendar()
            self.sched_list = []
            for i in range(1,17):
                    if ('location' in self.events[str(i)]):
                        event = "• " + self.events[str(i)]['start']['dateTime'][5:10] + " | " + self.events[str(i)]['start']['dateTime'][11:16] + " | " + self.events[str(i)]['summary'] + "\n   " + self.events[str(i)]['location'] + "\n\n"
                    else:
                        event = "• " + self.events[str(i)]['start']['dateTime'][5:10] + " | " + self.events[str(i)]['start']['dateTime'][11:16] + " | " + self.events[str(i)]['summary'] + "\n\n"
                    print("e", event)
                    sched_list += event
                    print("sl", sched_list)
                    if i == 8 or i == 16:
                        self.sched_list.append(sched_list)
                        sched_list = "                      Schedule\n\n"
        except:
            print("ERROR")
        '''
        if self.sched_list == []:
            return ["                      Schedule\n\n"]

        return self.sched_list
    
    def Return_Events(self):
        return self.events
    
class Facial_Recognition:
    def __init__(self):
        pass

class Text_To_Speech:
    def __init__(self):
        pass

class Speech_To_Text:
    def __init__(self):
        pass

class Person_Recognizer:
    def __init__(self):
        pass

class Music:
    def __init__(self):
        self.music_path = os.getcwd()
        self.playlist_name = self.music_path
        self.artist = ""
        self.song = ""
        self.title = ""
        self.length = 0
        self.playlist = []
        self.play_count = 0
        self.curr_count = 0
        self.repeat = False
        self.mode = 0

    def get_music_list(self,playlist):
        self.playlist_name = os.getcwd() + playlist
        self.playlist = os.listdir(self.playlist_name)   
        self.play_count = len(self.playlist)

    def next_song(self):

        if(self.curr_count < self.play_count):
            self.curr_count+=1
            self.music_choice = self.playlist_name + "\\" + self.playlist[self.curr_count]
            self.title = self.playlist[self.curr_count]
        
        elif((self.curr_count < self.play_count) and self.repeat):
            self.curr_count = 0
            self.music_choice = self.playlist_name + "\\" + self.playlist[self.curr_count]
        
        elif((self.curr_count < self.play_count) and not self.repeat):
            self.curr_count = 0
            self.Stop_Song()

    def play_song(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_choice)
        pygame.mixer.music.play()
        self.mode = 1
        # while pygame.mixer.music.get_busy() == True:
        #     time.sleep(3)
        #     self.Pause_Song()
        #     continue

    def Stop_Song(self):
        pygame.mixer.init()
        pygame.mixer.music.stop()
        self.mode = 0

    def Pause_Song(self):
        pygame.mixer.init()
        pygame.mixer.music.pause()
        self.mode = 2

    def Resume_Song(self):
        pygame.mixer.init()
        pygame.mixer.music.unpause()
        self.mode = 1

    def Parse_Title(self):
        self.title = self.title[:len(self.title)-4]
        self.title = self.title.replace('-', ' ')
        title_list = self.title.split()
        self.song = title_list[1]
        self.artist = title_list[0]
        self.length = int(title_list[2])

    def Get_Song(self):
        return self.song

    def Get_Artist(self):
        return self.artist
    
class NextMatch:
    def __init__(self):
        self.cred = credentials.Certificate(json_dir+"firestore.json")
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()  
        self.teams = {}
        self.teams["Everton"] = Team()
        self.teams["Finland"] = Team()
        self.teams["Nigeria"] = Team()
        self.teams["US"] = Team()
        self.teams["LAFC"] = Team()

    def Load_Match(self,team):
        docs = self.db.collection(u'Football').document(u'7CieuAL9oIdvE2C2MRuv').collection(u'' + team).limit(1).get()
        for doc in docs:
            next_match = doc.to_dict()
            self.teams[team].match_id = doc.id
        if not(self.teams[team].match_id == "Match 99999999"):
            self.teams[team].date = next_match["Date"].replace("/"," ").split()[1:]
            self.teams[team].time = next_match["Time"].replace(":"," ").split() 
            self.teams[team].team = next_match["Team"]
            self.teams[team].HA = next_match["H/A"]
        else:
            self.teams[team].date = "N/A"
            self.teams[team].time = "N/A"
            self.teams[team].team = "N/A"
            self.teams[team].HA = "Home"
    def Get_Teams(self):
        return self.teams

    def Check_Match_Date(self,team):
        date = time.strftime("%m %d", time.localtime()).split()
        if (date[0] > self.teams[team].date[0]) or ((date[0] == self.teams[team].date[0]) and (date[1] > self.teams[team].date[1])):
            return True
        return False

    def Match_In_Progress(self,team):

        if(self.Check_Match_Date(team)):
            self.db.collection(u'Football').document(u'7CieuAL9oIdvE2C2MRuv').collection(u'' + team).document(u''+self.teams[team].match_id).delete()
            self.Load_Match(team)

        if (self.teams[team].HA == "Home"):
            return [team, self.teams[team].team]

        return [self.teams[team].team, team]
        
class Team:
    def __init__(self):
        self.team = ""
        self.date = []
        self.time = []
        self.HA = ""
        self.match_id = ""

    def Set_Fixture(self, team, date, time, HA):
        self.team = team
        self.date = date
        self.time = time
        self.HA = HA


#a = Personal_Schedule()
#a.List_Events()

t = Tasks()
(t.Return_Tasks())
'''
b = Email()
print(b.check_email())
'''
