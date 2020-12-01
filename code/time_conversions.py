'''This is a time module that converts the format hhmmss to seconds
and also holds to log function'''
import time
import json
import logging
from datetime import date

def minutes_to_seconds( minutes: str ) -> int:
    """Converts minutes to seconds"""
    return int(minutes)*60

def hours_to_minutes( hours: str ) -> int:
    """Converts hours to minutes"""
    return int(hours)*60

def hhmm_to_seconds( hhmm: str ) -> int:
    '''converts hours minutes to seconds'''
    if len(hhmm.split(':')) != 2:
        log('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
        minutes_to_seconds(hhmm.split(':')[1])

def current_time_hhmm():
    '''returns the current tim eof the system in the format hhmm'''
    return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)

def current_date():
    '''returns the current date'''
    return str(date.today())

def hhmmss_to_seconds( hhmmss: str ) -> int:
    '''returns the input time (hhmmss) in seconds'''
    if len(hhmmss.split(':')) != 3:
        log('Incorrect format. Argument must be formatted as HH:MM:SS')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmmss.split(':')[0])) + \
        minutes_to_seconds(hhmmss.split(':')[1]) + int(hhmmss.split(':')[2])

def log(text):
    '''This function logs text to the specified log file'''
    #using the JSON config file to find where the log file\
    #is or is to be located
    with open("./json_files/config.json", "r") as jfile:
        location = json.load(jfile)
        location = location["config"]
        location = location[2]['log_file']
    str(location)
    location = location + str(current_date()) + ".log"
    #specifying how the file is to be logged
    logging.basicConfig(filename=location, level=logging.INFO, format='%(asctime)s %(message)s')
    #writing the input text to the log file
    logging.info(text)
