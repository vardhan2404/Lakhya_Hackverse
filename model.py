from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np
import random

rlk = random.randint


def genPatientData(mean, var, numSamples):
    data = mean*np.ones(numSamples)
    varRange = int(var*mean)
    varData = [random.randint(0, varRange) for _ in range(numSamples)]
    return (data+varData)


def getPatientSeverity(bpVector):
    mn = np.mean(bpVector)
    sd = np.std(bpVector)
    return (sd/mn)


def myPriority(patientSevrity, hospitalDistances, hospitalReputation):
    numOptions = len(hospitalDistances)
    importanceReputation = 0.3
    importanceSeverity = 0.7
    myprior = []
    for i in range(numOptions):
        myprior.append(hospitalDistances[i]/(importanceSeverity *
                       patientSevrity+importanceReputation*hospitalReputation[i]))
    return myprior


def generateLearningData(numData, numOptions):
    X = []
    y = []
    for _ in range(numData):
        distance = [random.uniform(0, 1) for _ in range(numOptions)]
        reputation = [random.uniform(0, 1) for _ in range(numOptions)]
        severity = random.uniform(0, 1)
        priority = myPriority(severity, distance, reputation)
        for i in range(numOptions):
            X.append([severity, distance[i], reputation[i]])
            y.append(priority[i])
    return np.array(X), np.array(y)


def HospitaltoDisease():

    hnames = [["Manipal", "Heart Problem"], ["Fortis", "ENT"], [
        "Appolo", "Psychological"], ["Vydehi", "Heart"], ["Citizen", "General"]]
    return hnames


def getMLPrediction(model, severity, distance, reputation, numOptions):
    myprior = []
    for i in range(numOptions):
        myprior.append(model.predict(
            np.array([severity, distance[i], reputation[i]]).reshape(1, -1))[0])
    return myprior
# Code for testing paient severity computation
# data = genPatientData(80, 0.1, 10)
# print(data)
# severity = getPatientSeverity(data)
# print(severity)


# Code to test priority computation
'''
numOptions = 5
importanceReputation = 0.3
importanceSeverity = 0.7
distance = [random.uniform(0,1) for _ in range(numOptions)]
reputation = [random.uniform(0,1) for _ in range(numOptions)]
sev = 0.7
prior = myPriority(sev, distance, reputation)
print(prior)
'''
numSamples = 100
numOptions = 5
X, y = generateLearningData(numSamples, numOptions)
print(X.shape, y.shape)
model = linear_model.LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
hnames = HospitaltoDisease()
numOptions = 5
distance = [random.uniform(0, 1) for _ in range(numOptions)]
reputation = [random.uniform(0, 1) for _ in range(numOptions)]
severity = 0.7
x = getMLPrediction(model, severity, distance, reputation, numOptions)
