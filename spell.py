# based on http://norvig.com/spell-correct.html

import os
import re
import csv
import string
import pickle
from collections import Counter
import model

class SpellCorrector:

    NEWLINE = '\n'
    SKIP_FILES = {'cmds'}
    CORPUS_PATH  = 'data/clean/'

    def __init__(self, load=False, corpus_path=CORPUS_PATH):
        if load is False:
            self.words = self.__words(corpus_path)
            self.counter = self.__counter(self.words)
            self.model = model.LanguageModel()
        else:
            self.words = pickle.load(open("pickled/_spell_words.p", "rb"))
            self.counter = pickle.load(open("pickled/_spell_counter.p", "rb"))
            self.model = model.LanguageModel(load=True)

        self.candidates_dict = {}

    def __read_files(self, path):
        for root, dir_names, file_names in os.walk(path):
            for path in dir_names:
                self.__read_files(os.path.join(root, path))
            for file_name in file_names:
                if file_name not in SpellCorrector.SKIP_FILES:
                    file_path = os.path.join(root, file_name)
                    if os.path.isfile(file_path):
                        lines = []
                        f = open(file_path, encoding='latin-1')
                        for line in f:
                            lines.append(line)
                        f.close()
                        content = SpellCorrector.NEWLINE.join(lines)
                        yield file_path, content

    def __words(self, corpus_path):
        words = []
        for file_name, text in self.__read_files(corpus_path):
            print("process data => "+ file_name)
            words += re.findall(r'\w+', text.lower())
        return words

    def __counter(self, words):
        return Counter(words)

    def __wordProb(self, word):
        "Probability of `word`."
        return self.counter[word] / sum(self.counter.values())

    def correction(self, word):
        "Most probable spelling correction for word."
        return max(self.candidates(word), key=self.__wordProb)

    def candidates(self, word):
        # TODO: save candidates to REDIS, lookup first before generating candidates
        "Generate possible spelling corrections for word."
        if self.candidates_dict.get(word):
            return self.candidates_dict[word]
        else:
            candidates = (self.__known([word]) | self.__known(self.__edits1(word)) | self.__known(self.__edits2(word)) | self.__known(self.__edits3(word)) | {word})

            # cache it
            self.candidates_dict[word] = candidates
            return candidates

    def __known(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.counter)

    def __edits1(self, word):
        "All edits that are one edit away from `word`."
        letters      = 'aiueon'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(inserts)

    def __edits2(self, word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.__edits1(word) for e2 in self.__edits1(e1))

    def __edits3(self, word):
        return (e3 for e1 in self.__edits1(word) for e2 in self.__edits1(e1) for e3 in self.__edits1(e2))

    def save(self):
        pickle.dump( self.words, open( "pickled/_spell_words.p", "wb" ) )
        pickle.dump( self.counter, open( "pickled/_spell_counter.p", "wb" ) )
        self.model.save()

    def validate(self, sentence, debug=False):
        translator = str.maketrans({key: None for key in string.punctuation})
        words = [token.translate(translator).strip() for token in sentence.split()]

        valid = []
        for idx, word in enumerate(words):
            if word in self.words:
                valid.append(word.lower())
            else:
                candidates = self.candidates(word.lower())
                if  idx == 0:
                    max_word = max([w for w in candidates], key=lambda w : self.model.unigram_prob(w))
                    valid.append(max_word)

                    if debug:
                        print('candidates for '+ word +': '+ str(candidates) +', max prob word is '+ max_word.lower())

                elif idx == 1:
                    max_word = max([w for w in candidates], key=lambda w : self.model.sentence_prob(valid[idx - 1] +' '+ w))
                    valid.append(max_word)

                    if debug:
                        print('candidates for '+ word +': '+ str(candidates) +', max prob word is '+ max_word.lower())

                # calculate probability with context (trigrams)
                else:
                    max_word = max([w for w in candidates], key=lambda w : self.model.sentence_prob(valid[idx - 2] +' '+ valid[idx - 1] +' '+ w))
                    valid.append(max_word)

                    if debug:
                        print('candidates for '+ word +': '+ str(candidates) +', max prob word is '+ max_word.lower())

        return ' '.join(valid)
