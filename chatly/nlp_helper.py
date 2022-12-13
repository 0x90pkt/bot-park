import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer as stemmer


def tokenize(sentence):
    # Splits sentence into word, number, or punctuation "tokens"
    return nltk.word_tokenize(sentence)

def stem(word):
    # Cuts the words down into their perceived root
    # Returns as lower
    return stemmer.stem(word.lower())

def bow(token_sentence, words):
    # Returns a bag of words as an array -- "1" if word exists; "0" if it does not
    # stem the words first
    sentence_words = [stem(word) for word in token_sentence]
    # initialize the array
    bag = np.zeros(len(words), dtype=np.float32)
    for indx, w in enumerate(words):
        if w in sentence_words:
            bag[indx] = 1
    return bag