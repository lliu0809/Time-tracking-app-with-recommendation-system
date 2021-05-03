from datetime import date, timedelta
import json

# "class": 0,
# "lunch": 1,
# "nap": 2,
# "study": 3,
# "dinner": 4
# "other": 5

# data format
# [date, day, time, AM/PM, event], day={0 (Mon), 1, ..., 6 (Sun)}, time={12.0, 12.5, ..., 11.5}, AM/PM= {0=AM, 1=PM}, event={0, 1, ..., 4}

# get the day corresponding to date: day={0 (Mon), 1, ..., 6 (Sun)}
# date.weekday()

# THIS GENERATES DEFAULT JSON VALUES FOR THE CURRENT WEEK
# HERE IS A SAMPLE
#  "2020-11-30": {
#     "10:30_0": {              -> time_0=AM, time_1=PM
#       "unsatisfied": 0,       -> 1 means unsatisfied
#       "ideal_start": "",      -> time string
#       "start_time": "10:30",  -> time string
#       "ideal_ampm": "",       -> "AM" or "PM"
#       "date": "2020-11-30",
#       "duration": 0,          -> float
#       "day": "Monday",
#       "starter": 0            -> signals the beginning time for an activity
#       "category": "other",    -> string version of event
#       "ampm": "AM",  
#       "ideal_duration": 0,    -> float
#       "newConflict" : 0,      -> newly added event in feedback table causes conflict -> 1
#       "activity": ""          -> activity name, ex: playing soccer
#     },


intervalSlots = {"12:00", "12:30", "1:00", "1:30", "2:00", "2:30", "3:00", "3:30", "4:00", "4:30", "5:00", "5:30", "6:00", "6:30", "7:00", "7:30", "8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30"}

weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")


def getDateNDaysAgo(n):
    return date.today() - timedelta(days=n)

def createDict(myDict, numDays, date):
    startDate = date
    for day in range(0, numDays):
        date = startDate + timedelta(days=day)
        myDict[str(date)] = {}
        #initialize all time slots as "other" event
        for t in intervalSlots:
            myDict[str(date)][t + '_0'] = {"date": str(date), "day": weekDays[date.weekday()], "activity": "", "start_time": t, "duration": 0, "ampm": "AM", "category": "other", "unsatisfied": 0, "ideal_start": "", "ideal_duration": 0, "ideal_ampm":"", "starter": 0, "newConflict": 0}
            myDict[str(date)][t + '_1'] = {"date": str(date), "day": weekDays[date.weekday()], "activity": "", "start_time": t, "duration": 0, "ampm": "PM", "category": "other", "unsatisfied": 0, "ideal_start": "", "ideal_duration": 0, "ideal_ampm":"", "starter":0, "newConflict": 0}
    return myDict

# get n days prior
n = 0
today = date.today().weekday()
if today < 6:
    n = today + 1
dayRange = 7
date = getDateNDaysAgo(n)
json_dict = {}
json_dict = createDict(json_dict, dayRange, date)

with open("default_json.txt", "w") as json_file:
    json.dump(json_dict, json_file, indent=2)



