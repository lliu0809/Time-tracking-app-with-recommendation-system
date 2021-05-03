# CS 130 Project (Fall 2020)

**Team Members:** Roshni Iyer, Liunian Harold Li, Winnie Sun, Lihang Liu, Ethan Huang

Final Project Report: https://docs.google.com/document/d/1WcsC_o5rISezvUI-Ac_4q-TDt0p-kW8HNKbh1_J7uPE/edit

To start the app:

1. check if node has already been installed (if not, install node: https://nodejs.org/en/download/package-manager/):

```sh
$ node -v
```

2. download the repo with Git or SVN

3. change the absolute path in line 15 in app.js

4. start the server

```sh
$ node local.js
```

3. access http://localhost:8000/ in browser

Toy Data & ML system-related information is indicated by blue text.
UI & UI Data Store Backend-related information is indicated by red text.

**Application Class Structure Hierarchy Overview**

-   **Class torch.nn.Module**
    -   **Class Model:** Defines our NN model (MLP, LSTM)
    -   **Class TrainModelConfig:** Defines config params used for training our model
-   **Class DataGen:** Generates toy data used esp. for different test scenarios to evaluate the effectiveness of the ML System
-   **Class DataInput:** Retrieves and parses stored data input and passes it to the ML system for generating recommendations
    -   **Class Event:** Creates Events from the data, the data format that the ML System parses the data. Performs dimensionality reduction of the raw data using an encoding process, a format that is amenable to the ML System
        -   **Class GetEvent:** Getter functions to get certain data examples (x & y)
    -   **Class MakeRecommendation:** Uses the ML System predictions to generate more user friendly / understandable data in the form of prediction 1 & 2 (see below)
-   **Class GUI:** Superclass of all pages, shares event information & display functionality across subclasses
-   **Class Dashboard:** User input activities and the calendar displays user’s schedule and ML recommendations
-   **Class Charts:** Graphs user events based on category & duration in bar & donut chart
-   **Class Login:** Gives user access to the time tracking app
-   **Class Register:** Enables user to create account
-   **Class Backend:** Simple abstraction of file storage & retrieval
-   **Class EventInput:** Stores user event information and provides methods on how to process & retrieve user input

Testing:

ML model with Toy Data

1. Run ML model tests for each of the user data patterns by specifying: type = "cooccurrence" #'cooccurrence', 'always_occurring', 'exclusive', 'noisy_situation' (dafault = cooccurrence)
2. Run python data-gen.py
3. In train.py, specify: config.type == "mlp" #"mlp", "lstm" to run MLP or LSTM model
4. Run python train.py

Server-side feedback implementation
\*\* Goal: be able to generate default events for each time slot in json files for the current week, store json objects that represent user-inputted activities in json files, and conver them into .txt files for the ML

1. Navigate to "data_transfer_demo"
2. Run "python ./json-gen.py" to get current week's default json file as "default_json.txt"
3. Open "test.js".
   Scroll to line 111 to see sample events and get familiar with structure.
   Refer to line 406 for the scenario that these functions would be used if the feedback table worked.
4. Make sure each function call besides "getDefaultJson(def_json_txt);" is commented.
   Run test.js (i used VScode, right clicked and "run code" not sure if you need to use node) to generate the 3 default json files.
5. Comment getDefaultJson and uncomment "testScenario();". Run test.js
   This adds every event object from #3 to the jsons.
   Open actual_data.json to see how regEvent & regEvent2 are recorded based on duration.
   Tip: Ctrl-F the activity names
   "ate at a buffet" -> in all 3 jsons
   "catch up on sleep" -> not in actual_data.json
   "study for finals" -> not in actual_data.json
   "ate dinner with fam" -> in all 3 jsons
   "need more sleep" -> not in actual_data.json
   "late night grind" -> not in actual_data.json
6. Comment testScenario and uncomment storeData(feedback_j, acData.txt); Run test.js
   This will output "actual_data.txt" with every single event in the json file, in the desired format.
7. Comment storeData(feedback_j, acData.txt) and uncomment getUFJ(feedback_j, mod_feedback_j); Run test.js
   This modifies the mod_feedback.json such that activities that were marked "unsatisfied" and given ideal start time & durations became recorded as new events in the correct time slot.
   It correctly overrides other events that used to be in that time slot(refer back to event objects from #3)
   It also correctly deals with new ideal activities that user would've added to the feedback table. If there were time conflicts, it would also override the activity that was there.
8. Comment getUFJ, uncomment the last line, and run test.js
   This converts mod_feedback.json to the desired user_feedback.txt format, where all user input that marked an activity as unsatisfied or created a new ideal activity would correctly be created as a text file.
