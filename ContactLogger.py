import tkinter as tk
import tkinter.messagebox
from tkinter import font
from datetime import datetime
import csv
from tkinter import *


HEIGHT = 500 # WINDOW HEIGHT
WIDTH = 600 # WINDOW WIDTH
BACKGROUND = "slate grey"




# FUNCTION AREA
def loggerPopup():
	tkinter.messagebox.showinfo(title = "W7DXD Logger", message = "Contact Logged")

def submitLog():
	if popupVar.get() == 0:
		loggerPopup()
	with open("ContactLog.csv", mode = "a", newline = "") as csvfile:
		x = csv.writer(csvfile, delimiter = ",")
		x.writerow([callSignEntry.get(), freqEntry.get(), timeEntry.get(), locationEntry.get(), modeDrop.get(modeDrop.curselection())])

	callSignEntry.delete(0, 20)
	timeEntry.delete(0, 20)
	locationEntry.delete(0, 20)
	
	

def getTime():
	now = datetime.utcnow()
	currentTime = now.strftime("%H:%M:%S")
	timeEntry.delete(0, 20)
	timeEntry.insert(0, currentTime)



# WINDOW AREA
window = tk.Tk()

popupVar = tk.IntVar() # VARIABLE FOR CHECKBOX (HAS TO BE WITHIN TK.TK() AREA)

window.title("W7DXD Simple Contact Logger")

canvas = tk.Canvas(window, height = HEIGHT, width = WIDTH)
canvas.pack()

frame = tk.Frame(window, bg = BACKGROUND)
frame.place(relheight = 1, relwidth = 1)

titleLabel = tk.Label(frame, text = "Simple Contact Logger", bg = BACKGROUND, font = ("rockwell, 14"))
titleLabel.place(relx = .3, rely = -.02, relheight = .15, relwidth = .4)

submitButton = tk.Button(frame, text = "Submit", command = lambda : submitLog())
submitButton.place(relx = .4, rely = .9, relheight = .04, relwidth = .2)

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
getTimeButton.place(relx = .425, rely = .2, relheight = .04, relwidth = .1)

locationLabel = tk.Label(window,text = 'GRID SQR', bg = BACKGROUND, font = ('rockwell', 10))
locationLabel.place(relx = .55, rely = .1, relheight = .04, relwidth = .145)

locationEntry = tk.Entry(window)
locationEntry.place(relx = .555, rely = .15, relheight = .04, relwidth = .145)

modeLabel = tk.Label(window,text = 'MODE', bg = BACKGROUND, font = ('rockwell', 10))
modeLabel.place(relx = .70, rely = .1, relheight = .04, relwidth = .145)

modeDrop = tk.Listbox(window)
modeDrop.insert(1, "      SSB     ")
modeDrop.insert(2, "      FM      ")
modeDrop.insert(3, "      AM      ")
modeDrop.insert(4, "      FT8     ")
modeDrop.insert(5, "      JS8     ")
modeDrop.insert(6, "      RTTY    ")
modeDrop.insert(7, "      CW      ")
modeDrop.place(relx = .725, rely = .15, relheight = .23, relwidth = .10)

popupCheckBox = tk.Checkbutton(window, text = "Disable Popup", bg = BACKGROUND, font = ('rockwell', 10), variable = popupVar)
popupCheckBox.place(relx = .715, rely = .4)




window.mainloop()
