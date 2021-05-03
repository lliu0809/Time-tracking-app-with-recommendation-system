const app = require("./app.js");
const port = process.env.PORT || 8000;
const fs = require("fs");

var def_json_txt = "./default_json.txt";
// var actual_data_j = "./actual_data.json";
var feedback_j = "./feedback.json";
var mod_feedback_j = "./mod_feedback.json";

// START OF LOADING: generate default json txt with json-gen, convert into 3 default jsons
function getDefaultJson(text) {
    fs.readFile(text, function (err, data) {
        if (err) throw err;
        // convert file into json object
        var jsontxt = JSON.parse(data);
        // convert object back to json
        var mod = JSON.stringify(jsontxt);
        // write to file
        // fs.writeFile(actual_data_j, mod, err => {
        //     if (err) throw err;
        // });
        fs.writeFile(feedback_j, mod, err => {
            if (err) throw err;
        });
        fs.writeFile(mod_feedback_j, mod, err => {
            if (err) throw err;
        });
    });
}

// when we run this program, make sure the jsons are reset
getDefaultJson(def_json_txt);

app.listen(port, () => {
   console.log(`Listening on: http://localhost:${port}`);
});