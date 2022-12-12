import numpy as np
import json
import random
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from nlp_helper import bow, tokenize, stem
from nn_model import NeuralNet

with open('intents.json', 'r') as f:
    intents = json.load(f)

# loop through intents and tokenize into arrays
# make xy pairs for tokens and tags
all_words = []
tags = []
xy = []
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

# stem words and return as lower
ignore = ['!', '@', '.', '?', '$']
all_words = [stem(w) for w in all_words if w not in ignore]
# clean and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# create training data
x_train = []
y_train = []
for (sentence_pattern, tag) in xy:
    bag = bow(sentence_pattern, all_words)
    x_train.append(bag)
    label = tags.index(tag)
    y_train.append(label)

x_train = np.array(x_train)
y_train = np.array(y_train)

# hyper-parameters
total_epochs = 1000
batch_size = 8
learn_rate = 0.001
input_size = len(x_train[0])
hidden_size = 8
output_size = len(tags)

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=2)

device = torch.device('cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learn_rate)

# train it
for epoch in range(total_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device)
        outputs = model(words)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{total_epochs}], Loss: {loss.item():.4f}')

print(f'final loss: {loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'Training complete. File saved to {FILE}')