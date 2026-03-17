from pylibrelinkup import PyLibreLinkUp
from pylibrelinkup import api_url
from datetime import datetime
import getpass
import os
import time
import configparser

#os.environ["http_proxy"] = "<server>:<port>"
#os.environ["https_proxy"] = "<server>:<port>"

COLOUR_RED = '\033[31m'
COLOUR_GREEN = '\033[32m'
COLOUR_YELLOW = '\033[33m' # orange on some systems
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
while True:
    sensor_reading = client.latest(patient_identifier=patient)
    nowtime = datetime.now()
    lastmeas = sensor_reading.timestamp
    diff = nowtime - lastmeas
    if sensor_reading.measurement_color == 1:
        thecolour = COLOUR_GREEN
    elif sensor_reading.measurement_color == 2:
        thecolour = COLOUR_YELLOW
    elif sensor_reading.measurement_color == 3:
        thecolour = COLOUR_ORANGE
    elif sensor_reading.measurement_color == 4:
        thecolour = COLOUR_RED
    else:
        thecolour = COLOUR_WHITE
    if diff.total_seconds()>=70:
        print(f"{COLOUR_NEGATIVE}{sensor_reading.timestamp} Current Reading: {thecolour}{sensor_reading.value}{COLOUR_WHITE}{" HIGH" if sensor_reading.is_high else ""}{" LOW" if sensor_reading.is_low else ""} Trend: {sensor_reading.trend.indicator} Offline for: {diff}{COLOUR_RESET}")
    else:
        print(f"{sensor_reading.timestamp} Current Reading: {thecolour}{sensor_reading.value}{COLOUR_RESET}{" HIGH" if sensor_reading.is_high else ""}{" LOW" if sensor_reading.is_low else ""} Trend: {sensor_reading.trend.indicator}")
    time.sleep(60)

#other useful functions, for noting
#
#graph_data = client.graph(patient_identifier=patient)
#print(f"graph data ({len(graph_data)} measurements):")
#
#for measurement in graph_data:
#    print(f"{measurement.value} {measurement.timestamp} {measurement.factory_timestamp}")
#
#logbook_data = client.logbook(patient_identifier=patient)
#print(f"logbook data: ({len(logbook_data)} entries)")
#
#for measurement in logbook_data:
#    print(f"{measurement.value} {measurement.timestamp} {measurement.factory_timestamp}")
