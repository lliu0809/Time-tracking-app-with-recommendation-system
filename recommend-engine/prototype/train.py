import torch
from torch.autograd import Variable
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np
# from models import *

import torch.nn as nn
import torch
from torch.autograd import Variable
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np
from torch.utils.data import DataLoader
from tqdm import tqdm
from collections import Counter


# logistic regression model
def createlogisticRegression():
    linear = nn.Linear(3, 1, bias=True)
    sigmoid = nn.Sigmoid()
    model_logistic_regression = nn.Sequential(linear, sigmoid)
    return model_logistic_regression


# relu classifier
def createReLUModel():
    linear = nn.Linear(3, 1, bias=True)
    sigmoid = nn.Sigmoid()
    relu = nn.ReLU()
    model_relu = nn.Sequential(relu, linear, sigmoid)
    return model_relu


#### Create toy data

global event_dict
event_dict = {
    0: "class",
    1 : "lunch",
    2 : "nap",
    3 : "study",
    4 : "dinner",
    5 : "other"
}

def GetKey(val, dictA):
   for key, value in dictA.items():
      if val == value:
         return key
      return "key doesn't exist"

"""Defines our NN model (MLP, LSTM)"""
class Model(nn.Module):
    def __init__(self, config):
        super(Model, self).__init__()
        self.config = config
        if config.type == "mlp":
            self.linear = nn.Linear(config.hid_dim, config.large_hid_dim, bias=True)
            relu = nn.ReLU()
            self.second_linear = nn.Linear(config.large_hid_dim, config.class_num, bias=True)
            self.model = nn.Sequential(self.linear, relu, self.second_linear)
        elif config.type == "lstm":
            self.lstm = nn.LSTM(input_size=config.hid_dim + 1, hidden_size=config.large_hid_dim, num_layers=config.layer, batch_first=True)
            self.second_linear = nn.Linear(config.large_hid_dim, config.class_num, bias=True)

    """Forward propagation step"""
    def forward(self, input):
        if config.type == "mlp":
            output = self.model(input)
        elif config.type == "lstm":
            output, (hn, cn) = self.lstm(input)
            #print(output.size())
            output = self.second_linear(output)
            #print(output.size())
            output = output[:, -1]
        return output


"""Defines config params used for training our model"""
class TrainModelConfig(nn.Module):
    def __init__(self):
        super(TrainModelConfig, self).__init__()
        self.type = "mlp"
        self.hid_dim = 3
        self.large_hid_dim = 10
        self.class_num = 6

        self.total_step = 500
        self.batch_size = 20
        self.epoch = 1100

        #self.type = "lstm"
        self.large_hid_dim = 10
        self.layer = 2
        #self.batch_size = 2

        self.lr = 0.0001

"""Retrieves and parses stored data input and passes it to the ML model for generating recommendations"""
class DataInput():
    def __init__(self, feedback_filename, eval_filename):
        self.file_feedback = open(feedback_filename, "r")
        self.file_eval = open(eval_filename, "r")
        self.lines_feedback = self.file_feedback.readlines()
        self.lines_eval = self.file_eval.readlines()

    """Given input file, converts each data example to Events which will be stored in a dataset to be directly used by the NN model"""
    def createEventsData(self, myList, fileLines):
        # Assuming the date is sorted by date
        same_date_data = []
        tmp_date = ""
        for line in fileLines:
            data = line.split(' ')
            date = data[0]
            weekday = int(data[1])
            start_time = float(data[2])
            am_pm = int(data[3])
            event_type = int(data[4].split('\n')[0])

            include_in_eval = 0

            if len(data) > 5:
                include_in_eval = int(data[5].strip())

            if date != tmp_date:
                if len(same_date_data) > 0:
                    same_date_data = sorted(same_date_data, key=DataInput.key_for_sort_event)
                    myList.extend(same_date_data)
                same_date_data = []
                tmp_date = date

            same_date_data.append(
                Event(date=date, weekday=weekday, start_time=start_time, am_pm=am_pm, event_type=event_type, include_in_eval = include_in_eval))
        return myList
    
    @staticmethod
    def key_for_sort_event(event):
        return event.am_pm * 1000 + event.start_time

"""Creates Events from the data, the data format that the ML model parses the data. Performs dimensionality reduction of the raw 
data using an encoding process, a format that is amenable to the ML model"""
class Event(DataInput):
    def __init__(self, date, weekday, start_time, am_pm, event_type, include_in_eval = True):
        self.date = date
        self.weekday = weekday
        self.start_time = start_time
        self.am_pm = am_pm
        self.event_type = event_type
        self.include_in_eval = include_in_eval
        self.lr = 0.0001

    """Creates a tensor from event data: 

torch.Tensor([self.weekday, self.start_time, self.am_pm])"""
    def to_tensor(self):
        return torch.Tensor([self.weekday, self.start_time, self.am_pm])

    # def to_label(self):
    #     return torch.LongTensor([event_dict[self.event_type]])

    """Creates a tensor with the data label, which corresponds to the class category of the event type (see event_type above)"""
    def to_label_direct(self):
        return torch.LongTensor([self.event_type])

    """X = torch.Tensor([self.weekday, self.start_time, self.am_pm])

    Y = torch.LongTensor([self.event_type])"""
    @staticmethod
    def convert_events_into_include_in_eval(events):
        return [event.include_in_eval for event in events]

    @staticmethod
    def date_to_integer(date):
        year, month, day = [int(i) for i in date.split("-")]
        return 10000*year + 100*month + day

    @staticmethod
    def convert_events_into_vectors(events, normalize=True):
        x = []
        y = []
        for event in events:
            x.append(event.to_tensor())
            y.append(event.to_label_direct())
            # y.append(event.to_label())

        x = torch.stack(x, dim=0)
        y = torch.stack(y, dim=0)

        if normalize:
            #means = x.mean(dim=0, keepdim=True)
            #stds = x.std(dim=0, keepdim=True)
            means = torch.Tensor([3.5, 6, 0.5]).unsqueeze(0)
            stds = torch.Tensor([7, 12, 1]).unsqueeze(0)
            x = (x - means) / stds

        return x, y

"""Getter functions to get certain data examples (x & y)"""
class GetEvent(Event, torch.utils.data.Dataset):
    def __init__(self, x, y, use_lstm = False, include_in_eval = None):
        self.x = x
        self.y = y
        self.include_in_eval = include_in_eval

        self.use_lstm = use_lstm
        
        if use_lstm:
            all_data = []
            all_data_y = []
            include_in_eval = [] if self.include_in_eval else None
            y_as_feature = None
            means = y.float().mean(dim=0, keepdim=True)
            stds = y.float().std(dim=0, keepdim=True)
            y_as_feature = (y.float() - means) / stds

            for index in range(len(x) - 49):
                all_data.append(torch.cat((x[index:index+48], y_as_feature[index:index+48]), dim = -1))
                all_data_y.append(y[index + 48])
                if self.include_in_eval is not None:
                    include_in_eval.append(self.include_in_eval[index])
            self.x = all_data
            self.y = all_data_y
            self.include_in_eval = include_in_eval

    """Returns size of data x"""
    def __len__(self):
        return len(self.x)

    """Gets particular training example (data x) and corresponding label"""
    def __getitem__(self, index):
        if self.include_in_eval is not None:
            return self.x[index], self.y[index], self.include_in_eval[index]
        return self.x[index], self.y[index]

"""Uses the ML model predictions to generate more user friendly / understandable data in the form of prediction 1 & 2 (see below)
"""
class MakeRecommendation(DataInput):
    def __init__(self, num_classes, train_data, eval_data, eval_label_pred):
        self.train_data = train_data
        self.eval_data = eval_data
        self.label_lst = eval_label_pred  # list
        self.num_classes = num_classes

    """Predict the duration of the activity the user prefers to
# spend each day and notify the user if that duration is not being met.
"""
    def prediction1(self):
        train_x, train_y = Event.convert_events_into_vectors(self.train_data)

        file_user_feedback = open("user_feedback_day_count.txt", "r")
        file_eval = open("eval_data_day_count.txt", "r")

        for line in file_user_feedback:
            user_feedback_day_count = int(line.split()[0]) // 7
        for line in file_eval:
            eval_day_count = int(line.split()[0]) // 7


        # user preferred data
        train_y_unique = train_y.unique(sorted=True)
        train_y_unique_count = torch.stack([(train_y == x_u).sum() for x_u in train_y_unique])

        # user predicted data
        eval_y_unique = sorted(Counter(self.label_lst).keys())
        eval_y_unique_count = sorted(Counter(self.label_lst).values())

        print(train_y_unique_count)
        print(eval_y_unique_count)


        for i in range(max(len(train_y_unique), len(eval_y_unique))):
            if (i < len(train_y_unique)):
                weekly_train_event = train_y_unique_count[i] // user_feedback_day_count
                try:
                    pos = eval_y_unique.index(train_y_unique[i])
                    weekly_eval_event = eval_y_unique_count[pos] // eval_day_count
                    self.compare(weekly_train_event, weekly_eval_event, train_y_unique[i])
                except:
                    weekly_eval_event = 0
                    self.compare(weekly_train_event, weekly_eval_event, train_y_unique[i])
            else: # i > len(train_y_unique)
                if (eval_y_unique[i] not in train_y_unique):
                    weekly_train_event = 0
                    weekly_eval_event = eval_y_unique_count[i] // eval_day_count
                    self.compare(weekly_train_event, weekly_eval_event, eval_y_unique[i])

        return

    def compare(self, trainCount, testCount, eventType):
        if (trainCount > testCount):
            print("Spend less time on activity: " + event_dict[eventType.item()] + '\n')
            print("Aim to spend around " + str(testCount // 2) + "hrs weekly")
        if (trainCount < testCount):
            print("Spend more time on activity: " + event_dict[eventType.item()] + '\n')
            print("Aim to spend around " + str(testCount // 2) + "hrs weekly")



global config
config = TrainModelConfig()

torch.manual_seed(10)

train_data = []
eval_data = []

data_input = DataInput("/Users/harold/Personal/Project/course_project/cs130/cs130-proj/recommend-engine/prototype/user_feedback.txt", "/Users/harold/Personal/Project/course_project/cs130/cs130-proj/recommend-engine/prototype/eval_data.txt")
train_data = data_input.createEventsData(train_data, data_input.lines_feedback)
eval_data = data_input.createEventsData(eval_data, data_input.lines_eval)
train_x, train_y = Event.convert_events_into_vectors(train_data)

train_dataset = GetEvent(train_x, train_y, use_lstm=config.type == "lstm")
train_loader = DataLoader(
    train_dataset, num_workers=0,
    collate_fn=lambda x: x,
    batch_size=config.batch_size,
    shuffle=True
)

eval_x, eval_y = Event.convert_events_into_vectors(eval_data)
include_in_eval = Event.convert_events_into_include_in_eval(eval_data)

eval_dataset = GetEvent(eval_x, eval_y, use_lstm=config.type == "lstm", include_in_eval = include_in_eval)
eval_loader = DataLoader(
    eval_dataset, num_workers=0,
    collate_fn=lambda x: x,
    batch_size=config.batch_size,
    shuffle=False
)

model = Model(config)


def train(model):
    optimizer = torch.optim.Adam(model.parameters(), lr=config.lr)
    cost_fn = torch.nn.CrossEntropyLoss(ignore_index=-1)

    for epoch in range(config.epoch):
        all_loss = 0.0
        for batch in tqdm(train_loader):
            x, y = zip(*batch)

            x = torch.stack(x, dim=0)
            y = torch.stack(y, dim=0).squeeze(-1)

            prob = model(x)
            func = torch.nn.LogSoftmax()
            prob = func(prob)

            prob = prob.view(-1, prob.size(-1))
            y = y.view(-1)
            loss = cost_fn(prob, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            all_loss += loss.item()

        print("epoch {} Train loss: ".format(epoch), all_loss / len(train_loader))
        evaluate(model)

eval_label_pred=[]
def evaluate(model):
    correct_counter = 0
    all_counter = 0


    protocal = "mark_only" #if config.type == "lstm" else None

    for batch in eval_loader:
        x, y, include_in_eval = zip(*batch)

        x = torch.stack(x, dim=0)
        y = torch.stack(y, dim=0).squeeze(-1)
        include_in_eval = torch.LongTensor(include_in_eval)
        prob = model(x)
        eval_label_pred.extend(prob.argmax(-1).tolist())

        if protocal == "mark_only":
            y[include_in_eval != 2] = 0
            #print("yy", y)
            #print(prob.argmax(-1))
            
            correct_counter += ((prob.argmax(-1) == y) * (y != 0)).sum().item()
            all_counter += (y.view(-1) != 0).long().sum().item()
        else:
            correct_counter += (prob.argmax(-1) == y).sum().item()
            all_counter += len(y.view(-1))
    print("Eval acc: ", correct_counter / all_counter)


train(model)
evaluate(model)
#MakeRecommendation(6, train_data, eval_data, eval_label_pred=eval_label_pred).prediction1()