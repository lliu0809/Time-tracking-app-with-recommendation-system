from ics import Calendar, Event
c = Calendar()
e = Event()
e.name = "My cool event"
e.begin = '2020-12-20 12:00:00'
c.duration = {"minutes":30}
c.events.add(e)
with open('my.ics', 'w') as f:
    f.write(str(c))