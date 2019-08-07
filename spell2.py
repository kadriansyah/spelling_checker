# based on http://norvig.com/spell-correct.html

import os
import re
import csv
import string
import pickle
from collections import Counter
import model
from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

class SpellCorrector:

    NEWLINE = '\n'
    SKIP_FILES = {'cmds'}
    CORPUS_PATH  = 'corpus/questions/'

    __control_dict = {'yg':'yang'}

    def __init__(self, load=False, corpus_path=CORPUS_PATH):
        if load is False:
            self.words = self.__words(corpus_path)
            self.counter = self.__counter(self.words)
            self.model = model.LanguageModel(corpus_path=corpus_path)
        else:
            self.words = pickle.load(open("pickled/_spell_words.p", "rb"))
            self.counter = pickle.load(open("pickled/_spell_counter.p", "rb"))
            self.model = model.LanguageModel(load=True)

        self.candidates_dict = {}

        # maximum edit distance per dictionary precalculation
        max_edit_distance_dictionary = 2
        prefix_length = 7

        # create object
        self.sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
        # load dictionary
        dictionary_path = os.path.join(os.path.dirname(__file__), "corpus/dictionary/dictionary.txt")
        # dictionary_path = os.path.join(os.path.dirname(__file__), "corpus/symspellpy/frequency_dictionary_en_82_765.txt")
        term_index = 0  # column of the term in the dictionary text file
        count_index = 1  # column of the term frequency in the dictionary text file
        if not self.sym_spell.load_dictionary(dictionary_path, term_index, count_index):
            print("Dictionary file not found")
            return

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

    def candidates(self, word, debug=False):
        "Generate possible spelling corrections for word."
        if self.candidates_dict.get(word):
            return self.candidates_dict[word]
        else:
            # max edit distance per lookup
            # (max_edit_distance_lookup <= max_edit_distance_dictionary)
            max_edit_distance_lookup = 2
            suggestion_verbosity = Verbosity.CLOSEST  # TOP, CLOSEST, ALL
            suggestions = self.sym_spell.lookup(word, suggestion_verbosity, max_edit_distance_lookup)

            # cache it
            if SpellCorrector.__control_dict.get(word) != None:
                candidates_0 = (self.__known([word]) | self.__known(self.__edits1(word)) | self.__known(self.__edits2(word)) | self.__known(self.__edits3(word)) | {SpellCorrector.__control_dict.get(word)} | {word})
            else:
                candidates_0 = (self.__known([word]) | self.__known(self.__edits1(word)) | self.__known(self.__edits2(word)) | self.__known(self.__edits3(word)) | {word})
            candidates_1 = set(suggestion.term for suggestion in suggestions)
            candidates = candidates_0.union(candidates_1)

            # print(candidates)

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

    def save(self, python2=False):
        if python2 is False:
            pickle.dump( self.words, open( "pickled/_spell_words.p", "wb"))
            pickle.dump( self.counter, open( "pickled/_spell_counter.p", "wb"))
            self.model.save()
        else:
            pickle.dump( self.words, open( "pickled/_spell_words.p", "wb"), protocol=2)
            pickle.dump( self.counter, open( "pickled/_spell_counter.p", "wb"), protocol=2)
            self.model.save()

    # TODO: implement mechanism to calculate lambda for interpolation
    def __trigram_interpolation(self, w1, w2, w3):
        lambda1 = 0.75
        lambda2 = 0.20
        lambda3 = 0.05
        return (lambda1 * self.model.sentence_prob(w1 +' '+ w2 +' '+ w3)) + (lambda2 * self.model.sentence_prob(w2 +' '+ w3)) + (lambda3 * self.model.unigram_prob(w3))

    # TODO: implement mechanism to calculate lambda for interpolation
    def __bigram_interpolation(self, w1, w2):
        lambda1 = 0.80
        lambda2 = 0.20
        return (lambda1 * self.model.sentence_prob(w1 +' '+ w2)) + (lambda2 * self.model.unigram_prob(w2))

    def validate(self, sentence, debug=False):
        # The method translate() returns a copy of the string in which all characters have been translated
        # using table (constructed with the maketrans() function in the str module),
        # optionally deleting all characters found in the string deletechars.
        translator = str.maketrans({key: ' ' for key in string.punctuation})
        words = [token.translate(translator).strip() for token in sentence.lower().split()]
        words = ' '.join(words)
        words =  [x.strip().lower() for x in words.split() if x.strip()] # Hapus seluruh empty char pada list

        valid = []
        for idx, word in enumerate(words):
            if word in self.words:
                valid.append(word.lower())
            else:
                candidates = self.candidates(word.lower())
                if  idx == 0 :
                    max_word = max([w for w in candidates], key=lambda word: self.model.unigram_prob(word))
                    valid.append(max_word)
                    if debug:
                        print('candidates for '+ word +': '+ str(candidates) +', max prob word is '+ max_word.lower())

                elif idx == 1:
                    max_word = max([w for w in candidates], key=lambda word: self.__bigram_interpolation(valid[0], word))
                    valid.append(max_word)
                    if debug:
                        print('candidates for '+ word +': '+ str(candidates) +', max prob word is '+ max_word.lower())

                else:
                    max_word = max([w for w in candidates], key=lambda word: self.__trigram_interpolation(valid[idx - 2], valid[idx - 1], word))
                    valid.append(max_word)
                    if debug:
                        print('candidates for '+ word +': '+ str(candidates) +', max prob word is '+ max_word.lower())

        return ' '.join(valid)
