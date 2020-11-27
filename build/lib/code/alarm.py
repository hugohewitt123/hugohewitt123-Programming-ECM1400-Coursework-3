'''This is a module that organises the alarms,
deleting them, adding them, scheduling them,
refreshing them and saying them, it depends on
the function that's called'''
import time
import json
import sched
import pyttsx3
from time_conversions import log, current_time_hhmm, hhmm_to_seconds, current_date
from news import news
from weather import weathers
from covid import get_covid

lst=[]
#setting the scheduler information to s
s = sched.scheduler(time.time, time.sleep)

def write_json(data, alarm):
    '''This function opens the alarm json file
    and then adds the date passed to the function
    to the file'''
    with open('./json_files/alarms.json','w') as jfile:
        json.dump(data, jfile, indent=4)
    log("alarm for " + alarm + " has been added")

def print_job_name(alarm, name, weather, article, covid):
    '''This function takes in input strings and then says them
    with pyttsx3'''
    #initiating the pyttsx3
    engine = pyttsx3.init()
    alarm1 = alarm[11:]
    #adding the strings that have been passed to the function\
    #to the say engine
    engine.say(alarm1)
    engine.say(name)
    engine.say(weather)
    engine.say(article)
    engine.say(covid)
    try:
        #saying the strings that are in the say engine
        engine.runAndWait()
        #logging that the alam has been said
        log("alarm for " + alarm + " has been said")
        ##removing the alarm as it has happened
        remove_alarm(alarm)
    except:
        log("FAILED speech run failed due to another item in the scheduler")

def add_alarm(alarm,name,weather,article,covid,pick_news,pick_weather):
    '''This function adds the alarms inputed to the function to
    the json file of alarms and or adds it to the scheduler
    depends on conditions'''
    #running the scheduler
    s.run(blocking=False)
    #setting alarm1 to be the time part of the alarm title
    alarm1 = alarm[11:]
    if alarm1:
        #convert alarm_time to a delay
        current_time = current_time_hhmm()
        #working out the delay by subtracting the current time (in seconds)\
        #from the time on the alarm (in seconds)
        delay = hhmm_to_seconds(alarm1) - hhmm_to_seconds(current_time)
        #setting a new name variable to append to  what is in the input\
        #and still keep the input var
        new_name = name
        #The conditions on whether to manipulate the weather,news & covid\
        #depending on whether they were inputted
        if weather != '' and weather["cod"] == 200:
            #setting weath to the main attributes of the weather input
            weath = weather["main"]
            #getting the tempurature
            current_temp = weath["temp"]
            #getting the pressure
            current_press = weath["pressure"]
            #getting the humidity
            current_humid = weath["humidity"]
            #setting weath to the weather attribute of the weather input
            weath = weather["weather"]
            #getting the description from the weather input (from weath)
            weather_desc = weath[0]["description"]
            #concatonating all the variables gathered on weather into one string with\
            #more descriptions of them
            weather = "Weather update: the temperature outside is "+str(int(current_temp - 273.15))\
                + "degrees centigrade; the atmospheric pressure is "\
                    + str(current_press) + "hectopascals; the humidity is " + str(current_humid) +\
                        "percent; and it is " + str(weather_desc)
            #adding this to the newname variable
            new_name = str(new_name) + ".  '''''''' " + str(weather)
        #inputting to the alarm that there is an error if false weather data is added to an alarm
        elif weather != '' and weather["cod"] != 200:
            wdic = {'title': weather["cod"], 'content': weather['message']}
            new_name = str(new_name) + ".  '''''''' " + str(wdic)
        if article != '':
            #getting the title from the news input
            article = article[0]['title']
            article = str('The top news story is: ') + str(article)
            #adding this information plus a description to the newname variable
            new_name = str(new_name) + ". '''''''' " + str(article)
        if covid != '':
            covid = 'The local coronavirus infection rates are: ' + str(covid)
            #adding the information on covid to the newname variable
            new_name = str(new_name) + ".  ''''''' " + str(covid)
        #setting the details abotu the news alarm from the inputs
        new_alarm = {"title": alarm, "content": new_name, "pick_news": pick_news,\
            "pick_weather": pick_weather}
        #opening the alarm json file and getting all the alarms from it
        with open('./json_files/alarms.json') as jfile:
            data = json.load(jfile)
            temp = data['alarms']
        in_alarms = False
        if len(temp) != 0:
            #looping though the alarms json if it isnt empty
            for i in temp:
                if i['title'] == alarm:
                    #if the alarm exists that is being added then in alarms is true if not its false
                    in_alarms = True
                    break
        #appending the json file if that alarm doesnt exist
        if not in_alarms:
            # appending data to alarms
            temp.append(new_alarm)
            #calling the write function to add the new alarms to the json file
            write_json(data, alarm)
        else:
            log('cannot make alarm as there is already an alarm for this time')
            return end()
        #saying the event if it is set for the time now\
        #and if the date on the alarm is the same as todays date
        if alarm[:10] == current_date() and delay == 0:
            print_job_name(alarm,name,weather,article,covid)
        #Not adding the alarm if it is set in the past
        elif alarm[:10] == current_date() and delay < 0:
            log("alarm " + alarm +" is set in the past")
            remove_alarm(alarm, True)
        #only adding an item to the scheduler if it has less than 60 seconds\
        #and if the date on the alarm is the same as todays date
        elif alarm[:10] == current_date() and 0 < delay < 61:
            lst.append(s.enter(int(delay), 1, print_job_name, [alarm,name,weather,article,covid,]))
            #logging that the alarm has been added to the scheduler
            log("alarm "+ alarm +" added to the scheduler")
        return end()
    #returning end if there is nothing to do
    return end()

def refresh(covid,articles,weather):
    '''This function will update the alarms with the latest covid,weather&news'''
    #getting all the alarms from the alarms json file
    with open("./json_files/alarms.json", "r") as jfile:
        alarm = json.load(jfile)
        alarmj = alarm["alarms"]
    #the length of the alarms (how many alarms ar set)
    length = len(alarmj)
    #a blank variable to use in the alarms call
    temp = ''
    #looping through each item in the alarm
    for i in range(length):
        #setting variables to tell the add alarm function if\
        #there is a news and/or weather item in this alarm
        incl_news = alarmj[i]['pick_news']
        incl_weather = alarmj[i]['pick_weather']
        #setting the alarm title from the alarm in the json file
        alarm = alarmj[i]['title']
        content = alarmj[i]['content']
        #setting content to a string
        content = str(content)
        #the length of content
        content_length = len(content)
        #looping through the content to get the message that\
        #the user entered
        for j in range(content_length):
            if content[j] == "'" and content[j+1] == "'":
                ending = j
                break
        content = content[:(ending-3)]
        #then removing the old alarm so there are no duplicates again
        remove_alarm(alarm, True)
        #logging that the alarm is updated
        log("alarm for " + alarm + " has been updated")
        #adding this to the alarms with the add alarm function\
        #accoding to if the news and weather has been set
        if incl_news and incl_weather:
            #calling the add alarm function to add the updated alarm
            add_alarm(alarm, content, weather, articles, covid, incl_news, incl_weather)
        elif  incl_weather:
            add_alarm(alarm, content, weather, temp, covid, incl_news, incl_weather)
        elif incl_news:
            add_alarm(alarm, content, temp, articles, covid, incl_news, incl_weather)
        else:
            add_alarm(alarm, content, temp, temp, covid, incl_news, incl_weather)

def remove_alarm(title, status=False):
    '''This function opens the json file for the alarms and
    then it loops through the file until the title is the same
    and it removes that alarm'''
    with open('./json_files/alarms.json') as jfile:
        data = json.load(jfile)
        #getting the alarms from the json file
        temp = data['alarms']
        #the number of alarms in the file
        length = len(temp)
        #looping through each alarm in the list
        for i in range(length):
            #then checkign each alarm title agaist the input title,
            #and if they are the same this will remove it
            if temp[i]["title"] == title:
                temp.pop(i)
                log("alarm for " + title + " has been removed")
                break
    #re-wrtiting the updated alarms to the json file
    with open('./json_files/alarms.json','w') as jfile:
        json.dump(data, jfile, indent=4)
    length = len(lst)
    if status:
        #looping through the scheduler list
        for i in range(length):
            try:
                #canceling the events in the list
                s.cancel(lst[i])
                #logging that this has been done
                log('alarm '+ title +' removed from scheduler')
            except:
                log('alarm'+ title +'could not be removed from the scheduler')
            #removing the item from the list
        lst.clear()
    if not status:
        refresh(get_covid(), news(), weathers())

def end():
    '''This function loads the alarm json file and returns the alarms in it'''
    with open("./json_files/alarms.json", "r") as jfile:
        alarm = json.load(jfile)
        alarmj = alarm["alarms"]
    return alarmj
