import time
import requests
import json

class Alarm:
    def __init__(self):
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
    
    def calc_timer(self):
        self.curr_time = time.time()
        self.timer = str(int(self.curr_time) - int(self.start_time))

class Quotes:
    def __init__(self):
        import json

        with open('SMART-MiRRoR\Random\quotes.json') as f:
            self.quote_data = json.load(f)

        self.quote = ""
        self.author = ""

    def new_quote(self):
        import random

        random_quote = random.choice(self.quote_data)
        self.quote = random_quote['quoteText']
        self.author = random_quote['quoteAuthor']

class News:
    def __init__(self):
        pass

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

