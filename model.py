import pickle
import string
import nltk
from nltk.corpus import PlaintextCorpusReader

class LanguageModel:
    CORPUS_PATH  = 'data/'

    def __init__(self, is_read=False, corpus_path=CORPUS_PATH):
        if is_read is False:
            self.words = self.__read_corpus(corpus_path)
            self.freq_dist = self.__freq_dist(self.words)
            self.bigram_cfreq_dist = self.__bigram_conditional_freq_dist(self.words)
            self.bigram_cprob_dist = self.__bigram_conditional_prob_dist(self.bigram_cfreq_dist)
        else:
            self.words = pickle.load( open( "pickled/_words.p", "rb" ) )
            self.freq_dist = pickle.load( open( "pickled/_freq_dist.p", "rb" ) )
            self.bigram_cfreq_dist = pickle.load( open( "pickled/_bigram_cfreq_dist.p", "rb" ) )
            self.bigram_cprob_dist = pickle.load( open( "pickled/_bigram_cprob_dist.p", "rb" ) )

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

    def __bigram_conditional_freq_dist(self, words):
        return nltk.ConditionalFreqDist(nltk.bigrams(words))

    def __bigram_conditional_prob_dist(self, cfreq_dist):
        return nltk.ConditionalProbDist(cfreq_dist, nltk.MLEProbDist)

    def unigram_prob(self, word):
        return self.freq_dist[word] / len(self.words)

    def sentence_prob(self, sentence):
        words = sentence.split()
        probability = 1
        for idx, word in enumerate(words):
            if idx == len(words) - 1:
                break
            probability *= self.bigram_cprob_dist[word].prob(words[idx + 1])

        probability *= self.unigram_prob(words[0])
        return probability

    def save(self):
        pickle.dump( self.words, open( "pickled/_words.p", "wb" ) )
        pickle.dump( self.freq_dist, open( "pickled/_freq_dist.p", "wb" ) )
        pickle.dump( self.bigram_cfreq_dist, open( "pickled/_bigram_cfreq_dist.p", "wb" ) )
        pickle.dump( self.bigram_cprob_dist, open( "pickled/_bigram_cprob_dist.p", "wb" ) )
