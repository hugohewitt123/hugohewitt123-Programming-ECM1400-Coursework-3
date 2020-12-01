'''This is the main module for the alarm program, it is
an alarm system that gets the latest news, weather and covid
updates and displays this on a webpage for the user
it also allows the user to set alarms and choose whether they
want the alarm to also say the latest news story and weather'''
import atexit
from flask import Flask, render_template, request, redirect
from news import news
from weather import weathers
from alarm import add_alarm, remove_alarm, refresh
from covid import get_covid
from time_conversions import log
from organise_dictionaries import org_func, remove_notification

app = Flask(__name__)

@app.route('/')
def rootindex():
    '''This adds, started, to the logfile and redirects the
    user to the index page'''
    log('-------STARTED-------')
    return redirect("/index")

@app.route('/index')
def index():
    '''This module is what connects the modules and then
    shows this on the webpapge'''
    #getting the information from the form on the webpage\
    #when the user submits their alarm the alarm
    alarm = str(request.args.get("alarm"))
    #the label for the alarm
    name = request.args.get("two")
    #whether they want a news update in the alarm or not
    inclnews = request.args.get("news")
    #whether they want a weather update in the alarm or not
    inclweather = request.args.get("weather")
    #if the user decides to delete an alarm
    delete = request.args.get("alarm_item")
    #if the user decides to delete a notification
    rem_notif = request.args.get("notif")
    #passing the delete info to the remove function
    if delete:
        remove_alarm(delete, True)
    if rem_notif:
        remove_notification(rem_notif)
    #using the covid function to get the latest stats from the api
    covid = get_covid()
    #using the news function to get the latest news from the news api
    articles = news()
    #using the weather function to get the latest weather from the weather api
    weather = weathers()
    #setting a blank variable to be used in the alarm function calls
    temp = ''
    #using if statements to decide what to call the alarm with dependin on user inputs
    if inclnews == 'news' and inclweather == 'weather':
        pick_news = True
        pick_weather = True
        #calling the add alarm function to add the details the user inputted to the json file
        alarmj = add_alarm(alarm, name, weather, articles, covid, pick_news, pick_weather)
    elif inclweather:
        pick_news = False
        pick_weather = True
        alarmj = add_alarm(alarm, name, weather, temp, covid, pick_news, pick_weather)
    elif inclnews:
        pick_news = True
        pick_weather = False
        alarmj = add_alarm(alarm, name, temp, articles, covid, pick_news, pick_weather)
    else:
        pick_news = False
        pick_weather = False
        alarmj = add_alarm(alarm, name, temp, temp, covid, pick_news, pick_weather)
    if name is None:
        #checking and refreshing the alarms to the latest weather, news and covid info
        alarmj = refresh(covid,articles,weather)
    #putting all the updates (covid,news,weather) into one dictionary\
    #to be passed to the html as notifications
    organised = org_func(covid, weather, articles)
    #rendering all this informaion to the html template as a website
    return render_template('template.html', notifications=organised, alarms=alarmj,\
        image='icons8-clock-64.png')

@atexit.register
def logg():
    '''This logs when the python service is closed'''
    log('-------FINISHED-------')

#initializing the program
if __name__ == '__main__':
    app.run()
