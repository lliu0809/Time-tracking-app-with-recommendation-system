import torch.nn as nn
import torch
from torch.autograd import Variable
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np


# logistic regression model
def createlogisticRegression():

    linear = nn.Linear(2, 1, bias = True)
    sigmoid = nn.Sigmoid()
    model_logistic_regression = nn.Sequential(linear, sigmoid)
    return model_logistic_regression


# relu classifier
def createReLUModel():
    linear = nn.Linear(2, 1, bias = True)
    sigmoid = nn.Sigmoid()
    relu = nn.ReLU()
    model_relu = nn.Sequential(relu, linear, sigmoid)
    return model_relu