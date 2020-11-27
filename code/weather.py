'''This module is called from the main function to get the
json file from the weather api website'''
import json
import requests
from time_conversions import log

def weathers():
    '''This function does the api call to the website and it gets
    the api key from the config json file, then it returns the json file
    from the api call'''
    #setting the base url for the api call
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    #getting the users api key and their location (city name or town) from the config json file
    with open("./json_files/config.json", "r") as jfile:
        key = json.load(jfile)
        key = key["config"]
        api_key = key[0]['weatherkey']
        city_name = key[3]['weather_city_or_town']
    #adding this information to the base url so the api call can be made
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    try:
        #making an api call with the requests module and the complete url
        response = requests.get(complete_url)
        weather_json = response.json()
        #logging that the weather has been retrieved
        if weather_json['cod'] == 200:
            log("weather retrieved -- " + str(requests.get(complete_url)))
        else:
            log("error getting the api data")
            log(requests.get(complete_url))
            log(weather_json)
        #returning the weather data
        return weather_json
    except:
        #logging and returning that the api calling has errored
        log("FAILED to get Weather data from api" + str(requests.get(complete_url)))
        return [{'cod':'404','message':"FAILED couldn't get weather data"}]
