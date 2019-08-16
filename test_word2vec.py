from phrase_vector import PhraseVector
from gensim.models import KeyedVectors

corpus_file  = 'corpus/questions/corpus.txt'
result_file  = 'test/test_result-1.txt'

model = KeyedVectors.load('models/word2vec.model')

# s1 = 'dok apakah normal jika wanita orgasme tapi tidak mengeluarkan cairan kental seperti sperma'
# s2 = 'dok apakah normal jika wanita orgasme tapi tidak mengeluarkan cairan kental seperti sperma'

# phraseVector1 = PhraseVector(model, s1)
# phraseVector2 = PhraseVector(model, s2)
# similarityScore  = phraseVector1.CosineSimilarity(phraseVector2.vector)
# print("Similarity Score: ", similarityScore)

f = open(result_file,"w+")

s1 = 'dok apakah normal jika wanita orgasme tapi tidak mengeluarkan cairan kental seperti sperma'
# s1 = 'dok saya sedang hamil 9 minggu bolehkah saya minum air kelapa muda kelapa hijau terima kasih'
phraseVector1 = PhraseVector(model, s1)
for sentence in open(corpus_file):
    phraseVector2 = PhraseVector(model, sentence)
    similarityScore  = phraseVector1.CosineSimilarity(phraseVector2.vector)
    if similarityScore >= 0.95:
        print("sentence-1: {}".format(s1))
        print("sentence-2: {}".format(sentence))
        print("Similarity Score: {}\r\n\r\n".format(similarityScore))

        f.write("sentence-1: {}".format(s1))
        f.write("sentence-2: {}".format(sentence))
        f.write("Similarity Score: {}\r\n\r\n".format(similarityScore))
f.close()
