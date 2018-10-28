import time
import requests
import json
import winsound

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
        self.weather_url = "https://api.darksky.net/forecast/<<API_KEY>>/35.2827524,-120.6596156"
        self.current_weather = ""
        self.current_temp = ""
        self.forecast_summary = ""
        self.temp_high = ""
        self.temp_lows = ""   

    def Obtain_Weather(self):
        import requests
        import json

        weather_respone = requests.get(self.weather_url)
        weather_data = json.loads(weather_respone.content)

        self.current_weather = weather_data["hourly"]["data"][0]["summary"]
        self.current_temp = str(int(weather_data["hourly"]["data"][0]["temperature"]))
        self.forecast_summary = weather_data["daily"]["data"][0]["summary"]
        self.temp_high = str(int(weather_data["daily"]["data"][0]["temperatureHigh"]))
        self.temp_lows = str(int(weather_data["daily"]["data"][0]["temperatureLow"]))



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

        newsapi = NewsApiClient(api_key='948b7b39ae1c456cbff5cff29cb3b5b6')

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
        pass

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
        pass
