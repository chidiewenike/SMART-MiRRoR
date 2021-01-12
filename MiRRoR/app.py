# Python packages
import flask
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import json
import os
import random

# Custom Packages
import Small_Classes

app = flask.Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True

with open('quotes.json') as f:
    data = json.load(f)

@app.route('/', methods=['POST', 'GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def home():

    query = request.get_json()
    print( query )

    output = process_query( query[ "Data" ] )

    print( "Sending: ", output )

    return jsonify( output )

def process_query( query:str ) -> dict:
    '''
    :param query: String of the client query
    :return response: Dict of the response date for the client

    response = {
                    "quote" : "Dale dale dale",
                    "author": "Ollie Lafc"
                }
    '''

    response = {
                    "result"    : "ERROR"
                }

    if ( query == "quote" ):
        response = get_quote()

    elif ( query == "emails" ):
        response = get_email()

    elif ( query == "word" ):
        response = get_word()

    elif ( 
            ( query == "current_weather" ) or
            ( query == "forecast_weather" )
         ):
        response = get_weather( query )

    elif ( query == "football" ):
        response = get_football()

    elif ( query == "news" ):
        response = get_news()

    elif ( query == "tasks" ):
        response = get_tasks()

    elif ( query == "schedule" ):
        response = get_schedule()

    return response

def get_schedule() -> dict:
    '''
    Makes the API request to Google Calendar and obtains a dict of events.

    :return task_dict: Dict with the events data

           sched_dict = {
                            "event_1" : "01/01 | 12:00 | Event | Some Place",
                            ...
                        }
    '''
    schedule = Small_Classes.Schedule()

    sched_dict = schedule.obtain_calendar()

    print( sched_dict )

    return sched_dict

def get_tasks() -> dict:
    '''
    Makes the API request to Google Tasks and obtains a dict of tasks.

    :return task_dict: Dict with the tasks data

    task_data = {
                        "task_1" : "Do something first",
                        "task_2" : "Do something afterwards",
                        ....
                    }
    '''
    tasks = Small_Classes.Tasks()

    task_dict = tasks.obtain_tasks()

    print( task_dict )

    return task_dict

def get_news() -> dict:
    '''
    Makes the API request to newsapi and gets the news data.

    :return news_dict: 	Dict of news data per source

    news_dict = {
                    "reuters_1" : "Things happened\nAnd they happened",
                    "reuters_2" : "Things happened\nAnd they happened",
                    ...
                }
    '''

    # news = Small_Classes.News()

    # news_dict = news.obtain_news()

    # print( news_dict )

    with open('news.json', "r") as f:
        news_dict = json.load( f )

    return news_dict

def get_football() -> dict:
    '''
    Makes the API request to API-Football and gets the fixture data.

    :return football_dict: 	Dict of fixture data per team

    football_dict = {
                        "Everton_Home"      :   "Wolves",
                        "Everton_Away"      :   "Everton",
                        "Everton_Date"      :   "01/13/2020",
                        "Everton_Time"      :   "07:00",
                        ...
                    }
    '''

    # football = Small_Classes.Football_Fixtures()

    # football_dict = football.obtain_matches()

    # print( football_dict )

    with open('fixtures.json', "r") as f:
        football_dict = json.load( f )

    return football_dict

def get_quote() -> dict:
    '''
    Loads the quote JSON and returns a random quote.

    :return quote: Dict of a quote and its author
    '''

    with open('quotes.json') as f:
        quotes = json.load(f)

    quote = random.choice( quotes )
    
    return quote

def get_word() -> dict:
    '''
    Makes the API request to WotD and gets the word, definition, and PoS.

    :return word_dict: Dict of word of the day meta data

    word_dict = {
                    "word"          : "querimony",
                    "definition"    : "A complaint; a complaining.",
                    "type"          : "noun"
                 }
    '''
    
    word = Small_Classes.Word_of_the_Day()

    word_dict = word.new_word()

    print(word_dict)

    return word_dict

def get_weather( data_req:str ) -> dict:
    '''
    Makes the API request to DarkSky API and obtains a list of weather data.

    :param  data_req:       Data to be requested
    :return weather_dict:   Dict of weather data

    weather_dict = {
                        "day_1_weather"     : "sunny",
                        "day_1_high"        : "79",
                        "day_1_low"         : "52",
                        "day_1_day"         : "Today"

                        ...
                    }    
    '''

    weather = Small_Classes.Weather()

    if ( data_req == "current_weather" ):
        weather_dict = weather.obtain_current_weather()

    else:
        weather_dict = weather.obtain_five_day_forecast()

    return weather_dict

def get_email() -> dict:
    '''
    Makes the API request to Gmail and obtains a list of email dicts.

    :return email_data: Dict with the list of email dicts

    email_dict = {
                    "subject" : "Cal Poly Newsletter",
                    "from"    : "Cal Poly"
                 }
    '''
    email = Small_Classes.Email()

    email_dict = email.check_email()

    print(email_dict)

    return email_dict

if __name__ == '__main__':
    app.run( threaded=True, port=5000 ) 