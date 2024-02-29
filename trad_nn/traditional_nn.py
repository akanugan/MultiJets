import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import hist
from hist import Hist

torch.cuda.is_available()

import matplotlib.pyplot as plt
#import pandas as pd


#dataset is 94312
X = torch.load("x_1750_tensor.pd")
Y = torch.load("y_1750_tensor.pd")


ratio = 0.93

X_train = X[:round(len(X)*ratio)]
Y_train = Y[:round(len(Y)*ratio)]
X_test = X[round(len(X)*ratio):]
Y_test = Y[round(len(Y)*ratio):]


print("Loaded tensors, training data size " + str(len(X_train)) + ", test data size " + str(len(X_test)) )

model = nn.Sequential(
    nn.Linear(80, 64),
    nn.ReLU(),
    nn.Linear(64, 20),
    nn.ReLU(),
    nn.Linear(20, 20),
    nn.ReLU(),
    nn.Linear(20, 10),
    nn.Sigmoid()
)

def masym_model(X):
    asym = []
    y_val = np.zeros(10)
    for i in range(0, len(X), 8):
        asym.append(X[i])
    best_val = asym[0]
    best_index = 0
    for j in range(1,len(asym)):
        if(asym[j] < best_val):
            best_val = asym[j]
            best_index = j
    y_val[best_index] = 1
    return y_val

loss_fn = nn.BCELoss()  # binary cross entropy
optimizer = optim.Adam(model.parameters(), lr=0.001)

n_epochs = 75
batch_size = 20

losses = []

for epoch in range(n_epochs):
    for i in range(0, len(X_train), batch_size):
        Xbatch = X_train[i:i+batch_size]
        y_pred = model(Xbatch)
        ybatch = Y_train[i:i+batch_size]
        loss = loss_fn(y_pred, ybatch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f'Finished epoch {epoch}, latest loss {loss}')
    losses.append(float(loss))

with torch.no_grad():
    y_pred = model(X_test)

nn_rounded = y_pred.argmax(1)

m = torch.zeros(y_pred.shape).scatter(1, nn_rounded.unsqueeze(1), 1.0)

accuracy = (y_pred.round() == Y_test).float().mean()
print(f"Accuracy {accuracy}")

y_masym_pred = [masym_model(k) for k in X_test]
y_masym_pred = torch.tensor(y_masym_pred, dtype=torch.float32)


accuracy = (y_masym_pred.round() == Y_test).float().mean()
print(f"Mass Asymmetry Minimization Accuracy {accuracy}")

print("Plotting Loss vs Epochs...")

fig, ax = plt.subplots()
plt.plot(losses,color='orange')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.savefig("plots/loss.png")


print("Plotting Triplet Mass...")
M = torch.load("m_1750_tensor.pd")
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

plt.savefig("plots/inv_mass.png")


