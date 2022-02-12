import requests
import xmltodict
import json
from tkinter import *

# şu bir yer arıyınca butonlar geliyor ya he onları frame içine koy böylece kolay temizle .destroy() ile, çünkü şuan enter spamlayınca bir sürü yazı oluşuyor silinmiyor

########### THIS APP IS IN EARLY DEMO ###############
########### THIS APP IS IN EARLY DEMO ###############
########### THIS APP IS IN EARLY DEMO ###############
# this app is so simple but i was out of ideas dont bully me lmaoo

with open("settings.json", "r") as json_file:
    data = json.load(json_file)


#def updateFile():
#    with open("settings.json", "w") as json_file:
#        json.dump(data, json_file, indent=4, sort_keys=False)

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
    if degreeType != "C" and degreeType != "F":
        degreeType = "C"
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

GUI = Tk()
GUI.title("HELLO")
GUI.minsize(500, 500)

guigap = Label(GUI, text=" \n ")
guigap.pack()
mf = Frame(GUI) # main frame
mf.pack(side=TOP, fill=X)
#gf = Frame(GUI, bd=0) # gridded frame
#gf.pack(side=TOP, fill=X)

def search():
    label = Label(mf, text="Please enter a place name to search for weather:")
    label.pack()
    entry = Entry(mf)
    entry.pack()
    Label(mf, text="").pack() #space

    def buttonFunc():
        for w in outputFrame.winfo_children():
            w.destroy()
        print("Recieved", entry.get())
        res = searchForPlace(entry.get(), data["degreeType"])
        print(json.dumps(res, indent=4, sort_keys=True))
        if res == 0:
            Label(outputFrame, text="Place not found").pack()
        else:
            Label(outputFrame, text="Please click one of the places to see the weather:").pack()
            def turnDataToString(index):
                d = res[index]
                op = ""
                for w in outputFrame.winfo_children():
                    w.destroy()
                op = op + "Place Name: " + d["locationname"]
                op = op + "\n\n-- Today --"
                op = op + "\nTemperature: " + d["temperature"] + " " + data["degreeType"]
                op = op + "\nStatus: " + d["skytext"]
                op = op + "\nWind: " + d["wind"]
                op = op + "\nHumidity: " + d["humidity"] + "%\n\n"
                op = op + "-- Tomorrows Forecast --"
                op = op + "\nDay: " + d["forecast"]["day"]
                op = op + "\nStatus: " + d["forecast"]["skytext"]
                op = op + "\nHigh: " + d["forecast"]["high"] + " " + data["degreeType"]
                op = op + "\nStatus: " + d["forecast"]["low"] + " " + data["degreeType"]
                Label(outputFrame, text=op).pack()
                
            indx = 0
            for i in res:
                b = Button(outputFrame, text=i["locationname"], command=lambda indx=indx: turnDataToString(indx))
                b.pack()
                indx += 1


    button = Button(mf, text="ENTER", command=buttonFunc)
    button.pack()
    Label(mf, text="").pack() #space
    outputFrame = Frame(mf)
    outputFrame.pack()

search()

GUI.mainloop()