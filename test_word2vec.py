# from phrase_vector import PhraseVector
from gensim.models import KeyedVectors

# result_file  = 'test/test_result-2.txt'
corpus_file  = 'corpus/questions/corpus.txt'

model = KeyedVectors.load('models/word2vec.model')
print(model.wv.most_similar(positive=["vagina"]))

# f = open(result_file,"w+")

# # s1 = 'dok apakah normal jika wanita orgasme tapi tidak mengeluarkan cairan kental seperti sperma'
# s1 = 'dok saya sedang hamil 9 minggu bolehkah saya minum air kelapa muda kelapa hijau terima kasih'
# phraseVector1 = PhraseVector(model, s1)
# for sentence in open(corpus_file):
#     phraseVector2 = PhraseVector(model, sentence)
#     similarityScore  = phraseVector1.CosineSimilarity(phraseVector2.vector)
#     if similarityScore >= 0.95:
#         print("sentence-1: {}".format(s1))
#         print("sentence-2: {}".format(sentence.replace('\n','')))
#         print("Similarity Score: {}\r\n\r\n".format(similarityScore))

#         f.write("sentence-1: {}\r\n".format(s1))
#         f.write("sentence-2: {}\r\n".format(sentence.replace('\n','')))
#         f.write("Similarity Score: {}\r\n\r\n".format(similarityScore))
# f.close()
