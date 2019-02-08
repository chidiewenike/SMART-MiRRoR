from __future__ import print_function
import time
import requests
import json
import winsound
import os
class Alarm:
    def __init__(self):
        self.alarm1 = ["",""]
        self.alarm2 = ["",""]
        self.alarm3 = ["",""]
        self.alarm4 = ["",""]
        self.alarm5 = ["",""]
        self.snooze = "10"
        self.person = Facial_Recognition()

    def trigger_alarm(self, hour, minute):    
        if time.strftime("%H")==hour and time.strftime("%M")==minute:
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

        self.weather_url = "<Insert API CALL>"
        self.current_weather = ""
        self.current_temp = ""
        self.forecast_summary = ""
        self.temp_high = ""
        self.temp_lows = ""   
        self.current_image = ""
        self.image_dict = {"cloudy":["cloud.png","Cloudy"],"clear-night":["moon.png","Clear"], "clear-day":["sun.png","Clear"], "rain":["rain.png","Rain"],"snow":["snow.png","Snow"],"partly-cloudy-day":["partlycloudy.png","Partly Cloudy"],"partly-cloudy-night":["partly_cloudy_night.png","Partly Cloudy"],"fog":["fog.png","Foggy"],"wind":["wind.png","Windy"]}

    def Obtain_Current_Weather(self):
        import requests
        import json

        weather_respone = requests.get(self.weather_url)
        weather_data = json.loads(weather_respone.content)

        self.current_weather = weather_data["hourly"]["data"][0]["summary"]
        self.current_temp = str(int(weather_data["hourly"]["data"][0]["temperature"]))
        self.forecast_summary = weather_data["daily"]["data"][0]["summary"]
        self.temp_high = str(int(weather_data["daily"]["data"][0]["temperatureHigh"]))
        self.temp_lows = str(int(weather_data["daily"]["data"][0]["temperatureLow"]))
        self.current_image = str(weather_data["hourly"]["data"][0]["icon"])
        self.current_text = str(weather_data["hourly"]["data"][0]["icon"])

    def Obtain_Sev_Day_Forecast(self):
        import requests
        import json

        weather_respone = requests.get(self.weather_url)
        weather_data = json.loads(weather_respone.content)

        self.current_weather = weather_data["hourly"]["data"][0]["summary"]
        self.current_temp = str(int(weather_data["hourly"]["data"][0]["temperature"]))
        self.forecast_summary = weather_data["daily"]["data"][0]["summary"]
        self.temp_high = str(int(weather_data["daily"]["data"][0]["temperatureHigh"]))
        self.temp_lows = str(int(weather_data["daily"]["data"][0]["temperatureLow"]))
        self.current_image = str(weather_data["hourly"]["data"][0]["icon"])



    def Get_Weather_Image(self):
        #print(self.image_dict[self.image_dict] )
        return self.image_dict[self.current_image][0] 

    def Get_Weather_Text(self):
        return " " + self.image_dict[self.current_image][1] + "\n High: " + self.temp_high + " F (" + str(int((float(self.temp_high)-32)*(5/9))) + " C) Low: " + self.temp_lows + " F"

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
        self.time = time.strftime("%X", time.localtime())
        return [self.date,self.time]    

class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.curr_time = ""
        self.timer = ""
        self.hours = str(int(self.timer) // 60)
        self.minutes = str(int(self.timer) % 60)
    
    def Calc_Timer(self):
        self.curr_time = time.time()
        self.timer = str(int(self.curr_time) - int(self.start_time))



class Quotes:
    def __init__(self):
        import json

        with open('SMART-MiRRoR\\Random\\quotes.json') as f:
            self.quote_data = json.load(f)

        self.quote = ""
        self.author = ""

    def Reload_Quotes(self):
        with open('SMART-MiRRoR\\Random\\quotes.json') as f:
            self.quote_data = json.load(f)
            
    def New_Quote(self):
        import random

        random_quote = random.choice(self.quote_data)
        self.quote = random_quote['quoteText']
        self.author = random_quote['quoteAuthor']



class News:
    def __init__(self):
        self.bbc_news_title = ""
        self.bbc_news_description = ""
        self.ny_times_title = ""
        self.ny_times_descriptiom = ""
        self.scientist_title = ""
        self.scientist_description = ""
        self.engadget_title = ""
        self.engadget_description = ""
        self.fft_title = ""
        self.fft_description = ""



    def Fetch_News(self):
        from newsapi import NewsApiClient

        newsapi = NewsApiClient(api_key='<API KEY>')

        bbc_news = newsapi.get_top_headlines(sources='bbc-news')
        self.bbc_news_title = bbc_news['articles'][0]['title']
        self.bbc_news_description = newsapi.get_top_headlines(sources='bbc-news')['articles'][0]['description']

        ny_times = newsapi.get_top_headlines(sources='the-new-york-times')
        self.ny_times_title = ny_times['articles'][0]['title']
        self.ny_times_descriptiom = ny_times['articles'][0]['description']

        scientist = newsapi.get_top_headlines(sources='new-scientist')
        self.scientist_title = scientist['articles'][0]['title']
        self.scientist_description = scientist['articles'][0]['description']

        engadget = newsapi.get_top_headlines(sources='engadget')
        self.engadget_title = engadget['articles'][0]['title']
        self.engadget_description = engadget['articles'][0]['description']

        fft = newsapi.get_top_headlines(sources='fft')
        self.fft_title = fft['articles'][0]['title']
        self.fft_description = fft['articles'][0]['description']



class Personal_Schedule:
    def __init__(self):
        self.curr_date = ""
        

    def check_calendar(self):
        import pickle
        import os.path
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import datetime

        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='Chidi Ewenike', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])    



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
    def __init__(self,playlist):
        self.music_path = ""

    def recheck_music_list(self):
        return os.listdir(self.music_path)   

    def play_playlist(self,playlist):
        self.music_choice = self.music_path + "\\" + playlist

    def display_music_choice(self):
        playlist = self.recheck_music_list()
        # display to UI
