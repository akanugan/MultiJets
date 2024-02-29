import argparse

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

torch.cuda.is_available()

import matplotlib.pyplot as plt
#import pandas as pd

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

f = open(args.title + "/model_info.txt", "a")

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

print("",file=f)
print(model, file=f)
print("",file=f)


print("Loaded tensors, training data size " + str(len(X_train)) + ", test data size " + str(len(X_test)) )
print("Training data size " + str(len(X_train)) + ", test data size " + str(len(X_test)), file=f )
print("",file=f)


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

loss_fn = nn.BCELoss()  # binary cross entropy
optimizer = optim.Adam(model.parameters(), lr=0.001)

n_epochs = 1000
batch_size = 20

min_loss, stale_epochs = 100.00, 0

losses = []

for epoch in range(n_epochs):
    batch_loss = []
    for i in range(0, len(X_train), batch_size):
        Xbatch = X_train[i:i+batch_size]
        y_pred = model(Xbatch)
        ybatch = Y_train[i:i+batch_size]
        loss = loss_fn(y_pred, ybatch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        batch_loss.append(loss.item())
            # Forward pass on validation set.
        output = model(X_test)

        val_loss = loss_fn(output, Y_test)

            # Monitor the loss function to prevent overtraining.
        if stale_epochs > 20:
            break

        if val_loss.item() - min_loss < 0:
            min_loss = val_loss.item()
            stale_epochs = 0
            torch.save(model.state_dict(), args.title + "/pytorch_model_best.pth")
        else:
            stale_epochs += 1

      
    print(f'Finished epoch {epoch}, latest loss {loss}')
    losses.append(float(np.mean(batch_loss)))

print("Trained for " +str(epoch) + " epochs",file=f)
print('',file=f)


print("Plotting Loss vs Epochs...")

fig, ax = plt.subplots()
plt.plot(losses,color='orange')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.savefig(args.title + "/plots/loss.png")


f.close()
