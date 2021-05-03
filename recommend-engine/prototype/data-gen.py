from datetime import date, timedelta
import random

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

######################################################################################
#################    EDIT BY USER   ##################################################
######################################################################################

# cooccurrence, always_occurring, exclusive, noisy_situation
type = "cooccurrence"#'always_occurring'
# cooccurrence = True
# always_occurring = False #(e.g., tests if model reminds user of forgotten activities)
# exclusive = False
# noisy_situation = False # generate always occurring data with some probability
######################################################################################

"""Generates toy data used esp. for different test scenarios to evaluate the effectiveness of the ML model"""
class DataGen():
    def __init__(self):
        self.intervalSlots = {12.0, 12.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5,
                         9.0, 9.5, 10.0, 10.5, 11.0, 11.5}

    """Get calendar date n days ago from today"""
    def getDateNDaysAgo(self, n):
        return date.today() - timedelta(days=n)

    """Using given parameters use feature encoding to form a String that is written into training/testing data files"""
    def writeEntry(self, date, time, am_pm, event):
        return str(date) + ' ' + str(date.weekday()) + ' ' + str(time) + ' ' + str(am_pm) + ' ' + str(event) + '\n'

    """Create a dictionary of all 30min time slots, initially blank (e.g., all fields populated with class “other”)"""
    def createDict(self, myDict, numDays, date, dayStop):
        startDate = date
        for day in range(0, numDays):
            date = startDate + timedelta(days=day)
            myDict[str(date)] = {}
            # initialize all time slots as "other" event
            if day < dayStop:
                for t in self.intervalSlots:
                    myDict[str(date)][str(t) + '.0'] = [date.weekday(), t, 0, 5]
                for t in self.intervalSlots:
                    myDict[str(date)][str(t) + '.1'] = [date.weekday(), t, 1, 5]
        return myDict

    """Populate the given file with dictionary entries of the user actual data and feedback data time slots (used for training & testing)"""
    def writeData(self, dict, file):
        for k, v in dict.items():
            for key in v.keys():
                #myStr = str(k) + ' ' + str(v[key][0]) + ' ' + str(v[key][1]) + ' ' + str(v[key][2]) + ' ' + str(v[key][3]) + '\n'
                myStr = str(k) + " " + " ".join([str(i) for i in v[key]]) + '\n'
                file.write(myStr)
        file.close()


# get n days prior
n = 100
dayRange = 70
trainEndDay = 56
date = DataGen().getDateNDaysAgo(n)
dict_actual = {}
dict_actual = DataGen().createDict(dict_actual, dayRange, date, dayRange)
dict_feedback_alwaysOccur = {}
dict_feedback_alwaysOccur = DataGen().createDict(dict_feedback_alwaysOccur, trainEndDay, date, trainEndDay)
dict_feedback_cooccur = {}
dict_feedback_cooccur = DataGen().createDict(dict_feedback_cooccur, dayRange, date, trainEndDay)
dict_feedback_exclusive = {}
dict_feedback_exclusive = DataGen().createDict(dict_feedback_exclusive, dayRange, date, trainEndDay)
dict_feedback_noisy_situation = {}
dict_feedback_noisy_situation = DataGen().createDict(dict_feedback_noisy_situation, dayRange, date, trainEndDay)
dict_eval = {}
dict_eval = DataGen().createDict(dict_eval, dayRange - trainEndDay, DataGen().getDateNDaysAgo(n - trainEndDay + 1), dayRange - trainEndDay)
# print(dict_eval)

f1 = open("actual_data.txt", "w")
f2 = open("user_feedback.txt", "w")
f3 = open("eval_data.txt", "w")

f4 = open("actual_data_day_count.txt", "w")
f5 = open("user_feedback_day_count.txt", "w")
f6 = open("eval_data_day_count.txt", "w")


################
#cooccurrence###
################

if type == 'cooccurrence':

    # actual data

    f4.write(str(dayRange))

    dateCopy = date
    n_new = n
    for day in range(0, dayRange):

        # 10-11am class M through F, 4-6pm study M through F
        if (not day % 7 == 5) and (not day % 7 == 6) and (day < trainEndDay):
            for time in {10.0, 10.5}:
                dict_actual[str(dateCopy)][str(time) + '.0'] = [dateCopy.weekday(), time, 0, 0]
            for time in {4.0, 4.5, 5.0, 5.5}:
                dict_actual[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 3]

        # 12-1pm lunch and 1-2pm nap after the first 3 weeks
        if (day >= 21):
            for time in {12.0, 12.5}:
                dict_actual[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 1]
            if (day < trainEndDay): # forgot to enter "nap" for days 56 to 70
                for time in {1.0, 1.5}:
                    dict_actual[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 2]

        # 1-2pm lunch for the first 3 weeks (2-3pm nap forgotten)
        if (day < 21):
            for time in {1.0, 1.5}:
                dict_actual[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 1]
            # 2-3pm nap
            for time in {2.0, 2.5}:
                dict_feedback_cooccur[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 2]

        # 6-7pm dinner
        if (day < trainEndDay):
            for time in {6.0, 6.5}:
                dict_actual[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 4]

        n_new -= 1
        dateCopy = DataGen().getDateNDaysAgo(n_new)

    #-----------------------

    # user feedback data for training

    f5.write(str(dayRange))

    n_new = n
    dateCopy = date
    for day in range(0, dayRange):

        # 10-11am class M through F, 4-6pm study M through F
        if (not day % 7 == 5) and (not day % 7 == 6) and (day < trainEndDay):
            for time in {10.0, 10.5}:
                dict_feedback_cooccur[str(dateCopy)][str(time) + '.0'] = [dateCopy.weekday(), time, 0, 0]
            for time in {4.0, 4.5, 5.0, 5.5}:
                dict_feedback_cooccur[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 3]

        # 12-1pm lunch and 1-2pm nap weeks 4-8
        if (day >= 21) and (day < trainEndDay):
            for time in {12.0, 12.5}:
                dict_feedback_cooccur[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 1]
            for time in {1.0, 1.5}:
                dict_feedback_cooccur[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 2]
            '''for time in {1.0, 1.5}:
                dict_feedback_cooccur[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 1]
            # 2-3pm nap
            for time in {2.0, 2.5}:
                dict_feedback_cooccur[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 2]'''

        # 1-2pm lunch and 2-3pm nap for the first 3 weeks
        if (day < 21):
            for time in {2.0, 2.5}:
                dict_feedback_cooccur[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 1]
            # 2-3pm nap
            for time in {3.0, 3.5}:
                dict_feedback_cooccur[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 2]

        # 6-7pm dinner
        if (day < trainEndDay):
            for time in {6.0, 6.5}:
                dict_feedback_cooccur[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 4]

        n_new -= 1
        dateCopy = DataGen().getDateNDaysAgo(n_new)

    # -----------------------

    # user feedback data for evaluation

    f6.write(str(dayRange - trainEndDay + 1))

    n_new = n - trainEndDay + 1
    dateCopy = DataGen().getDateNDaysAgo(n_new)
    for day in range(trainEndDay, dayRange):

        # 10-11am class M through F, 4-6pm study M through F
        if (not day % 7 == 5) and (not day % 7 == 6):
            for time in {10.0, 10.5}:
                dict_eval[str(dateCopy)][str(time) + '.0'] = [dateCopy.weekday(), time, 0, 0]
            for time in {4.0, 4.5, 5.0, 5.5}:
                dict_eval[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 3]

        # 2-3pm lunch and 3-4pm nap
        for time in {2.0, 2.5}:
            dict_eval[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 1]
        for time in {3.0, 3.5}:
            dict_eval[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 2, 2]

        # 6-7pm dinner
        for time in {6.0, 6.5}:
            dict_eval[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 4]

        n_new -= 1
        dateCopy = DataGen().getDateNDaysAgo(n_new)

####################
#always_occurring###
####################

if type == "always_occurring":

    # actual data

    f4.write(str(dayRange))

    dateCopy = date
    n_new = n
    for day in range(0, dayRange):

        # 12-1pm lunch and 1-2pm nap all weeks
        for time in {12.0, 12.5}:
            dict_actual[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 1]
        for time in {1.0, 1.5}:
            dict_actual[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 2]

        # USER FORGETS: 6-7pm dinner all weeks

        n_new -= 1
        dateCopy = DataGen().getDateNDaysAgo(n_new)

    #-----------------------

    # user feedback data for training

    f5.write(str(trainEndDay))

    n_new = n
    dateCopy = date
    for day in range(0, trainEndDay):

        # 12-1pm lunch and 1-2pm nap all weeks
        for time in {12.0, 12.5}:
            dict_feedback_alwaysOccur[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 1]
        for time in {1.0, 1.5}:
            dict_feedback_alwaysOccur[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 2]

        # 6-7pm dinner all weeks
        for time in {6.0, 6.5}:
            dict_feedback_alwaysOccur[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 4]

        n_new -= 1
        dateCopy = DataGen().getDateNDaysAgo(n_new)

    # -----------------------

    # user feedback data for evaluation

    f6.write(str(dayRange - trainEndDay + 1))

    n_new = n - trainEndDay + 1
    dateCopy = DataGen().getDateNDaysAgo(n_new)
    for day in range(trainEndDay, dayRange):

        # 12-1pm lunch and 1-2pm nap all weeks
        for time in {12.0, 12.5}:
            dict_eval[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 1]
        for time in {1.0, 1.5}:
            dict_eval[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 2]

        # 6-7pm dinner all weeks
        for time in {6.0, 6.5}:
            dict_eval[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 4]

        n_new -= 1
        dateCopy = DataGen().getDateNDaysAgo(n_new)

####################
#exclusive##########
####################

if type == "exclusive":

    # actual data

    f4.write(str(dayRange))

    dateCopy = date
    n_new = n
    for day in range(0, dayRange):
        # 10-11am class M through F
        if (not day % 7 == 5) and (not day % 7 == 6) and (day < trainEndDay):
            for time in {10.0, 10.5}:
                dict_actual[str(dateCopy)][str(time) + '.0'] = [dateCopy.weekday(), time, 0, 0]

        # USER FORGETS: there are holidays, e.g., weekdays with no classes

        n_new -= 1
        dateCopy = DataGen().getDateNDaysAgo(n_new)

    #-----------------------

    # user feedback data for training


    n_new = n
    dateCopy = date
    for day in range(0, dayRange):

        # 10-11am class on even dates
        # 11-12am study M on odd dates
        # If I have class, I do not study
        if day % 2 == 0:
            for time in {10.0, 10.5}:
                dict_feedback_exclusive[str(dateCopy)][str(time) + '.0'] = [dateCopy.weekday(), time, 0, 0]
        if day % 2 == 1:
            for time in {11.0, 11.5}:
                dict_feedback_exclusive[str(dateCopy)][str(time) + '.0'] = [dateCopy.weekday(), time, 1, 3]

        # 6-7pm dinner
        if (day < trainEndDay):
            for time in {6.0, 6.5}:
                dict_feedback_exclusive[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 4]

        n_new -= 1
        dateCopy = DataGen().getDateNDaysAgo(n_new)

    # -----------------------

    # user feedback data for evaluation

    f6.write(str(dayRange - trainEndDay + 1))

    n_new = n - trainEndDay + 1
    dateCopy = DataGen().getDateNDaysAgo(n_new)
    for day in range(trainEndDay, dayRange):

        # 10-11am class on even dates
        # 11-12am study M on odd dates
        # If I have class, I do not study
        if day % 2 == 0:
            for time in {10.0, 10.5}:
                dict_eval[str(dateCopy)][str(time) + '.0'] = [dateCopy.weekday(), time, 0, 0]
        if day % 2 == 1:
            for time in {11.0, 11.5}:
                dict_eval[str(dateCopy)][str(time) + '.0'] = [dateCopy.weekday(), time, 1, 3, 2]

        # 6-7pm dinner
        for time in {6.0, 6.5}:
            dict_eval[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 4]

        n_new -= 1
        dateCopy = DataGen().getDateNDaysAgo(n_new)



####################
#noisy_situation####
####################

if type == "noisy_situation":
    # generate all events with some probability

    # actual data

    f4.write(str(dayRange))

    dateCopy = date
    n_new = n
    probability = random.uniform(0, 1)
    for day in range(0, dayRange):

        # 12-1pm lunch and 1-2pm nap all weeks
        if (probability > 0.1):
            for time in {12.0, 12.5}:
                dict_actual[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 1]
            for time in {1.0, 1.5}:
                dict_actual[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 2]

        # USER FORGETS: 6-7pm dinner all weeks

        n_new -= 1
        dateCopy = DataGen().getDateNDaysAgo(n_new)

    # -----------------------

    # user feedback data for training

    f5.write(str(trainEndDay))

    n_new = n
    dateCopy = date
    probability_1 = random.uniform(0, 1)
    probability_2 = random.uniform(0, 1)
    for day in range(0, trainEndDay):

        if (probability_1 > 0.1):
            # 12-1pm lunch and 1-2pm nap all weeks
            for time in {12.0, 12.5}:
                dict_feedback_noisy_situation[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 1]
            for time in {1.0, 1.5}:
                dict_feedback_noisy_situation[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 2]

        if (probability_2 > 0.3):
            # 6-7pm dinner all weeks
            for time in {6.0, 6.5}:
                dict_feedback_noisy_situation[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 4]

        n_new -= 1
        dateCopy = DataGen().getDateNDaysAgo(n_new)

    # -----------------------

    # user feedback data for evaluation

    f6.write(str(dayRange - trainEndDay + 1))

    n_new = n - trainEndDay + 1
    dateCopy = DataGen().getDateNDaysAgo(n_new)
    for day in range(trainEndDay, dayRange):

        # 12-1pm lunch and 1-2pm nap all weeks
        for time in {12.0, 12.5}:
            dict_eval[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 1]
        for time in {1.0, 1.5}:
            dict_eval[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 2]

        # 6-7pm dinner all weeks
        for time in {6.0, 6.5}:
            dict_eval[str(dateCopy)][str(time) + '.1'] = [dateCopy.weekday(), time, 1, 4]

        n_new -= 1
        dateCopy = DataGen().getDateNDaysAgo(n_new)



# populate actual_data, user_feedback
DataGen().writeData(dict_actual, f1)
if type == "cooccurrence":
    DataGen().writeData(dict_feedback_cooccur, f2)
if type == "always_occurring":
    DataGen().writeData(dict_feedback_alwaysOccur, f2)
if type == "exclusive":
    DataGen().writeData(dict_feedback_exclusive, f2)
if type == "noisy_situation":
    DataGen().writeData(dict_feedback_noisy_situation, f2)
DataGen().writeData(dict_eval, f3)

f4.close()
f5.close()
f6.close()