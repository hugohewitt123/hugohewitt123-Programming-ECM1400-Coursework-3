'''This module is called from the main function to get the
json file from the news api website'''
import json
import requests
from time_conversions import current_time_hhmm, log

lst = []

def news():
    '''This function does the api call to the news website and it gets
    the api key from the config json file, then it returns the json file
    from the api call'''
    length = len(current_time_hhmm())
    #looping through the time to find the middle (:)
    for i in range(length):
        if current_time_hhmm()[i] == ":":
            start = i+1
    #only getting the news from the api every 15 mins, or when the function is first called
    if int(current_time_hhmm()[start:])%15==0 or current_time_hhmm()[start:] == '' or len(lst) == 0:
        if len(lst) == 0:
            lst.append('1')
        #setting the base url
        base_url = "https://newsapi.org/v2/top-headlines?"
        #getting the user key from the config json file
        with open("./json_files/config.json", "r") as jfile:
            key = json.load(jfile)
            key = key["config"]
            api_key = key[1]['newskey']
        #adding these (key an country) to the base url to get the url for an api call
        complete_url = base_url + "country=gb&apiKey=" + api_key
        #trying to get the data from the api call, if it can't
        #it will return failed so that the program can continue
        try:
            #making an api call with the requests module and the complete url
            response = requests.get(complete_url)
            articles = response.json()
            #getting the articles from the api call response
            articles = articles["articles"]
            #logging that the articles have been retrieved
            log("articles retrieved -- " + str(requests.get(complete_url)))
            #returning the list of articles
            return articles
        except:
            #logging and returning that the api calling has errored
            log('FAILED to get news data from api' + str(requests.get(complete_url)))
            return [{'title':'FAILED','content':"couldn't get news data"}]
    else:
        #opening the json file to read from it
        with open('./json_files/notifications.json') as jfile:
            data = json.load(jfile)
            #getting the notifications from the json file
            data = data['notifications'][0]
        log('notifications got from the json file')
        return data[2:]
