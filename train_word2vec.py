import os
import random

from gensim.models import Word2Vec
from phrase_vector import PhraseVector

corpus_file  = 'corpus/questions/corpus.txt'
test_file    = 'corpus/questions/test.txt'
class Sentences(object):
    def __init__(self, corpus):
        self.corpus = corpus
 
    def __iter__(self):
        for line in open(self.corpus):
            yield line.replace('\n','').split()

print("prepating training data...")
sentences = list(Sentences(corpus_file))
random.shuffle(sentences)

model = Word2Vec(size=300, window=10, min_count=1, workers=5, alpha=0.025, min_alpha=0.025, iter=1)
model.build_vocab(sentences)
model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
model.save('models/word2vec.model')

# Testing Similarity
sentence = ' '.join(sentences[0])
print("sentence-1:", sentence)
print("sentence-2:", sentence)
phraseVector1 = PhraseVector(model, sentence)
phraseVector2 = PhraseVector(model, sentence)
similarityScore  = phraseVector1.CosineSimilarity(phraseVector2.vector)
print("Similarity Score: ", similarityScore)

# # build the model
# model = Word2Vec(sentences, size=300, window=10, min_count=1, workers=5, alpha=0.025, min_alpha=0.025, iter=1)
# for epoch in range(10):
#     print('\ntraining epoch {:d} ...'.format(epoch))
#     model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)

#     model.alpha -= 0.002  # decrease the learning rate
#     model.min_alpha = model.alpha  # fix the learning rate, no decay

#     sentence = ' '.join(sentences[0])
#     print("sentence-1:", sentence)
#     print("sentence-2:", sentence)
#     phraseVector1 = PhraseVector(model, sentence)
#     phraseVector2 = PhraseVector(model, sentence)
#     similarityScore  = phraseVector1.CosineSimilarity(phraseVector2.vector)
#     print("Similarity Score: ", similarityScore)

#     # Randomly shuffle data
#     random.shuffle(sentences)

