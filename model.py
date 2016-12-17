import pickle
import string
import nltk
from nltk.corpus import PlaintextCorpusReader
from enum import Enum

class LanguageModel:
    CORPUS_PATH  = 'data/clean/'

    def __init__(self, load=False, corpus_path=CORPUS_PATH):
        if load is False:
            self.words = self.__read_corpus(corpus_path)
            self.freq_dist = self.__freq_dist(self.words)
            self.cond_freq_dist = self.__cond_freq_dist(self.words)
            self.cond_prob_dist = self.__cond_prob_dist(self.cond_freq_dist)
        else:
            self.words = pickle.load(open("pickled/_words.p", "rb"))
            self.freq_dist = pickle.load(open("pickled/_freq_dist.p", "rb"))
            self.cond_freq_dist = pickle.load(open("pickled/_cond_freq_dist.p", "rb"))
            self.cond_prob_dist = pickle.load(open("pickled/_cond_prob_dist.p", "rb"))

    def __read_corpus(self, corpus_path):
        wordlists = PlaintextCorpusReader(corpus_path, '.*', encoding='latin-1')

        # The method translate() returns a copy of the string in which all characters have been translated
        # using table (constructed with the maketrans() function in the str module),
        # optionally deleting all characters found in the string deletechars.
        translator = str.maketrans({key: None for key in string.punctuation})
        words = [z.translate(translator).strip() for z in wordlists.words(wordlists.fileids())]

        # Hapus seluruh empty char pada list
        return [x.strip().lower() for x in words if x.strip()]

    def __freq_dist(self, words):
        return nltk.FreqDist(words)

    def __cond_freq_dist(self, words):
        return nltk.ConditionalFreqDist(nltk.bigrams(words))

    def __cond_prob_dist(self, cond_freq_dist):
        return nltk.ConditionalProbDist(cond_freq_dist, nltk.MLEProbDist)

    def __unigram_prob(self, word):
        return self.freq_dist[word] / len(self.words)

    def sentence_prob(self, sentence):
        words = sentence.split()
        prob  = self.__unigram_prob(words[0])
        for ii in range(1, len(words) - 1):
            prob *= self.cond_prob_dist[words[ii]].prob(words[ii + 1])
        return prob

    def save(self):
        pickle.dump( self.words, open( "pickled/_words.p", "wb" ) )
        pickle.dump( self.freq_dist, open( "pickled/_freq_dist.p", "wb" ) )
        pickle.dump( self.cond_freq_dist, open( "pickled/_cond_freq_dist.p", "wb" ) )
        pickle.dump( self.cond_prob_dist, open( "pickled/_cond_prob_dist.p", "wb" ) )
