import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer as stemmer
import random
import json
import torch
from nn_model import NeuralNet
from nlp_helper import bow, tokenize

device = torch.device('cpu')
with open('intents.json', 'r') as intent_data:
    intents = json.load(intent_data)

FILE = "data.pth"
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Chatly"
print("Let's chat! (type 'quit' to exit)")
while True:
    sentence = input("You: ")
    if sentence == "quit":
        break

    sentence = tokenize(sentence)
    X = bow(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
    else:
        print(f"{bot_name}: I do not understand...")

'''
class ChatBot():
    def __init__(self, name):
        print("=== Initiating", name, "===")
        self.name = name

if __name__ == "__main__":
    ai = ChatBot(name="Chatly")
'''