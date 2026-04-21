from pylibrelinkup import PyLibreLinkUp
from pylibrelinkup import api_url
from datetime import datetime
import tkinter as tk
import getpass
#import os
import time
import configparser
import matplotlib.pyplot as plt
import sched, time

def getllvalues():
    global lblvalue
#    scheduler.enter(60, 1, getllvalues, (scheduler,))
    sensor_reading = client.latest(patient_identifier=patient)
    nowtime = datetime.now()
    lastmeas = sensor_reading.timestamp
    diff = nowtime - lastmeas
    textdisplay = str(sensor_reading.value) + sensor_reading.trend.indicator
    if sensor_reading.measurement_color == 1:
        thecolour = COLOUR_GREEN
        colour1 = "green"
        colour2 = "black"
        lblvalue.config(text = textdisplay,fg = "green")
    elif sensor_reading.measurement_color == 2:
        thecolour = COLOUR_YELLOW
        colour1 = "yellow"
        colour2 = "black"
        lblvalue.config(text = textdisplay,fg = "yellow")
    elif sensor_reading.measurement_color == 3:
        thecolour = COLOUR_ORANGE
        colour1 = "orange"
        colour2 = "black"
        lblvalue.config(text = textdisplay,fg = "orange")
    elif sensor_reading.measurement_color == 4:
        thecolour = COLOUR_RED
        colour1 = "red"
        colour2 = "black"
        lblvalue.config(text = textdisplay,fg = "red")
    else:
        thecolour = COLOUR_WHITE
        colour1 = "white"
        colour2 = "black"
    if diff.total_seconds()>=70:
        print(f"{COLOUR_NEGATIVE}{sensor_reading.timestamp} Current Reading: {thecolour}{sensor_reading.value}{COLOUR_RESET}{COLOUR_NEGATIVE}{" HIGH" if sensor_reading.is_high else ""}{" LOW" if sensor_reading.is_low else ""} Trend: {sensor_reading.trend.indicator} Offline for: {diff}{COLOUR_RESET}")
        lblvalue.config(text = textdisplay,fg = colour2, bg = colour1)
        lbltime.config(text = sensor_reading.timestamp,fg = colour2, bg = colour1)
    else:
        print(f"{sensor_reading.timestamp} Current Reading: {thecolour}{sensor_reading.value}{COLOUR_RESET}{" HIGH" if sensor_reading.is_high else ""}{" LOW" if sensor_reading.is_low else ""} Trend: {sensor_reading.trend.indicator}")
        lblvalue.config(text = textdisplay,fg = colour1, bg = colour2)
        lbltime.config(text = sensor_reading.timestamp,fg = colour1, bg = colour2)
    window.after(60000,getllvalues)
    
def getllvaluesgraph():
    global graph
#    scheduler.enter(300, 1, getllvaluesgraph, (scheduler,))
    graph_data = client.graph(patient_identifier=patient)
    x.clear()
    y.clear()
    for measurement in graph_data:
#        print(f"{measurement.value} {measurement.timestamp}")
        x.append(measurement.timestamp)
        y.append(measurement.value)
    graph.remove()
    graph = plt.plot(x, y)[0]
    #plt.gcf().autofmt_xdate()
    plt.pause(0.25)
    
#os.environ["http_proxy"] = "<server>:<port>"
#os.environ["https_proxy"] = "<server>:<port>"

window = tk.Tk()
window.title('Current CGM')
window.configure(bg = "black")
lblvalue = tk.Label(window, text = "---",bg = "black", font=("Arial",192))
lbltime = tk.Label(window, text = "--/--/---- --:--:--",bg = "black", font=("Arial",18))
lblvalue.pack()
lbltime.pack()

COLOUR_RED = '\033[31m'
COLOUR_GREEN = '\033[32m'
COLOUR_YELLOW = '\033[33m' # orange on  some systems
COLOUR_WHITE = '\033[97m'
COLOUR_ORANGE = '\033[38;2;255;165;0m'
COLOUR_RESET = '\033[0m' # called to return to standard terminal text color
COLOUR_NEGATIVE = "\033[7m"

config = configparser.ConfigParser()
config.read('config.ini')

the_username = config['account']['llusername']
the_password = getpass.getpass(prompt='Enter password: ')

client = PyLibreLinkUp(email=the_username, password=the_password, api_url = api_url.APIUrl.EU2)
client.authenticate()

patient_list = client.get_patients()
print(patient_list)

#colours:
# 0 = ?
# 1 = green
# 2 = yellow
# 3 = ?
# 4 = red
patient = patient_list[0]

#plt.ion()
#x = []
#y = []
#graph = plt.plot(x, y)[0]
#plt.xlabel('Date')
#plt.ylabel('CGM')
#plt.pause(0.25)

#my_scheduler = sched.scheduler(time.time, time.sleep)
#my_scheduler.enter(0, 1, getllvalues, (my_scheduler,))
#my_scheduler.enter(0, 1, getllvaluesgraph, (my_scheduler,))
#my_scheduler.run()

window.after(0,getllvalues)
window.mainloop()

#other useful functions, for noting
#
#print(f"graph data ({len(graph_data)} measurements):")
#
#logbook_data = client.logbook(patient_identifier=patient)
#print(f"logbook data: ({len(logbook_data)} entries)")
#
#for measurement in logbook_data:
#    print(f"{measurement.value} {measurement.timestamp} {measurement.factory_timestamp}")
