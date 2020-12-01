*** This system has been designed to work with UK data (covid, weather and news data) ***

# Introduction:
(This is from the CA3 specification "./specification/CA3-2021.pdf")
Since the outbreak of COVID-19 the day-to-day routine for many people has been disrupted and the instability of our environment
means we have to be adaptable to current events. Keeping up-todate with the rapidly changing local and national infection rates and
regularly updated government guidelines has become a daily challenge for many as well as keeping track of the weather and plans
that are often changed at short notice.
   
Smart systems are automated systems that adapt to input data streams. Alarm clocks are an everyday item that we use to schedule our
lives. The scope for a smart alarm clock that can access information about the COVID infection rate and provide scheduled updates
about the the weather and the news and engage with us through a lightweight interface has the potential to be very useful.

(This isn't)
So this system has been provideded to meet those observations. It is a lightweight alarm clock with only 4 options on the page plus
the ability to delete alarms once they have been set. This system gives textual updates about the coivid infection numbers for the
local area (defined in the config file), weather (also for the local area defined in the config file) and news. Then when an alarm
is set there is the option for a message plus weather and/or top news story update. When the alarm goes off the time will be said
(through the pyttsx3 text to speech module) along with a covid infection number update for the local area, and then if the user
selects it, an update on the weather and news.

# Prerequisites:
The python version used to develop this, is python version 3.7, but it has been tested to work on 3.6 and above (3.7,3.8,3.9).
You will need a version of python installed (if you don't already) to run the code. 'https://www.python.org/downloads/'
You will also need an internet connection, and the modules listed below. There is a 'pip install' command to run that installs them
all at once.

# Installation:
The list of modules that you will need to 'pip install':  
    1. flask  
    2. multiexit  
    3. logger  
    4. schedule  
    5. pyttsx3  
    6. pylint  
    7. requests  
    8. pytest  
As a one command line: "pip install flask multiexit logger schedule pyttsx3 pylint requests pytest"

# Getting started:
Navigate to the 'code' folder
## Config file:
This should be a file located in the json_files folder in the code folder (./code/json_files)  
The file should be set out like this:  
{  
"config": [  
{  
    "weatherkey": "your_weather_api_key"  
    },  
{  
    "newskey": "your_news_api_key"  
    },  
{  
    "log_file": "./file/log_file"  
    },  
{  
    "weather_city_or_town": "your_city_or_town"  
    },  
{  
    "Area_location": "your_region_Eg.'South West"  
    }  
    ]  
}  
-For the weather key you will need to sign up for the free weather api and request a key, http://api.openweathermap.org  
-For the news key you will need to sign up for the free news api and request a key, https://newsapi.org  
-For the log file, enter the location you want the log file to be stored. I suggest a place so you can easily find and look at
it, if anything goes wrong. Also do NOT add an extension to the end of the file (as shown in the example above).  
-For the weather city or town, just enter the city or town that you live in the uk, make sure it starts with a capital letter.  
-For the area location, enter the region or city or council area that you live in the uk, eg. South West or Exeter, and make sure that the starts of the words are capitalised.  
-The regions are:  
    1. Scotland  
    2. Northern Ireland  
    3. Wales  
    4. North East  
    5. North West  
    6. Yorkshire and the Humber  
    7. West Midlands  
    8. East Midlands  
    9. South West  
    10. South East  
    11. East of England  
    12. London  
To be more specific you can put your cicty or council area that you live in, enter your postcode into this BBC site to confirm your area name: https://www.bbc.co.uk/news/uk-51768274
## alarms file:
This should be a file located in the json_files folder in the code folder (./code/json_files)  
The file should be set out like this:  
{  
    "alarms": []  
}  
## notifications file:
This should be a file located in the json_files folder in the code folder (./code/json_files)  
The file should be set out like this:  
{  
    "notifications": []  
}  
## seen file:
This should be a file located in the json_files folder in the code folder (./code/json_files)  
The file should be set out like this:  
{  
    "notifications": []  
}  

## The Log file:
It is formatted such that at the start of each line will be the time that that event was logged and after will be what is being
logged  
Eg: "2020-11-25 23:46:43,716 articles retrieved -- <Response [200]>" or for the html logs: "2020-11-25 23:46:43,803 127.0.0.1
[25/Nov/2020 23:46:43] [37mGET /index HTTP/1.1[0m 200]"  
At the end of the html log (and also the response from the api log) there is the code that the site is giving back.  
Here are a list of codes that can be sent back and what they mean: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
The most common ones: '200 OK', '201 Created', '204 No Content', '304 Not Modified', '400 Bad Request', '401 Unauthorized',
'403 Forbidden', '404 Not Found', '409 Conflict' and '500 Internal Server Error'
## Running the code:
To start the program after all of the above has been run the 'main.py' file with python the the command line (or in an IDE),
once this has been done. Navigate to the site that is returned it should look like this ('http://127.0.0.1:5000/')
## To note:
-You cannot set two alarms for the same time and date.  
-You cannot set alarms for in the past.  
-You can delete the notifications but the file containing delete notifications is deleted every hour. And the notifications are updated every 15 minutes  

# Testing:
## TBA

# Developer Documentation:  
See "/docs/build/html/index.html" for more information about what modules and functions do.  

# Details:
© 2020 Hugo Hewitt (hh538@exeter.ac.uk)  
html template: Matt Collison  
https://github.com/hugohewitt123/Programming-ECM1400-Coursework-3
