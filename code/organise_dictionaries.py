'''This module organises the dictionaries that are inputed, this is the covid, artices and weateher
then it puts these all in a json file. After this it reads from the file and checks each item
against another json file with the notifications that have been delted, and if it isn't in there
it is added to the list that is returned
The remove notification adds the notification that is removed to the seen file'''
import json
from flask import Markup
from time_conversions import current_time_hhmm, log

def write_json(data):
    '''This function opens the notification json file
    and then adds the data passed to the function
    to the file'''
    with open('./json_files/notifications.json','w') as jfile:
        json.dump(data, jfile, indent=4)
    log("notifications have been added to the json file")

def org_func(covid, weather, articles):
    '''This function takes in the 3 dictionsaries covid, weather & articles
    and then it formats them and returns them in one list'''
    length = len(current_time_hhmm())
    for i in range(length):
        if current_time_hhmm()[i] == ":":
            start = i+1
    #refreshing the seen file so it doesn't contain irrelevent info
    if current_time_hhmm()[start:] == '':
        with open('./json_files/seen.json','w') as jfile:
            json.dump({'notifications':[]}, jfile, indent=4)
    #this wil update the notifications collumn ever 15 mins
    if int(current_time_hhmm()[start:])%15 == 0 or current_time_hhmm()[start:] == '':
        length = len(articles)
        i = 0
        #this will loop through every item (article) in articles
        #if the api call didn't fail
        if articles[0]['title'] != 'FAILED':
            while i < length:
                #adding the url of the website in the article to the content variable as\
                #markup so it can be displayed on the website (with html)
                content=Markup(("<a href='%s'target='_blank'>click_here</a>"%(articles[i]['url'])))
                #then adding this to the content of the spcific article
                articles[i]['content'] = str(articles[i]['description']) + ' ------ ' + content
                i+=1
        #setting the covid input to be added as a dictionary
        dic = {'title': 'Daily local covid infection rates', 'content': str(covid), 'url': ''}
        #adding this dictionary to articles
        articles.insert(0, dic)
        #chekcing if there has been weather data inputted and that there hasn't been an error
        if weather != [] and weather["cod"] == 200:
            #setting mweather to the main attributes of the weather input
            mweather = weather["main"]
            #getting the tempurature
            current_temp = mweather["temp"]
            #getting the pressure
            current_press = mweather["pressure"]
            #getting the humidity
            current_humid = mweather["humidity"]
            #setting mweather to the weather attribute of the weather input
            mweather = weather["weather"]
            #getting the description from the weather input (from mweather)
            weather_desc = mweather[0]["description"]
            #concatonating all the variables gathered on weather into one string with\
            #more descriptions of them
            description = "temp in celsius = " + str(int(current_temp - 273.15)) +\
                "\n; atmospheric pressure in hPa = "+ str(current_press) + "\n; humidity in % = " +\
                    str(current_humid) + "\n; description = " + str(weather_desc)
            #putting this description into a dictionary with the other informaiont about weather
            wdic = {'title': 'Weather in Exeter', 'content': description, 'url': ''}
            #adding this dictionary to articles
            articles.insert(1, wdic)
        #adding to articles that there has been an error with the api call
        elif weather != [] and weather["cod"] != 200:
            wdic = {'title': weather["cod"], 'content': weather['message'], 'url': ''}
            articles.insert(1, wdic)
        #logging that the inputs have been organised into notifications
        log("notifications organised")
        data = {'notifications':[articles]}
        #calling the write function to add the new notifications to the json file
        write_json(data)
    #opening the json file to read from it
    with open('./json_files/notifications.json') as jfile:
        data = json.load(jfile)
        #getting the notifications from the json file
        data = data['notifications'][0]
    log('notifications from json file returned')
    #looping through the json file and adding the urls as links
    length = len(data)
    if data[2]['title'] != 'FAILED':
        for i in range(length):
            if data[i]['url']:
                #adding the url of the website in the article to the content variable as\
                #markup so it can be displayed on the website (with html)
                content=Markup(("<a href='%s'target='_blank'>click_here</a>"%(data[i]['url'])))
                #then adding this to the content of the spcific article
                data[i]['content'] = str(data[i]['description']) + ' ------ ' + content
    notifications = []
    #getting the seen notifications file
    with open('./json_files/seen.json') as jfil:
        seen = json.load(jfil)
        #getting the notificatios from the json file
        seen = seen['notifications']
    for i in data:
        if i not in seen:
            notifications.append(i)
    #returning the notifications in the json file
    return notifications

def remove_notification(title):
    '''This function will remove a notification from the notifications json file'''
    with open('./json_files/notifications.json') as jfile:
        data = json.load(jfile)
        #getting the notificatios from the json file
        temp = data['notifications']
        #the number of notifications in the file
        length = len(temp[0])
    #getting the seen notifications file
    with open('./json_files/seen.json') as jfil:
        seen_data = json.load(jfil)
        #getting the notificatios from the json file
        seen = seen_data['notifications']
    #looping through each notifications in the list
    for i in range(length):
        #then checking each notification title agaist the input title,
        #and if they are the same this will remove it
        if temp[0][i]["title"] == title:
            # appending data to seen notifications file
            seen.append(temp[0][i])
            with open('./json_files/seen.json','w') as jfile:
                json.dump(seen_data, jfile, indent=4)
            log("notifications json file updated")
            log("notification for '" + title + "' has been removed")
            break
