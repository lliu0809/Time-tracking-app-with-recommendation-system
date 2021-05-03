
const fs = require("fs");

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

var def_json_txt = "./default_json.txt";
var actual_data_j = "./actual_data.json";
var feedback_j = "./feedback.json";
var mod_feedback_j = "./mod_feedback.json";
var acData_txt = "./actual_data.txt";
var fb_txt = "./user_feedback.txt";

// ----------------------------------------------------------------------------------

// START OF LOADING: generate default json txt with json-gen, convert into 3 default jsons
function getDefaultJson(text) {
    fs.readFile(text, function (err, data) {
        if (err) throw err;
        // convert file into json object
        var jsontxt = JSON.parse(data);
        // convert object back to json
        var mod = JSON.stringify(jsontxt);
        // write to file
        fs.writeFile(actual_data_j, mod, err => {
            if (err) throw err;
        });
        fs.writeFile(feedback_j, mod, err => {
            if (err) throw err;
        });
        fs.writeFile(mod_feedback_j, mod, err => {
            if (err) throw err;
        });
    });
}

// ----------------------------------------------------------------------------------

// 2+ hour span between 11:30AM-1:30PM is correctly accounted for
var regEvent = {
    "unsatisfied": 0,
    "ideal_start": "",
    "start_time": "11:30",
    "ideal_ampm": "",
    "date": "2020-11-30",
    "duration": 2,
    "day": "Monday",
    "starter": 0,
    "category": "lunch",
    "ampm": "AM",
    "ideal_duration": 0,
    "newConflict":0,
    "activity": "ate at a buffet"
};

// added event comes before and pushes existing event start time later
// 11:00AM - 12:00PM
var addPreEventConflict = {
    "unsatisfied": 0,
    "ideal_start": "",
    "start_time": "11:00",
    "ideal_ampm": "",
    "date": "2020-11-30",
    "duration": 1,
    "day": "Monday",
    "starter": 0,
    "category": "nap",
    "ampm": "AM",
    "ideal_duration": 0,
    "newConflict":0,
    "activity": "catch up on sleep"
}
// added event comes after and pushes existing event end time earlier
// 1:00PM - 2:00PM
// then the regEvent should update so that lunch is between 12:00-1:00pm
var addPostEventConflict = {
    "unsatisfied": 0,
    "ideal_start": "",
    "start_time": "1:00",
    "ideal_ampm": "",
    "date": "2020-11-30",
    "duration": 1,
    "day": "Monday",
    "starter": 0,
    "category": "study",
    "ampm": "PM",
    "ideal_duration": 0,
    "newConflict":0,
    "activity": "study for finals"
}

// replicating the above except with user feedback and ideal times
// dinner between 4:00PM - 6:00PM
var regEvent2 = {
    "unsatisfied": 0,
    "ideal_start": "",
    "start_time": "4:00",
    "ideal_ampm": "",
    "date": "2020-11-30",
    "duration": 2,
    "day": "Monday",
    "starter": 0,
    "category": "dinner",
    "ampm": "PM",
    "ideal_duration": 0,
    "newConflict":0,
    "activity": "ate dinner with fam"
};

// ideal time comes before and pushes existing event start time later
// assume they napped 3:00PM -4:00PM
// they wish they napped 2:30PM - 4:30PM
var idealPreConflict = {
    "unsatisfied": 1,
    "ideal_start": "2:30",
    "start_time": "3:00",
    "ideal_ampm": "PM",
    "date": "2020-11-30",
    "duration": 1,
    "day": "Monday",
    "starter": 0,
    "category": "nap",
    "ampm": "PM",
    "ideal_duration": 2,
    "newConflict":0,
    "activity": "need more sleep"
}
// ideal time comes after and pushes existing event end time earlier
// assume they studied 6:00PM -7:00PM
// they wish they studied 5:30PM - 7:30PM
var idealPostConflict = {
    "unsatisfied": 1,
    "ideal_start": "5:30",
    "start_time": "6:00",
    "ideal_ampm": "PM",
    "date": "2020-11-30",
    "duration": 1,
    "day": "Monday",
    "starter": 0,
    "category": "study",
    "ampm": "PM",
    "ideal_duration": 2,
    "newConflict":0,
    "activity": "late night grind"
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

// ----------------------------------------------------------------------------------

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

// ----------------------------------------------------------------------------------

/* SCENARIO
* user inputs regular event to calendar -> write to actual data/feedback/modfeedback json
* user adds new activity in feedback table that conflicts with current event -> update feedback json and mod feedback json to allow this conflict and display it
* user says they're unsatisfied with an existing activity in feedback table and sets an ideal time that conflicts with another event -> update feedback json and mod feedback json to allow this conflict and display
* update mod feedback json to resolve these conflicts(done right before generating user_feedback.txt).

*/

function testScenario() {
    // dashboard: actual activities
    modifyJson(regEvent, actual_data_j, 0);
    modifyJson(regEvent, feedback_j, 0);
    modifyJson(regEvent, mod_feedback_j, 0);
    modifyJson(regEvent2, actual_data_j, 0);
    modifyJson(regEvent2, feedback_j, 0);
    modifyJson(regEvent2, mod_feedback_j, 0);

    // feedback: desired events
    modifyJson(addPreEventConflict, feedback_j, 0);
    modifyJson(addPreEventConflict, mod_feedback_j, 0);
    modifyJson(addPostEventConflict, feedback_j, 0);
    modifyJson(addPostEventConflict, mod_feedback_j, 0);

    // feedback: ideal times
    modifyJson(idealPreConflict, feedback_j, 0);
    modifyJson(idealPreConflict, mod_feedback_j, 0);
    modifyJson(idealPostConflict, feedback_j, 0);
    modifyJson(idealPostConflict, mod_feedback_j, 0);
}

// ! make sure when testing that the example event dates are within this week's dates
// run getDefaultJson, then testScenario, then getUFJ, then storeData all separately
// functions do not know the results of other functions

// getDefaultJson(def_json_txt);
// testScenario();

// storeData(feedback_j, acData_txt);
// call getUFJ to modify mod feedback json, then store data
// getUFJ(feedback_j, mod_feedback_j);
storeData(mod_feedback_j, fb_txt);
