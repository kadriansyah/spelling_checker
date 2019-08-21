import os
import random
import multiprocessing
import numpy as np

import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.WARNING)

from gensim.models import Word2Vec
from phrase_vector import PhraseVector

corpus_file  = 'corpus/questions/corpus.txt'
test_file    = 'test/test-data.txt'
class Sentences(object):
    def __init__(self, corpus):
        self.corpus = corpus
 
    def __iter__(self):
        for line in open(self.corpus):
            yield line.replace('\n','').split()

print("prepating training data...")
sentences = Sentences(corpus_file)

# cores = multiprocessing.cpu_count() # Count the number of cores in a computer
# model = Word2Vec(min_count=20,
#                  window=2,
#                  size=300,
#                  sample=6e-5, 
#                  alpha=0.03, 
#                  min_alpha=0.0007, 
#                  negative=20,
#                  workers=cores-1)
# model.build_vocab(sentences)
# model.train(sentences, total_examples=model.corpus_count, epochs=50, report_delay=1)
# model.save('models/word2vec.model')

steps = 100
# build the model
# model = Word2Vec(sentences, size=300, window=10, min_count=1, workers=5, alpha=0.025, min_alpha=0.025, iter=1)
cores = multiprocessing.cpu_count() # Count the number of cores in a computer
model = Word2Vec(min_count=1,
                 window=5,
                 size=300,
                 sample=6e-5, 
                 alpha=0.03, 
                 min_alpha=0.0007, 
                 negative=20,
                 iter=1,
                 workers=cores-1)
model.build_vocab(sentences)
for epoch in range(steps):
    print('\ntraining epoch {:d} ...'.format(epoch))
    model.train(sentences, total_examples=model.corpus_count, epochs=model.iter, report_delay=1)

    print(model.wv.most_similar(positive=["asma"]))

    model.alpha -= 0.002  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay

    # print(model.wv.accuracy(test_file))
model.save('models/word2vec.model')

