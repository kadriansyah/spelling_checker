from phrase_vector import PhraseVector
from gensim.models import KeyedVectors

model = KeyedVectors.load('models/word2vec.model')

s1 = 'dok apakah normal jika wanita orgasme tapi tidak mengeluarkan cairan kental seperti sperma'
s2 = 'saya tanya apakah normal wanita orgasme dan tidak mengeluarkan cairan kental'

phraseVector1 = PhraseVector(model, s1)
phraseVector2 = PhraseVector(model, s2)
similarityScore  = phraseVector1.CosineSimilarity(phraseVector2.vector)
print("Similarity Score: ", similarityScore)