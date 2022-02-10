import requests
import xmltodict
import json
###import tkinter

########### THIS APP IS IN EARLY DEMO - TKINTER (GUI) VERSION COMING VERY SOON. #################
########### THIS APP IS IN EARLY DEMO - TKINTER (GUI) VERSION COMING VERY SOON. #################
########### THIS APP IS IN EARLY DEMO - TKINTER (GUI) VERSION COMING VERY SOON. #################
########### THIS APP IS IN EARLY DEMO - TKINTER (GUI) VERSION COMING VERY SOON. #################
# this app is so simple but i was out of ideas dont bully me lmaoo tkinter will make it look more complicated tho so no problem


def getNextDayForecast(inp):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dayi = days.index(inp["current"]["@day"]) + 1
    if dayi > 6: dayi = 0
    returnForecast = None
    for i in inp["forecast"]:
        if i["@day"] == days[dayi]:
            returnForecast = {
                "skytext": i["@skytextday"],
                "high": i["@high"],
                "low": i["@low"],
                "day": i["@day"]
            }
    return returnForecast

def simplifyResults(inp):
    return {
            "locationname": inp["@weatherlocationname"],
            "degreetype": inp["@degreetype"],
            "temperature": inp["current"]["@temperature"],
            "humidity": inp["current"]["@humidity"],
            "skytext": inp["current"]["@skytext"],
            "wind": inp["current"]["@winddisplay"],
            "lat": inp["@lat"],
            "long": inp["@long"],
            "forecast": getNextDayForecast(inp),
            "RAW_DATA": inp
        }

def searchForPlace(toSearch, degreeType="C"):
    resp = requests.get("https://weather.service.msn.com/find.aspx?src=outlook&weadegreetype=" + degreeType + "&culture=en&weasearchstr=" + toSearch)
    try:
        dict_data = xmltodict.parse(resp.content)
    except Exception:
        return 0
    if isinstance(dict_data["weatherdata"]["weather"], list) == True: #multiple results
        arr = []
        for i in dict_data["weatherdata"]["weather"]:
            arr.append(simplifyResults(i))
        return arr
    else: #one result
        return [simplifyResults(dict_data["weatherdata"]["weather"])]


##STARTUP

print("WELCOME TO THE DEMO WEATHER APP, TYPE A PLACE NAME TO SEARCH.")
while True:
    place = input("Type a place >>> ")
    if place == "EXIT": exit()
    res = searchForPlace(place)
    #res = searchForPlace(place, "F")
    if res == 0:
        print("Place not found. Try something else!\n")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))
