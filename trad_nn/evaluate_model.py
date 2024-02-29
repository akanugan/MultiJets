import argparse

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import hist
from hist import Hist

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Trains a neural network on data processed by the make_tensors script")
parser.add_argument('-t',"--title", help="Title of the directory", default="nn")
args = parser.parse_args()


#dataset is 94312
X = torch.load(args.title + "/x_tensor.pd")
Y = torch.load(args.title + "/y_tensor.pd")

ratio = 0.90

X_train = X[:round(len(X)*ratio)]
Y_train = Y[:round(len(Y)*ratio)]
X_test = X[round(len(X)*ratio):]
Y_test = Y[round(len(Y)*ratio):]

model = nn.Sequential(
    nn.Linear(X_train.size()[1], 64),
    nn.ReLU(),
    nn.Linear(64, 20),
    nn.ReLU(),
    nn.Linear(20, 20),
    nn.ReLU(),
    nn.Linear(20, 10),
    nn.Sigmoid()
)

model.load_state_dict(torch.load(args.title + "/pytorch_model_best.pth"))

f = open(args.title + "/model_info.txt", "a")

def masym_model(X):
    asym = []
    y_val = np.zeros(10)
    for i in range(0, len(X), round(len(X)/10)):
        asym.append(X[i])
    best_val = asym[0]
    best_index = 0
    for j in range(1,len(asym)):
        if(asym[j] < best_val):
            best_val = asym[j]
            best_index = j
    y_val[best_index] = 1
    return y_val




with torch.no_grad():
    y_pred = model(X_test)

nn_rounded = y_pred.argmax(1)

m = torch.zeros(y_pred.shape).scatter(1, nn_rounded.unsqueeze(1), 1.0)

model_accuracy = (y_pred.round() == Y_test).float().mean()
print(f"Accuracy {model_accuracy}")
print(f"Model Accuracy {model_accuracy}",file=f)


y_masym_pred = [masym_model(k) for k in X_test]
y_masym_pred = torch.tensor(y_masym_pred, dtype=torch.float32)


masym_accuracy = (y_masym_pred.round() == Y_test).float().mean()
print(f"Mass Asymmetry Minimization Accuracy {masym_accuracy}")
print(f"Mass Asymmetry Minimization Accuracy {masym_accuracy}",file=f)
print('',file=f)

f.close()

print("Plotting Triplet Mass...")
M = torch.load(args.title + "/m_tensor.pd")
M_train = M[:round(len(M)*ratio)]
M_test = M[round(len(M)*ratio):]


ax = hist.axis.Regular(40, 500, 2500, flow=False, name="x")
cax = hist.axis.StrCategory(["Neural Network", "Mass Asymmetry", "Truth"], name="c")

full_hist = Hist(ax,cax)

truth_rounded = Y_test.argmax(1)
masym_rounded = y_masym_pred.argmax(1)


for i,masses in enumerate(M_test):
    if masses[truth_rounded[i]][0] > masses[[truth_rounded[i]]][1]:
        full_hist.fill(x=masses[truth_rounded[i]][0],c="Truth")
    else:
        full_hist.fill(x=masses[truth_rounded[i]][1],c="Truth")
    if masses[masym_rounded[i]][0] > masses[[masym_rounded[i]]][1]:
        full_hist.fill(x=masses[masym_rounded[i]][0],c="Mass Asymmetry")
    else:
        full_hist.fill(x=masses[masym_rounded[i]][1],c="Mass Asymmetry")
    if masses[nn_rounded[i]][0] > masses[[nn_rounded[i]]][1]:
        full_hist.fill(x=masses[nn_rounded[i]][0],c="Neural Network")
    else:
        full_hist.fill(x=masses[nn_rounded[i]][1],c="Neural Network")

s = full_hist.stack("c")
s.plot()
plt.legend()
plt.xlabel("Invariant Mass of the Heavier of the Triplets [GeV]")
plt.ylabel("")

plt.savefig(args.title + "/plots/inv_mass.png")