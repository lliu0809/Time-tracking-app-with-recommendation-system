import time
import torch
# export PYTHONPATH=$PYTHONPATH:/Users/harold/Personal/Project/course_project/cs130/cs130-proj/recommend-engine/prototype/
import json
import subprocess as cmd
from train import model
from ics import Calendar, Event
import requests
event_dict = {
    0: "class",
    1 : "lunch",
    2 : "nap",
    3 : "study",
    4 : "dinner",
    5 : "other"
}
# new_activity
new_activity_file = "/Users/harold/Personal/Project/course_project/cs130/backup/cs130-proj/preICS.json"
with open(new_activity_file) as f:
    new_activity = json.load(f)['ICSEvents']

# record file
acitivty_time_file = "/Users/harold/Personal/Project/course_project/cs130/backup/cs130-proj/acitivity_time.json"
with open(acitivty_time_file) as f:
    acitivty_time = json.load(f)

# ics file
ics_file = "/Users/harold/Personal/Project/course_project/cs130/calendar_file/my.ics"
with open(ics_file) as f:
    calendar = Calendar(f.read())


# request feedback
new_tracker_file = "/Users/harold/Personal/Project/course_project/cs130/backup/cs130-proj/tracker.txt"
with open(new_tracker_file) as f:
    tracker = f.read()

def update_ics():
    cp = cmd.run("git add --all", check=True, shell=True)

    cp = cmd.run(f"git commit -m 's'", check=True, shell=True)
    cp = cmd.run("git push -u origin main -f", check=True, shell=True)

    commit_name = cmd.check_output(['git', 'rev-parse', 'main']).strip().decode('ascii')

    with open("/Users/harold/Personal/Project/course_project/cs130/backup/cs130-proj/index_backup.html") as f:
        html_str = f.read()
    with open("/Users/harold/Personal/Project/course_project/cs130/backup/cs130-proj/index.html", "w") as f:
        f.write(html_str.replace("%2Fmain%2F", "%2F"+commit_name+"%2F"))

latest_date = 18
week_day = 7
while True:
    time.sleep(0.5)
    #print(time.ctime())
    
    # Check changes to the activity file
    with open(new_activity_file) as f:
        _new_activity = json.load(f)['ICSEvents']
        
        if len(_new_activity) != len(new_activity):
            tmp_new_activity = _new_activity[-(len(_new_activity) - len(new_activity)):]
            #assert(0)
            for activity in tmp_new_activity:
                e = Event()
                e.name = "Lunch" # "date":"2020-12-10","start":"13:00:00","end":"14:00:00"}]
                e.begin = activity["date"] + " " + "19:00:00" #str(int(activity["start"]) + 7)
                e.end = activity["date"] + " " + "20:00:00" #str(int(activity["end"]) + 7)
                calendar.events.add(e)
                with open('my.ics', 'w') as f:
                    f.write(str(calendar))
            update_ics()
            new_activity = _new_activity
        
            acitivty_time["lunch"] += 1

            with open(acitivty_time_file, "w") as f:
                json.dump(acitivty_time, f)
    
    # Check changes to the recommendation 
    with open(new_tracker_file) as f:
        _tracker = f.read()
        if len(_tracker) > len(tracker):
            to_predict = [[6.0, 1], [12.0, 1], [1.0, 1]]
            latest_date += 1
            week_day += 1
            week_day = week_day % 7
            for i in to_predict:

                means  = torch.Tensor([3.5, 6, 0.5]).unsqueeze(0)
                stds = torch.Tensor([7, 12, 1]).unsqueeze(0)

                x = [week_day + 1] + list(i)
                x = torch.Tensor(x).unsqueeze(0)
                x = (x - means) / stds

                y = model(x)
                y = y.argmax(-1).item()
                print(y)

                if y != 5:
                    e = Event()
                    e.name = "Rec:" + event_dict[y]  # "date":"2020-12-10","start":"13:00:00","end":"14:00:00"}]
                    if i[0] == 6.0:
                        start = "01:00:00"
                        e.begin = "2020-10-"+ str(latest_date + 1) + " " + start
                    elif i[0] == 12.0:
                        start = "19:00:00"
                        e.begin = "2020-10-"+ str(latest_date) + " " + start
                    elif i[0] == 1.0:
                        start = "20:00:00"
                        e.begin = "2020-10-"+ str(latest_date) + " " + start
                    
                    e.duration = {"minutes": 60}
                    calendar.events.add(e)
                    with open('my.ics', 'w') as f:
                        f.write(str(calendar))
            update_ics()

            tracker = _tracker
        
                
            


    

