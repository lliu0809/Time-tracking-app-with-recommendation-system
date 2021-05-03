// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function loadJSON(callback) {   
  var xobj = new XMLHttpRequest();
  xobj.overrideMimeType("application/json");
  xobj.open('GET', '../../activity_time.json', true);
  xobj.onreadystatechange = function () {
    if (xobj.readyState == 4 && xobj.status == "200") {
        callback(JSON.parse(xobj.responseText));
    }
    };
    // xobj.responseText is empty for some reason
    xobj.send(null);
    return xobj;
}

// within this variable's function lies the json object
var test = loadJSON(function (json) {
    
    // Pie Chart Example
    var ctx = document.getElementById("myPieChart");

    var myPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["Class", "Lunch", "Nap", "Study", "Dinner", "Other"],
            datasets: [{
                data: [json["class"], json["lunch"], json["nap"], json["study"], json["dinner"], json["other"]],
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#cce7e8', '#1c2ed1'],
                hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#cce7e8'],
                hoverBorderColor: "rgba(234, 236, 244, 1)",
            }],
        },
        options: {
            maintainAspectRatio: false,
            tooltips: {
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10,
            },
            legend: {
                display: false
            },
            cutoutPercentage: 80,
        },
    });
  
});
