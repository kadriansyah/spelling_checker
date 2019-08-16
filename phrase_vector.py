import math
import numpy as np

class PhraseVector:
	def __init__(self, model, phrase):
		self.model = model
		self.vector = self.PhraseToVec(phrase)
	
	# <summary> Calculates similarity between two sets of vectors based on the averages of the sets.</summary>
	# <param>name = "vectorSet" description = "An array of arrays that needs to be condensed into a single array (vector). In this class, used to convert word vecs to phrases."</param>
	# <param>name = "ignore" description = "The vectors within the set that need to be ignored. If this is an empty list, nothing is ignored. In this class, this would be stop words."</param>
	# <returns> The condensed single vector that has the same dimensionality as the other vectors within the vecotSet.</returns>
	def ConvertVectorSetToVecAverageBased(self, vectorSet, ignore = []):
		if len(ignore) == 0:
			return np.mean(vectorSet, axis = 0)
		else:
			return np.dot(np.transpose(vectorSet),ignore)/sum(ignore)
	
	def PhraseToVec(self, phrase):
		phrase = phrase.lower()
		words_in_phrase = [word for word in phrase.split()]
		vector_set = []
		for word in words_in_phrase:
			try:
				word_vector = self.model[word]
				vector_set.append(word_vector)
			except:
				pass
		return self.ConvertVectorSetToVecAverageBased(vector_set)

	# <summary> Calculates Cosine similarity between two phrase vectors.</summary>
	# <param> name = "otherPhraseVec" description = "The other vector relative to which similarity is to be calculated."</param>
	def CosineSimilarity(self, otherPhraseVec):
		cosine_similarity = np.dot(self.vector, otherPhraseVec) / (np.linalg.norm(self.vector) * np.linalg.norm(otherPhraseVec))
		try:
			if math.isnan(cosine_similarity):
				cosine_similarity=0
		except:
			cosine_similarity=0
		return cosine_similarity