from configparser import ConfigParser
import os
import sys

import tkinter as tk
import tkinter.messagebox
from tkinter import font
from datetime import datetime
import csv
from tkinter import *
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys




config = ConfigParser()
config.read("config.ini")
CHROME_DRIVER_PATH = config.get("chromedriver", "path")

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)



HEIGHT = 500 # WINDOW HEIGHT
WIDTH = 600 # WINDOW WIDTH
BACKGROUND = "slate grey"



time = None

QRZ = "https://logbook.qrz.com/api"
key = ""
stationCall = ""
apiRequest = ""


# SELENIUM AREA

def callSearch():
	driver = webdriver.Chrome(CHROME_DRIVER_PATH)
	driver.get("https://www.qrz.com/lookup")
	search = driver.find_element_by_id("cs")
	search.send_keys(callSignEntry.get())
	search.send_keys(Keys.RETURN)
	

def pskReporter():
	PATH = "C:\chromedriver.exe"
	driver = webdriver.Chrome(PATH)
	driver.get("https://pskreporter.info/pskmap.html")
	search = driver.find_element_by_id("callsignfield")
	search.send_keys(stationCall)
	search.send_keys(Keys.RETURN)


def qrzNow():
	PATH = "C:\chromedriver.exe"
	driver = webdriver.Chrome(PATH)
	driver.get("https://qrznow.com/real-time-band-conditions/")
	
	
	


# FUNCTION AREA
def loggerPopup():
	tkinter.messagebox.showinfo(title = "W7DXD Logger", message = "Contact Logged")

def submitLog():
	global apiRequest
	global time
	time = datetime.utcnow()
	if popupVar.get() == 0:
		loggerPopup()
	with open("ContactLog.csv", mode = "a", newline = "") as csvfile:
		x = csv.writer(csvfile, delimiter = ",")
		x.writerow([callSignEntry.get(), freqEntry.get(), timeEntry.get(), locationEntry.get(), modeDrop.get(modeDrop.curselection())])

	band = ""
	try:
		if float(freqEntry.get()) <= 2.0:
			band = "160m"
		if float(freqEntry.get()) >= 3.5 and float(freqEntry.get()) <= 4.0:
			band = "80m"
		if float(freqEntry.get()) >= 5.3 and float(freqEntry.get()) <= 5.5:
			band = "60m"
		if float(freqEntry.get()) >= 7.0 and float(freqEntry.get()) <= 7.3:
			band = "40m"
		if float(freqEntry.get()) >= 10.1 and float(freqEntry.get()) <= 10.150:
			band = "30m"
		if float(freqEntry.get()) >= 14.0 and float(freqEntry.get()) <= 14.350:
			band = "20m"
		if float(freqEntry.get()) >= 18.068 and float(freqEntry.get()) <= 18.168:
			band = "17m"
		if float(freqEntry.get()) >= 21.0 and float(freqEntry.get()) <= 21.450:
			band = "15m"
		if float(freqEntry.get()) >= 24.890 and float(freqEntry.get()) <= 24.990:
			band = "12"
		if float(freqEntry.get()) >= 28.0 and float(freqEntry.get()) <= 29.7:
			band = "10m"
		if float(freqEntry.get()) >= 50.0 and float(freqEntry.get()) <= 54.0:
			band = "6m"
		if float(freqEntry.get()) >= 144.0 and float(freqEntry.get()) <= 148.0:
			band = "2m"
	except:
		print("ERROR WITH FREQ")


	apiRequest = QRZ + "?" + "KEY=" + config["APIKEY"]["key"] + "&ACTION=INSERT&ADIF=<band:" + str(len(band)) + ">" + band + "<mode:" + str(len(modeDrop.get(modeDrop.curselection()))) +">" + modeDrop.get(modeDrop.curselection()) + "<freq:" + str(len(freqEntry.get())) +">" + freqEntry.get() + "<call:" + str(len(callSignEntry.get())) + ">" + callSignEntry.get() + "<qso_date:8>" + time.strftime("%Y%m%d") + "<station_callsign:" + str(len(stationCall)) + ">" + config["CALLSIGN"]["call"] + "<time_on:4>" + time.strftime("%H%M") + "<eor>"
	APILOG = requests.get(apiRequest)
	print(apiRequest)
	print(APILOG)


	callSignEntry.delete(0, 20)
	timeEntry.delete(0, 20)
	locationEntry.delete(0, 20)
	
def getTime():
	now = datetime.utcnow()
	currentTime = now.strftime("%H:%M:%S")
	timeEntry.delete(0, 20)
	timeEntry.insert(0, currentTime)
	

def setupSubmit():
	config["APIKEY"]["key"] = keyEntry.get()
	config["CALLSIGN"]["call"] = yourCallEntry.get()
	with open("config.ini", "w") as configFile:
		config.write(configFile)
	setupWindow.withdraw()
	


# WINDOW AREA
window = tk.Tk()
popupVar = tk.IntVar() # VARIABLE FOR CHECKBOX (HAS TO BE WITHIN TK.TK() AREA)


window.title("W7DXD Simple Contact Logger")
icon = PhotoImage(file = "icon.png")
try:
	window.iconphoto(True, icon)
except:
	pass

canvas = tk.Canvas(window, height = HEIGHT, width = WIDTH)
canvas.pack()

frame = tk.Frame(window, bg = BACKGROUND)
frame.place(relheight = 1, relwidth = 1)

titleLabel = tk.Label(frame, text = "Simple Contact Logger", bg = BACKGROUND, font = ("rockwell, 14"))
titleLabel.place(relx = .3, rely = -.02, relheight = .15, relwidth = .4)

submitButton = tk.Button(frame, text = "Submit", command = lambda : submitLog())
submitButton.place(relx = .85, rely = .15, relheight = .2, relwidth = .14)

callSignLabel = tk.Label(window, text = 'CALLSIGN', bg = BACKGROUND, font = ('rockwell', 10))
callSignLabel.place(relx = .1, rely = .1, relheight = .04, relwidth = .12)

callSignEntry = tk.Entry(window)
callSignEntry.place(relx = .1, rely = .15, relheight = .04, relwidth = .12)

freqLabel = tk.Label(window,text = 'FREQUENCY', bg = BACKGROUND, font = ('rockwell', 10))
freqLabel.place(relx = .25, rely = .1, relheight = .04, relwidth = .145)

freqEntry = tk.Entry(window)
freqEntry.place(relx = .25, rely = .15, relheight = .04, relwidth = .145)

timeLabel = tk.Label(window,text = 'UTC TIME', bg = BACKGROUND, font = ('rockwell', 10))
timeLabel.place(relx = .40, rely = .1, relheight = .04, relwidth = .145)

timeEntry = tk.Entry(window)
timeEntry.place(relx = .425, rely = .15, relheight = .04, relwidth = .1)

getTimeButton = tk.Button(frame, text = "Get Time", command = lambda : getTime())
getTimeButton.place(relx = .425, rely = .21, relheight = .04, relwidth = .1)

locationLabel = tk.Label(window,text = 'GRID SQR', bg = BACKGROUND, font = ('rockwell', 10))
locationLabel.place(relx = .55, rely = .1, relheight = .04, relwidth = .145)

locationEntry = tk.Entry(window)
locationEntry.place(relx = .555, rely = .15, relheight = .04, relwidth = .145)

modeLabel = tk.Label(window,text = 'MODE', bg = BACKGROUND, font = ('rockwell', 10))
modeLabel.place(relx = .70, rely = .1, relheight = .04, relwidth = .145)

modeDrop = tk.Listbox(window)
modeDrop.insert(1, "SSB")
modeDrop.insert(2, "FM")
modeDrop.insert(3, "AM")
modeDrop.insert(4, "FT8")
modeDrop.insert(5, "JS8")
modeDrop.insert(6, "RTTY")
modeDrop.insert(7, "CW")
modeDrop.place(relx = .725, rely = .15, relheight = .23, relwidth = .1)
modeDrop.select_set(0)

popupCheckBox = tk.Checkbutton(window, text = "Disable Popup", bg = BACKGROUND, font = ('rockwell', 10), variable = popupVar)
popupCheckBox.place(relx = .715, rely = .4)

setupButton = tk.Button(window, text = "Setup", command = lambda : setupWindow.deiconify())
setupButton.place(relx = .725, rely = .46, relheight = .04, relwidth = .12)

searchCall = tk.Button(frame, text = "Search on QRZ", command = lambda : callSearch())
searchCall.place(relx = .088, rely = .21, relheight = .04, relwidth = .145)

openPSK = tk.Button(frame, text = "Open PSK Reporter", command = lambda : pskReporter())
openPSK.place(relx = .725, rely = .56, relheight = .038, relwidth = .18)

bandCond = tk.Button(frame, text = "Open Band Conditions", command = lambda : qrzNow())
bandCond.place(relx = .725, rely = .51, relheight = .038, relwidth = .22)






# SETUP WINDOW
setupWindow = Toplevel(frame, bg = BACKGROUND, height = HEIGHT / 2, width = WIDTH / 2)
keyLabel = tk.Label(setupWindow, text = "API Key", bg = BACKGROUND, font = ("rockwell, 14"))
keyLabel.place(relx = .3, rely = .02, relheight = .15, relwidth = .4)

def on_closing():  # FIXES ISSUE WITH SETUPWINDOW ONLY OPENING ONCE.
	setupWindow.withdraw()

setupWindow.protocol("WM_DELETE_WINDOW", on_closing)  # FIXES ISSUE WITH SETUPWINDOW ONLY OPENING ONCE.


if config["APIKEY"]["key"] != "" and config["CALLSIGN"]["call"] != "":
	setupWindow.withdraw()
	

keyEntry = tk.Entry(setupWindow)
keyEntry.insert(0, config["APIKEY"]["key"])
keyEntry.place(relx = .1, rely = .15, relheight = .1, relwidth = .8)

yourCallLabel = tk.Label(setupWindow, text = "Your Callsign", bg = BACKGROUND, font = ("rockwell, 14"))
yourCallLabel.place(relx = .1, rely = .4, relheight = .15, relwidth = .8)

yourCallEntry = tk.Entry(setupWindow)
yourCallEntry.insert(0, config["CALLSIGN"]["call"])
yourCallEntry.place(relx = .35, rely = .55, relheight = .1, relwidth = .3)

setupSubmitButton = tk.Button(setupWindow, text = "Submit", command = lambda : setupSubmit())
setupSubmitButton.place(relx = .4, rely = .85, relheight = .1, relwidth = .2)






window.mainloop()

