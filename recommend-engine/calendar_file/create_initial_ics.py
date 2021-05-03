from ics import Calendar, Event
c = Calendar()
#ics_file = "/Users/harold/Personal/Project/course_project/cs130/calendar_file/my.ics"
#with open(ics_file) as f:
#    c = Calendar(f.read())

for day in range(12, 19):
    e = Event()
    if day != 18:
        e.name = "Lunch"
        e.begin = '2020-10-{} 19:00:00'.format(day)
        c.duration = {"minutes":60}
        c.events.add(e)

    e = Event()
    e.name = "Nap"
    e.begin = '2020-10-{} 20:00:00'.format(day)
    c.duration = {"minutes":60}
    c.events.add(e)

    e = Event()
    e.name = "Dinner"
    e.begin = '2020-10-{} 01:00:00'.format(day + 1)
    c.duration = {"minutes":60}
    c.events.add(e)

for day in range(0, 8):
    
    if day == 0 or day == 4:
        e = Event()
        e.name = "Study"
        e.begin = '2020-09-{} 15:00:00'.format(day + 14)
        c.duration = {"minutes":60}
        c.events.add(e)


        e = Event()
        e.name = "Nap"
        e.begin = '2020-09-{} 16:00:00'.format(day + 14)
        c.duration = {"minutes":60}
        c.events.add(e)
    
    if day == 1 or (day == 2 or day == 5):
        e = Event()
        e.name = "Study"
        e.begin = '2020-09-{} 16:00:00'.format(day + 14)
        c.duration = {"minutes":60}
        c.events.add(e)

        e = Event()
        e.name = "Nap"
        e.begin = '2020-09-{} 17:00:00'.format(day + 14)
        c.duration = {"minutes":60}
        c.events.add(e)

    e = Event()
    e.name = "Dinner"
    e.begin = '2020-09-{} 01:00:00'.format(day + 15)
    c.duration = {"minutes":60}
    c.events.add(e)
e = Event()
e.name = "Study"
e.begin = '2020-09-21 17:00:00'
c.duration = {"minutes":60}
c.events.add(e)

e = Event()
e.name = "Rec:nap"
e.begin = '2020-09-21 18:00:00'
c.duration = {"minutes":60}
c.events.add(e)




with open('originalc.ics', 'w') as f:
    f.write(str(c))
with open('my.ics', 'w') as f:
    f.write(str(c))

import subprocess as cmd
cp = cmd.run("git add --all", check=True, shell=True)

cp = cmd.run(f"git commit -m 's'", check=True, shell=True)
cp = cmd.run("git push -u origin main -f", check=True, shell=True)

commit_name = cmd.check_output(['git', 'rev-parse', 'main']).strip().decode('ascii')

with open("/Users/harold/Personal/Project/course_project/cs130/backup/cs130-proj/index_backup.html") as f:
    html_str = f.read()
with open("/Users/harold/Personal/Project/course_project/cs130/backup/cs130-proj/index.html", "w") as f:
    f.write(html_str.replace("%2Fmain%2F", "%2F"+commit_name+"%2F"))

import json
activity_time = {"class": 0, "lunch": 6, "nap": 12, "study": 13, "dinner": 14, "other": 0}
with open("/Users/harold/Personal/Project/course_project/cs130/backup/cs130-proj/acitivity_time.json", "w") as f:
    json.dump(activity_time, f)