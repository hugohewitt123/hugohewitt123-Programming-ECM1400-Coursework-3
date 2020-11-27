'''This module pulls the releveent information from the covid api'''
import json
import requests
from time_conversions import log

def get_covid():
    '''This function gets the date for today and
    gets the key from teh confic json file and
    it then calls the api and returns the response'''
    #getting the users region from the config json file
    with open("./json_files/config.json", "r") as jfile:
        key = json.load(jfile)
        key = key["config"]
        region_name = key[4]['Area_location']
    #concatonating the url fro teh api call, involving the location and the structure\
    #which is, area name, date, new cases & new deaths
    complete_url = 'https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=region;areaName='\
        + region_name + '&structure={"areaName":"areaName","date":"date",'\
            +'"newCases":"newCasesByPublishDate","newDeaths":"newDeaths28DaysByPublishDate"}'
    #trying to get the data from the api call, if it can't
    #it will return failed so that the program can continue
    try:
        #making an api call with the requests module and the url
        response = requests.get(complete_url)
        report = response.json()
        #getting the data from the call
        report = report['data']
        #logging that the data has been retrieved
        log("covid data retrieved -- " + str(requests.get(complete_url)))
        #returning the latest data from the report data
        return report[0]
    except:
        #logging and returning that the api calling has errored
        log("FAILED to get covid data from api" + str(requests.get(complete_url)))
        return "error getting covid info, api call error"
