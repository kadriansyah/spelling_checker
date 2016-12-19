import pickle
import string
import nltk
from nltk.corpus import PlaintextCorpusReader
from enum import Enum
from functools import reduce

class LanguageModel:
    CORPUS_PATH  = 'corpus/article/'

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
        translator = str.maketrans({key: ' ' for key in string.punctuation})
        words = [z.translate(translator).lower().strip() for z in wordlists.words(wordlists.fileids())]
        words = ' '.join(words)
        return [x.strip().lower() for x in words.split() if x.strip()] # Hapus seluruh empty char pada list

    def __freq_dist(self, words):
        return nltk.FreqDist(words)

    def __cond_freq_dist(self, words):
        return nltk.ConditionalFreqDist(nltk.bigrams(words))

    def __cond_prob_dist(self, cond_freq_dist):
        # # MLEProbDist is the unsmoothed probability distribution
        # return nltk.ConditionalProbDist(cond_freq_dist, nltk.MLEProbDist)

        # # LaplaceProbDist is the add-one smoothed ProbDist
        # return nltk.ConditionalProbDist(cond_freq_dist, nltk.LaplaceProbDist, bins=len(self.words))

        # # WittenBellProbDist
        # return nltk.ConditionalProbDist(cond_freq_dist, nltk.WittenBellProbDist, bins=len(self.words))

        # # SimpleGoodTuringProbDist
        # return nltk.ConditionalProbDist(cond_freq_dist, nltk.SimpleGoodTuringProbDist, bins=1e5)

        # LidstoneProbDist
        return nltk.ConditionalProbDist(cond_freq_dist, nltk.LidstoneProbDist, gamma=0.2, bins=len(self.words))

    def unigram_prob(self, word):
        return self.freq_dist[word] / len(self.words)

    def sentence_prob(self, sentence):
        prob_list = [self.cond_prob_dist[a].prob(b) for (a,b) in nltk.bigrams(sentence.split())]
        return reduce(lambda x,y:x*y, prob_list)

    def save(self):
        pickle.dump( self.words, open( "pickled/_words.p", "wb" ) )
        pickle.dump( self.freq_dist, open( "pickled/_freq_dist.p", "wb" ) )
        pickle.dump( self.cond_freq_dist, open( "pickled/_cond_freq_dist.p", "wb" ) )
        pickle.dump( self.cond_prob_dist, open( "pickled/_cond_prob_dist.p", "wb" ) )
