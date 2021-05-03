
var addActivity = document.getElementById("add");
addActivity.addEventListener("click", addNewActivity);

function addNewActivity() {
    "use strict";
    
    var tableBody = document.getElementById("dataTable");
    var row = document.createElement("tr");
    var html= [];

    html.push('<input type="date" id="date" name="date"  style="width:150px;">');
    
    // html.push('<select name="weekday" id="weekday" style="font-size: 0.9rem; width: 100px; height: 30px; text-align: center;" ><option value="none"> </option><option value="0">Monday</option><option value="1">Tuesday</option><option value="2">Wednesday</option><option value="3">Thursday</option><option value="4">Friday</option><option value="5">Saturday</option><option value="6">Sunday</option></select>');
   
    html.push('<input id="name" name="name"  style="width: 100px;">');

    html.push('<select name="activity" id="activity" style="font-size: 0.9rem; width: 100px; height: 30px; text-align: center;" ><option value="none"> </option><option value="0">Class</option><option value="1">Lunch</option><option value="2">Nap</option><option value="3">Study</option><option value="4">Dinner</option><option value="5">Other</option></select>');

    html.push('<input style="width: 50px; height: 30px; text-align: center; font-size: 0.9rem;" type="number" id="hour" name="hour" max=12 min=0 > : <select name="minute" id="minute" style="font-size: 0.9rem; width: 50px; height: 30px; text-align: center;"><option value="none"> </option><option value="0">00</option><option value="1">30</option></select>                 <select name="ampm" id="ampm" style="font-size: 0.9rem; width: 50px; height: 30px; text-align: center;"><option value="none"> </option><option value="0">AM</option><option value="1">PM</option></select>');

    html.push('<input type="number" id="duration" name="duration" min=0  style="font-size: 0.9rem;  width: 50px; height: 30px;">');

    for(let i in html){
        var td =document.createElement("td");
   
        td.innerHTML+= html[i];

        row.appendChild(td);
    }

    for(let i =0; i< 3; i++){
        row.appendChild(document.createElement("td"));
    }
    // make the new entry appear first insert child before children.0
    tableBody.children[1].insertBefore(row, tableBody.children[1].children[0]);
    console.log(tableBody.rows);
    console.log(tableBody);
}
                    
// displaying the json data that user inputted
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let json = JSON.parse(this.responseText);
        
        for (date in json) {
            for (time in json[date]) {
                let event = json[date][time];
                // display all events that are starters
                if (event["starter"]) {
                    var tableBody = document.getElementById("dataTable");
                    var row = document.createElement("tr");
                    var eventDetails= [];
                    for (let i = 0; i < 8; i++){
                        var td = document.createElement("td");
                        eventDetails.push(td);
                    }
                    eventDetails[0].innerText = event["date"];
                    eventDetails[1].innerText = event["activity"];
                    eventDetails[2].innerText = event["category"];
                    eventDetails[3].innerText = event["start_time"] + ' ' + event["ampm"];
                    eventDetails[4].innerText = event["duration"];
                    if (event["unsatisfied"]) {
                        // all data is available
                        eventDetails[5].innerHTML += '<div>&#x1F62D</div>';	
                        eventDetails[6].innerText = event["ideal_start"] + ' ' + event["ideal_ampm"];
                        eventDetails[7].innerText = event["ideal_duration"];
                    } else {
                        // add options to make unsatisfied
                        eventDetails[5].innerHTML += '<input type="checkbox">';	
                        eventDetails[6].innerHTML += '<input style="width: 50px; height: 30px; text-align: center; font-size: 0.9rem;" type="number" id="hour" name="hour" max=12 min=0 > : <select name="minute" id="minute" style="font-size: 0.9rem; width: 50px; height: 30px; text-align: center;"><option value="none"> </option><option value="0">00</option><option value="1">30</option></select><select name="ampm" id="ampm" style="font-size: 0.9rem; width: 50px; height: 30px; text-align: center;"><option value="none"> </option><option value="0">AM</option><option value="1">PM</option></select>';	
                        eventDetails[7].innerHTML += '<input type="number" id="duration" name="duration" min=0  style="font-size: 0.9rem;  width: 50px; height: 30px;">';	

                    }
                    for (let i in eventDetails) {
                        row.appendChild(eventDetails[i]);
                    }
                    tableBody.children[1].appendChild(row);                    
                }
            }
        }
    }
};
xhttp.open("GET", "./feedback.json", true);
xhttp.send();


/*
 when clicking tables.html, send the html link
- tables.html loads a .js that uses xmlhttprequest to read feedback_json
   - in here,loop through each object with an activity name and a starter
      - if so, create thread entry will respective input types and append to table id?
      - if unsatisfied, display data. else += innerhtml code 

*/