import nltk
from nltk.corpus import PlaintextCorpusReader
import string

CORPUS_PATH  = 'data/article/'

def readCorpus():
    wordlists = PlaintextCorpusReader(CORPUS_PATH, '.*', encoding='latin-1')

    # The method translate() returns a copy of the string in which all characters have been translated
    # using table (constructed with the maketrans() function in the str module),
    # optionally deleting all characters found in the string deletechars.
    translator = str.maketrans({key: None for key in string.punctuation})
    words = [z.translate(translator).strip() for z in wordlists.words(wordlists.fileids())]

    # Hapus seluruh empty char pada list
    return [x.strip().lower() for x in words if x.strip()]

def freqDist(words):
    return nltk.FreqDist(nltk.trigrams(words))

def kneserNeyProbDist(freqDist):
    return nltk.KneserNeyProbDist(freqDist)

def sentenceProb(sentence, estimator):
    prob_sum = 1
    ngrams = nltk.trigrams(sentence.split())
    for pair in ngrams:
        prob_sum *= estimator.prob(pair)
    return prob_sum
