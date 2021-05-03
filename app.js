var express = require('express')
var app = express();
app.use(express.static(__dirname));
const fs = require('fs');

/* test commands ???
app.use(express.static("public"));
app.set("view engine", "ejs");
const http = require('http');
const { time } = require('console');
*/

// uncomment your path, comment the rest
let path = "/Users/Ethan/Desktop/CS130/cs130-proj/"
// let path = "/Users/harold/Personal/Project/course_project/cs130/backup/cs130-proj/"

/* actual_data contains calendar inputs
feedback_j contains feedback table inputs
mod_feedback_j contains the correct time intervals for added events/ideal times to be converted into ML system input
*/
var feedback_j = "./feedback.json";
var mod_feedback_j = "./mod_feedback.json";

// filename of ML system input
var fb_txt = "./user_feedback.txt";

// dicts to convert from json object values to ML-readable values
var dayToNum = {
	"Monday":0,
	"Tuesday":1,
	"Wednesday":2,
	"Thursday":3,
	"Friday":4,
	"Saturday":5,
	"Sunday":6,
};
var timeToNum = {
	"1:00": 1.0,
	"1:30": 1.5,
	"2:00": 2.0,
	"2:30": 2.5,
	"3:00": 3.0,
	"3:30": 3.5,
	"4:00": 4.0,
	"4:30": 4.5,
	"5:00": 5.0,
	"5:30": 5.5,
	"6:00": 6.0,
	"6:30": 6.5,
	"7:00": 7.0,
	"7:30": 7.5,
	"8:00": 8.0,
	"8:30": 8.5,
	"9:00": 9.0,
	"9:30": 9.5,
	"10:00": 10.0,
	"10:30": 10.5,
	"11:00": 11.0,
	"11:30": 11.5,
	"12:00": 12.0,
	"12:30": 12.5,
};
var numToTime = {
	1.0:"1:00",
	1.5:"1:30",
	2.0:"2:00",
	2.5:"2:30",
	3.0:"3:00",
	3.5:"3:30",
	4.0:"4:00",
	4.5:"4:30",
	5.0:"5:00",
	5.5:"5:30",
	6.0:"6:00",
	6.5:"6:30",
	7.0:"7:00",
	7.5:"7:30",
	8.0:"8:00",
	8.5:"8:30",
	9.0:"9:00",
	9.5:"9:30",
	10.0:"10:00",
	10.5:"10:30",
	11.0:"11:00",
	11.5:"11:30",
	12.0:"12:00",
	12.5:"12:30",
};
var ampmToNum = {
	AM: 0,
	PM: 1,
};
var catToNum = {
	class: 0,
	lunch: 1,
	nap: 2,
	study: 3,
    dinner: 4,
    other: 5,
};

// dicts to convert from ML readable values to json object
var htmlMinute = {
    0: "00",
    1: "30",
} 
var htmlAMPM = {
    0: "AM",
    1: "PM",
}
var htmlDay = {
    0:"Monday",
    1:"Tuesday",
    2:"Wednesday",
    3:"Thursday",
    4:"Friday",
    5:"Saturday",
    6:"Sunday",
}
var htmlActType = {
    0:"class",
    1:"lunch",
    2:"nap",
    3:"study",
    4:"dinner",
    5:"other",
}

/*
call this to update json file for every new event object
override=1 -> will override conflicting time slots(set by mod-feedback json)
override=0 -> leaves conflicting time slots alone(set by actual_data & feedback json)
*/
// when new events are added, the event with the starting time has starter=1
function modifyJson(event, json, override) {
    const thisWeek = require(json);

    let time, ampm, duration;

    time = event["start_time"];
    ampm = ampmToNum[event["ampm"]];
    duration = event["duration"];

    let loops = duration / 0.5,
        j = 0;    
    // update each 30-min event according to dateKey, recalculating timeKey each time
    // timeKey's time increments by 0.5 for every 30-min interval

    for (var i = 0; i < loops; i++){
        let newTime = (numToTime[(timeToNum[time] + (j * 0.5))]);
        j++;

        // flip AM/PM at 12:00
        if (newTime == "12:00") {
            if (ampm == 0) ampm = 1;
            else ampm = 0;
        } else if (newTime == "12:30") {
            // wrap-around 12:30 mark back to 1:00
            time = "1:00";
            j = 0;
        }

        // now i have the correct time index and its properties
        let timeKey = newTime + '_' + ampm;
        let obj = thisWeek[event["date"]][timeKey];
        // console.log(obj);
        if (override) {
            // prior to getUFJ calling this, there should've been several calls to modifyJson from feedback page's js file, trying to update its copy of feedback json & mod_feedback.json with new events from user input. 
            // don't care if there is an activity. if this was an unsatisfied activity, itll have been erased so we treat it like a regular activity
            // for the sake of user_feedback.txt, we only need to change category
            obj["category"] = event["category"];
            obj["activity"] = event["activity"];
            // console.log(obj);

        } else if (!obj["starter"]) {
            // if code reached this point, we're not overriding. only modify object if "activity" is not a starter(starters hold duration data for display), effectively cutting off certain events

            // checking whether next activity is a starter
            let nextTime = "",
                next_ampm = ampm,
                current_duration = duration - (i * 0.5);
            // calculate next time
            if (newTime == "12:30") {
                nextTime = "1:00";
            } else {
                nextTime = (numToTime[(timeToNum[newTime] + 0.5)]);
            }
            // flip AM/PM at 12:00
            if (nextTime == "12:00") {
                if (next_ampm == 0) next_ampm = 1;
                else next_ampm = 0;
            } 

            // now i have next time index and its properties
            let next_timeKey = nextTime + '_' + next_ampm;
            let next_obj = thisWeek[event["date"]][next_timeKey];
            // if next is a starter activity, set current object's conflict 
            if (current_duration > 0.5 && next_obj["starter"]) obj["newConflict"] = 1;
            
            if (event["unsatisfied"]) {
                obj["unsatisfied"] = event["unsatisfied"];
                obj["ideal_start"] = event["ideal_start"];
                obj["ideal_ampm"] = event["ideal_ampm"];
                obj["ideal_duration"] = event["ideal_duration"] - (i * 0.5);
            }
            obj["activity"] = event["activity"];
            obj["category"] = event["category"];
            if (i == 0) obj["starter"] = 1;
            obj["duration"] = current_duration;
        } else {
            // when not overriding and you've reached a filled activity, break out of this loop
            break;
        }
    }
    var mod = JSON.stringify(thisWeek);
    fs.writeFile(json, mod, err => {
        if (err) throw err;
    });
}

/*
* for updating mod-feedback.json with conflicts according to feedback json
at this point, feedback & mod-feedback should be the same
*/
function getUFJ(fb_json, modfb_json) {
    const fb = require(fb_json);
    var modfb = require(modfb_json);

    // for 1 activity, it can have many unsatisfied objects but only 1 is starter. we need to erase this activity's times, treating it like brand new event
    for (date in fb) {
        for (time in fb[date]) {
            let event = fb[date][time];
            if (event["starter"] && event["unsatisfied"]) {
                let removedEventDate = modfb[date];
                for (mod_time in removedEventDate) {
                    let removedEvent = removedEventDate[mod_time];
                    if (removedEvent["activity"] == event["activity"]) {
                        removedEvent["unsatisfied"] = 0;
                        removedEvent["ideal_start"] = "";
                        removedEvent["ideal_ampm"] = "";
                        removedEvent["duration"] = 0;
                        removedEvent["starter"] = 0;
                        removedEvent["category"] = "other";
                        removedEvent["ideal_duration"] = 0;
                        removedEvent["newConflict"] = 0;
                        removedEvent["activity"] = "";
                    }
                }
            }
        }
    }
       
    var mod = JSON.stringify(modfb);
    fs.writeFile(modfb_json, mod, err => {
        if (err) throw err;
    });

    for (date in fb) {
        /* given all time fields for a day, if it's a starter unsatisfied or just newConflict event, update the mod_feedback json accordingly
        */
        for (time in fb[date]) {
            let event = fb[date][time];
            if (event["starter"] && event["unsatisfied"]) {
                // turn this unsatisfied event into new event with appropriate time & duration
                let newEvent = event;
                newEvent["start_time"] = event["ideal_start"];
                newEvent["ampm"] = event["ideal_ampm"];
                newEvent["duration"] = event["ideal_duration"];
                console.log(newEvent);
                modifyJson(newEvent, modfb_json,1);
            }
        }
    }

    for (date in fb) {
        for (time in fb[date]) {
            let event = fb[date][time];
            if (event["newConflict"]) {
                modifyJson(event, modfb_json,1);
            }
        }
    }
}

/* 
*convert current json to .txt file based on ML format
*for each line in file, assume correct string format:
meaning:    [date day time ampm event]
type:       [string int float int int]
values:     [yyyy-mm-dd 0-6 12.0-11.5 0/1 0-4]
days: 0-mon 1-tues 2-wed 3-thurs 4-fri 5-sat 6-sun 
events: 0-class 1-lunch 2-nap 3-study 4-dinner 5-other 
*/

// use this for actual_data json & mod_feedback json
function storeData(json, textfile_name) {
    const thisWeek = require(json);

    for (date in thisWeek) {
        // confirm current week's dates
        // console.log(date);
        for (time in thisWeek[date]) {
            let dict = thisWeek[date][time];
            let line = dict["date"] + ' ' + dayToNum[dict["day"]] + ' ' + timeToNum[dict["start_time"]] + ' ' + ampmToNum[dict["ampm"]] + ' ' + catToNum[dict["category"]];
            fs.appendFile(textfile_name, line + '\n', err => {
                if (err) throw err;
            });
        }
    }
}

/* SCENARIO for using the above functions
* user inputs regular event to calendar -> write to actual data/feedback/modfeedback json
* user adds new activity in feedback table that conflicts with current event -> update feedback json and mod feedback json to allow this conflict and display it
* user says they're unsatisfied with an existing activity in feedback table and sets an ideal time that conflicts with another event -> update feedback json and mod feedback json to allow this conflict and display
* update mod feedback json to resolve these conflicts(done right before generating user_feedback.txt).
*/

// ----------------------------------------------------------------------------------
// Start dealing with user input

app.use(express.urlencoded());

app.get("/", function(req, res){
	res.sendFile(path + 'login.html')
});

// form-data is in HTTP req.body
app.post('/', function(req, res) {
	console.log("LOG: New activity added.");
    console.log(req);
    /* HTML form details: name type values
    date string yyyy-mm-dd
    weekday string 0-6 = Mon-Fri
    hour number 0-12
    minute string 0/1 = 00/30
    ampm string 0/1 = AM/PM
    duration number 0-inf
    activity string 0-5 class-other
    name string
    */

	let time = parseInt(req.body.hour) + (parseInt(req.body.minute) * 5);

	let duration = parseInt(req.body.duration);
	let activity = req.body.activity;
    let data_json = "activity_time.json";

    // updating sum hours per category for Charts
	fs.readFile(data_json, function readFileCallback(err, data) {
		if (err) {
			console.log(err);
		} else {
			obj = JSON.parse(data);
			if(activity == 0){
				obj.class += duration;
			}
			else if(activity == 1){
				obj.lunch += duration;
			}
			else if(activity == 2){
				obj.nap += duration;
			}
			else if(activity == 3){
				obj.study += duration;
			}
			else if(activity == 4){
				obj.dinner += duration;
			}
			else if(activity == 5){
				obj.other += duration;
			}
			let json = JSON.stringify(obj);
			fs.writeFile(data_json, json, (err)=>{
				if(err){
					throw err;
				}
			});
		}
	});

    // converting input data into an ICS object to append to ICS calendar
	var ap;
	if(req.body.ampm == 0){
		ap = 0;
	}
	else{
		ap = 12;
	}

	var minute;
	if(req.body.minute=="0"){
		minute = "00";
	}
	else{
		minute = "30";
	}

	var m_start = (parseInt(req.body.hour) + ap) + ':' + minute + ":00";
	var m_end = (parseInt(req.body.hour) + ap + parseInt(req.body.duration)) + ':' + minute + ":00";

	var m_type;

	if(activity == 0){
		m_type = "Class";
	}
	else if(activity == 1){
		m_type = "Lunch";
	}
	else if(activity == 2){
		m_type = "Nap";
	}
	else if(activity == 3){
		m_type = "Study";
	}
	else if(activity == 4){
		m_type = "Dinner";
	}
	else if(activity == 5){
		m_type = "Other";
	}


	let ICS_event = {
		name: req.body.name,
		type: m_type,
		date: req.body.date, 
		start: m_start, 
		end: m_end, 
	};

	fs.exists('preICS.json', function(exists) {
		let obj = {
			ICSEvents: []
		};
		if (exists) {
			fs.readFile('preICS.json', function readFileCallback(err, data) {
				if (err) {
					console.log(err);
				} else {
					obj = JSON.parse(data);
					obj.ICSEvents.push(ICS_event);
					let json = JSON.stringify(obj);
					fs.writeFile('preICS.json', json, (err)=>{
						if(err){
							throw err;
						}
					});
				}
			});
		} 
		else {
			obj.ICSEvents.push(ICS_event)
			let json = JSON.stringify(obj);
			fs.writeFile('preICS.json', json, 'utf8', (err)=>{
				if(err){
					throw err;
				}
			});
		}
	});

    // appending input data to actual_data
	for( i = 0; i < duration * 2; ++i){
		let m_activity = req.body.date + ' ' + req.body.weekday + ' ' + time + ' ' + req.body.ampm + ' ' + req.body.activity;
		time += 0.5;
		if(time == 13){
			time = 1;
		}
		// console.log("LOG: " + m_activity);

		fs.appendFileSync('actual_data.txt', m_activity + '\n', 'utf8', (err)=>{
			if(err){
				throw err;
			}
			else{
				console.log(m_activity);
			}
		});
	}

    // updating feedback_json & mod_feedback json with user inputted event
    // first check that the event is within the current week(that's what the json contains)
        // this is because demo will input events outside of this week
    const fb = require(feedback_j);
    const mod_fb = require(mod_feedback_j);
    var validDate = 0;
    for (date in fb) {
        if (req.body.date == date) {
            validDate = 1;
        }
    }
    if (validDate) {
        var newEvent = {
            "unsatisfied": 0,
            "ideal_start": "",
            "start_time": req.body.hour + ':' + htmlMinute[req.body.minute],
            "ideal_ampm": "",
            "date": req.body.date,
            "duration": req.body.duration,
            "day": htmlDay[req.body.weekday],
            "starter": 0,
            "category": htmlActType[req.body.activity],
            "ampm": htmlAMPM[req.body.ampm],
            "ideal_duration": 0,
            "newConflict":0,
            "activity": req.body.name
        }
        console.log(newEvent);
        modifyJson(newEvent, feedback_j, 0);
        modifyJson(newEvent, mod_feedback_j, 0);
    }
  

    // finish storing data and return to the page
	res.sendFile(path + 'index.html')
});

app.get("/dashboard", function(req, res){
	res.sendFile(path + 'index.html')
});

app.get("/charts", function (req, res) {
	res.sendFile(path + 'charts.html')
});

app.get("/recommendation", function (req, res) {
    // update the tracker text file so the ML system knows to read actual_data.txt
	fs.appendFileSync('tracker.txt', "User has requested recommendation from ML model.", 'utf8', (err)=>{
		if(err){
			throw err;
		}
	});
	res.sendFile(path + 'index.html')
});

app.get("/login", function(req, res){
	res.sendFile(path + 'login.html')
});

app.get("/tables", function (req, res) {
    res.sendFile(path + "tables.html"); 
});

app.post('/tables', function (req, res) {
    console.log(req);
    res.sendFile(path + "tables.html");
});


app.get("/register", function(req, res){
	res.sendFile(path + 'register.html')
});

app.get("/forgot-password", function(req, res){
	res.sendFile(path + 'forgot-password.html')
});

app.get("*", function(req, res){
	res.sendFile(path + '404.html')
});


module.exports = app;
