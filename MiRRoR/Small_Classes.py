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

json_dir = os.getcwd()
json_path = os.path.join( json_dir, "api_keys.json" )
misc_path = os.path.join( json_dir, "misc_keys.json" )

with open( json_path ) as f:
    api_keys = json.load( f )

with open ( misc_path ) as f:
    misc_keys = json.load( f )

#TODO: Format alarm code, pull alarm data from Firebase, and run alarm
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

#TODO: Train facial detection model, facial recognition model, and run
#      inference on camera data
class Facial_Recognition:

    def __init__(self):
        pass

#TODO: Utilize GCP TTS, obtain tts audio, and output audio
class Text_To_Speech:
    def __init__(self):
        pass

#TODO: Utilize Deepspeech STT, get transcription, and run command
class Speech_To_Text:
    def __init__(self):
        pass

#TODO: Format music code and output audio
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
    
class Email:
    def __init__(self):

        self.MAX_RESULTS = 30
        self.creds = None

        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        
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
                    json_path, SCOPES)
                self.creds = flow.run_local_server()
            
            # Save the credentials for the next run
            with open(json_dir + 'token_email.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def check_email( self ):
        '''
        Calls the Gmail API and extracts up to self.MAX_RESULTS unread emails.

        :returns response_data: Dict of [str : str] with email number as key
                                and email subject and sender as value

        response_data = {
                            "_0" : "Cal Poly Newsletter <calpoly@calpoly.edu>"
                            ...
                        }
        '''
        
        messages = []
        response_data = {}

        try:
            subject = ""
            from_val = ""

            service = build('gmail', 'v1', credentials=self.creds)
            
            response = service.users().messages()
            response = response.list(
                                        userId='me',
                                        labelIds='UNREAD',
                                        maxResults=self.MAX_RESULTS).execute()
                                        
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages()
                response = response.list(userId='me',
                                        labelIds='UNREAD',
                                        pageToken=page_token).execute()

            for i in range( len( messages ) ):
                curr_msg = service.users().messages()
                curr_msg = curr_msg.get(
                                            userId='me',
                                            id=messages[i]['id']).execute()

                for vals in curr_msg['payload']['headers']:
                    if vals['name'] == 'Subject':
                        subject = vals['value']
                    elif vals['name'] == 'From':
                        from_val = vals['value']

                response_data[ "_" + str( i ) ] = "%s. %s\n%s\n\n" %\
                                                 (str(i + 1), subject, from_val)
                                                                                   
        except:
            print( "Error with email request")
            pass

        return response_data
    
class Word_of_the_Day:

    def __init__(self):

        self.api_call = "https://api.wordnik.com/"\
                        "v4/words.json/wordOfTheDay"\
                        "?api_key=" + misc_keys["word"]
        
    def new_word(self):
        '''
        Makes the API call to Wordnik and obtains the word of the day to be
        returned to the caller.

        :return response_data: Dict of the WotD data

        response_data = {
                            "word" : "puerile",
                            "definition" : "childishly silly and trivial",
                            "type" : "adjective"
                        }        
        '''

        word_response = requests.get( self.api_call )
        try:
            word_data = json.loads( word_response.content.decode( 'utf-8' ) ) 
            print( "Obtained word of the day data: %s" % word_data )
            word = word_data["word"]
            definition = word_data["definitions"][0]["text"]
            type = word_data["definitions"][0]["partOfSpeech"]

            response_data = {
                                "word" : word,
                                "definition" : definition,
                                "type" : type
                            }

        except:
            print("Error getting WotD response")
            response_data = { "result" : "ERROR" }


        return response_data

class Weather:
    def __init__(self):

        loc_coord = "/35.28552,-120.6625"
        self.weather_url = "https://api.darksky.net/forecast/"\
                            + misc_keys["weather"] + loc_coord

    def obtain_current_weather( self ):
        '''
        Makes the Darksky API call to obtain the weather data

        :param self:            Current Weather object
        :return response_data:  Dict of current weather data

        response_data = {
                            "weather"       : "sunny",
                            "temperature"   : "79"
                        }

        '''

        import requests
        import json

        try:
            weather_response = requests.get( self.weather_url )

            decoded_data = weather_response.content.decode( "utf-8" )
            weather_data = json.loads( decoded_data )

            curr_temp = weather_data["hourly"]["data"][0]["temperature"]
            curr_weather = weather_data["hourly"]["data"][0]["icon"]

            curr_temp = str( int( curr_temp ) )
            curr_weather = str( curr_weather )

            response_data = {
                                "weather"       : curr_weather,
                                "temperature"   : curr_temp
                            }

        except:
            print("Error obtaining current weather data")
            response_data = { "result" : "ERROR" }

        return response_data

    def obtain_five_day_forecast(self):
        '''
        Makes the Darksky API call to obtain the weather data

        :param self:            Current Weather object
        :return response_data:  Dict of current weather data

        response_data = {
                            "day_1_weather"     : "sunny",
                            "day_1_high"        : "79",
                            "day_1_low"         : "52",
                            "day_1_day"         : "Today"

                            "day_2_weather"     : "sunny",
                            "day_2_high"        : "79",
                            "day_2_low"         : "52",
                            "day_2_day"         : "Tue"

                            "day_3_weather"     : "sunny",
                            "day_3_high"        : "79",
                            "day_3_low"         : "52",
                            "day_3_day"         : "Wed"

                            "day_4_weather"     : "sunny",
                            "day_4_high"        : "79",
                            "day_4_low"         : "52",
                            "day_4_day"         : "Thur"

                            "day_5_weather"     : "sunny",
                            "day_5_high"        : "79",
                            "day_5_low"         : "52"
                            "day_5_day"         : "Fri"
                        }

        '''

        import requests
        import json

        response_data = {}
        date_delta = datetime.datetime.today()
        
        try:
            for i in range(0,5):
                
                url_date = date_delta.strftime( "%Y-%m-%d" )
                url_date = url_date + "T12:00:00"

                weather_response = requests.get(self.weather_url + 
                                                "," + 
                                                url_date)

                decoded_data = weather_response.content.decode( "utf-8" ) 
                weather_data = json.loads( decoded_data )

                temp_high = weather_data["daily"]["data"][0]["temperatureHigh"]
                temp_low = weather_data["daily"]["data"][0]["temperatureLow"]
                weather = weather_data["daily"]["data"][0]["icon"]

                temp_high = str( int( temp_high ) )
                temp_low = str( int( temp_low ) )
                weather = str( weather )

                if ( i == 0 ):
                    day = "Today"

                else:    
                    day = date_delta.strftime( "%a" )

                response_data[ "day_%d_high" % ( i + 1 ) ] = temp_high 
                response_data[ "day_%d_low" % ( i + 1 ) ] = temp_low
                response_data[ "day_%d_weather" % ( i + 1 ) ] = weather
                response_data[ "day_%d_day" % ( i + 1 ) ] = day

                date_delta += datetime.timedelta( days=1 )

        except:
            print( "Error obtaining the five day weather forecast" )
            response_data = { "result" : "ERROR" }
        
        return response_data

class Football_Fixtures:
    def __init__( self ):
        self.base_url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/"
        self.end_url = "/next/1"

        self.querystring = {"timezone":"America/Los_Angeles"}

        self.headers = {
            'x-rapidapi-key': misc_keys["football"],
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
            }

        self.team_map = {
                            "Everton"           : "45",
                            "Los Angeles FC"    : "1616",
                            "Nigeria"           : "19",
                            "Finland"           : "1099",
                            "USA"               : "2384"  
                        }

    def obtain_matches( self ) -> dict:
        '''
        Makes an API call to API-Football and obtain the next match.
        :param arg: 	arg description
        :return response_data: 	Dict of football match data

        response_data = {
                            "Everton_Home"      :   "Wolves",
                            "Everton_Away"      :   "Everton",
                            "Everton_Date"      :   "01/13/2020",
                            "Everton_Time"      :   "07:00",
                            ...
                        }
        '''
        response_data = {}

        try:
            for team in self.team_map.keys():
                url = self.base_url + self.team_map[team] + self.end_url
                response = requests.request(
                                                "GET", 
                                                url, 
                                                headers=self.headers, 
                                                params=self.querystring
                                            )

                decoded_data = response.json()
                fixture_data = decoded_data["api"]["fixtures"]
                
                if fixture_data != []:
                    response_data = self.process_match_data(
                                                                team,
                                                                response_data,
                                                                fixture_data[ 0 ] )

                else:
                    response_data = self.process_match_data(
                                                                team,
                                                                response_data,
                                                                None )

        except:
            print("Error obtaining match data")
            response_data = { "result" : "ERROR" }

        return response_data

    def process_match_data( 
                            self,
                            team:str,
                            response_data: dict,
                            fixture_data:dict ) -> dict:
        '''
        Processes the fixture data and loads the response_data
        :param team:            String of the team
        :param response_data: 	Dict data to be returned to the user
        :param fixture_data: 	Dict of fixture data; None if match DNE
        :return response_data: 	Dict data to be returned to the user
        '''
        team_temp = team.replace(" ", "_")

        response_data["%s_Home" % team_temp] = team
        response_data["%s_Away" % team_temp] = "Default"
        response_data["%s_Date" % team_temp] = "N/A"
        response_data["%s_Time" % team_temp] = "N/A"

        if ( fixture_data != None ):
            home = fixture_data["homeTeam"]["team_name"]
            away = fixture_data["awayTeam"]["team_name"]

            date_time = fixture_data["event_date"].split("T")

            date = date_time[0].split("-")
            date = "%s.%s" % ( date[1], date[2] )

            time = date_time[1].split("-")[0]
            time = time.split(":")
            time = "%s:%s" % ( time[0], time[1] )

            response_data["%s_Home" % team_temp] = home
            response_data["%s_Away" % team_temp] = away
            response_data["%s_Date" % team_temp] = date
            response_data["%s_Time" % team_temp] = time

        return response_data

class News:
    def __init__(self):
        self.max_articles = 5
        self.count = 0
        self.sources = [
                            'reuters',
                            'associated-press',
                            'new-scientist',
                            'engadget',
                            'hacker-news',
                            'four-four-two'
                        ]

    def obtain_news(self):
        '''
        Requests the API data and returns the news data.

        :return response_data: Dict of news data

        response_data = {
                            "reuters_1" : "Things happened\nAnd they happened",
                            "reuters_2" : "Things happened\nAnd they happened",
                            ...
                        }
        '''

        from newsapi import NewsApiClient

        response_data = {}

        try:
            newsapi = NewsApiClient( api_key=misc_keys["news"] )

            for source in self.sources:
                articles = newsapi.get_top_headlines( sources=source )
                response_data = self.process_news( 
                                                    source,
                                                    articles,
                                                    response_data )

        except:
            print("Error obtaining the news data")
            response_data = { "result" : "ERROR" }

        return response_data

    def process_news( 
                        self, 
                        source:str,
                        api_data:dict, 
                        response_data:dict ) -> dict:
        '''
        Takes the API JSON data and adds it to the response_data

        :param source:          String of the news source
        :param api_data: 	    Dict of data from the API call
        :param response_data: 	Dict of data to be returned to the caller
        :return response_data: 	Dict of data to be returned to the caller
        '''
        num_articles = len( api_data['articles'] )
        
        for i in range( min( num_articles, self.max_articles ) ):
            title = api_data['articles'][i]['title'] 
            description = api_data['articles'][i]['description']
            source = self.capitalize_str( source )
            response_data[ "article_%d" % ( self.count ) ] = "%s - %s\n%s" % (
                                                                                source,                                                                                 
                                                                                title,
                                                                                description )
            self.count += 1

        return response_data

    def capitalize_str( 
                        self,
                        input_str:str ) -> str:
        '''
        Takes a string and capitalizes words in the str

        :param input_str:   String to be capitalized
        :return mod_str: 	String that is capitalized
        '''

        mod_str = ""
        split_str = input_str.split("-")

        for string in split_str:
            string = string[ 0 ].upper() + string[ 1: ]
            mod_str += ( string + " " )
                
        return mod_str
    
class Tasks:
    def __init__(self):

        self.creds = None
        self.task_id = 'MTIyODQxNjE5ODU0MTUyMzc1MjM6MDow'
        self.MAX_RESULTS = 20

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

        if os.path.exists( 'token_task.pickle' ):
            with open( 'token_task.pickle', 'rb' ) as token:
                self.creds = pickle.load( token )

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:

            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh( Request() )

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    json_path, SCOPES )
                self.creds = flow.run_local_server()

            # Save the credentials for the next run
            with open( 'token_task.pickle', 'wb' ) as token:
                pickle.dump( self.creds, token )

    def obtain_tasks( self ) -> dict:
        '''
        Makes an API call to the Google Tasks API and returns task data to the
        caller.

        :return response_data: Dict of task data

        response_data = {
                            "task_1" : "Do something first",
                            "task_2" : "Do something afterwards",
                            ....
                        }

        '''

        response_data = {}
        
        try:
            
            service = build( 'tasks', 'v1', credentials=self.creds )
            tasks = service.tasks().list( tasklist=self.task_id ).execute()

            num_iter = min( self.MAX_RESULTS, len( tasks['items'] ) )

            for i in range( 0, num_iter ):
                position = int( tasks['items'][i]['position'] )
                task_data = tasks['items'][i]['title']

                response_data[ "task_%d" % position ] = task_data

        except:
            print( "Error obtaining the tasks" )
            response_data = { "result" : "ERROR" }

        return response_data

class Schedule:
    def __init__(self):
        self.MAX_RESULTS    = 20
        self.MAX_LOC        = 10
        self.MAX_SUM        = 30

        self.creds = None

        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

        if os.path.exists('token_cal.pickle'):

            with open('token_cal.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:

            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    json_path, SCOPES)
                self.creds = flow.run_local_server()

            with open('token_cal.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def obtain_calendar( self ):
        '''
        Makes the API request to Google Calendars and returns the events data
        to the caller.

        :return response_data: Dict of events data

        response_data = {
                            "event_1" : "01/01 | 12:00 | Event | Some Place",
                            ...
                        }
        '''

        response_data = {}

        try:
            service = build( 'calendar', 'v3', credentials=self.creds )

            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = service.events()
            events_list = events_result.list(
                                                calendarId='primary', 
                                                timeMin=now,
                                                maxResults=self.MAX_RESULTS, 
                                                singleEvents=True,
                                                orderBy='startTime' ).execute()

            events = events_list.get( 'items', [] )

            response_data = self.process_events( events )
    
        except:
            print( "Error obtaining the calendar data" )
            response_data = { "result" : "ERROR" }
    
        return response_data

    def process_events( 
                        self,
                        events:list ) -> dict:
        '''
        Take the Calendar data and extract the relevant data

        :param events:      List of calendar event dicts
        :return event_data: Dict of events data	
        '''
        response_data = {}
        count = 0

        for event in events:
            event_str = ""

            if ( "dateTime" in event[ "start" ] ):
                start_date_time = event[ "start" ][ "dateTime" ]
                
                date_time = start_date_time.split( "T" )
                date = self.extract_date( date_time[ 0 ] )
                time = ( date_time[ 1 ].split( "-" ) )[ 0 ][:-3]

            elif ( "date" in event[ "start" ] ):
                start_date = event[ "start" ][ "date" ]

                time = "All Day"
                date = self.extract_date( start_date )
 
            else:
                time = "N/A"
                date = "N/A"

            if ( "location" in event ):

                temp_location = event[ "location" ]

                if ( "http" in temp_location ):
                    location = "Virtual"

                else:
                    location = temp_location[:self.MAX_LOC]

            else:
                location = "N/A"

            if ( "summary" in event ):
                summary = event[ "summary" ][:self.MAX_SUM]

            else:
                summary = "N/A"

            event_str = "\t\t%s\n%s\t\t|%s\t|%s" % (
                                                        summary,
                                                        time,
                                                        date,
                                                        location
                                                    )

            response_data[ "event_%d" % count ] = event_str

            count += 1

        return response_data

    def extract_date( 
                        self,
                        date:str ) -> str:
        '''
        Takes Google-formatted date and extracts date in "MM-DD" format

        :param date: 	    String of date in the "YYYY-MM-DD" format
        :return norm_date: 	String of date in "MM-DD" format
        '''
        norm_date = ""

        date = date.split("-")
        norm_date = "%s-%s" % ( date[1], date[2] )

        return norm_date

if __name__ == "__main__":
    sched = Personal_Schedule()
    print(sched.obtain_calendar())
