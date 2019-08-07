import os

from symspellpy.symspellpy import SymSpell  # import the module

CORPUS_FILE  = 'corpus/questions/corpus.txt'
DICT_FILE  = 'corpus/dictionary/dictionary.txt'

def main():
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 2
    prefix_length = 7
    # create object
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    
    # create dictionary using corpus.txt
    if not sym_spell.create_dictionary(CORPUS_FILE):
        print("Corpus file not found")
        return

    f= open(DICT_FILE,"w+")
    for key, count in sym_spell.words.items():
        print("{} {}".format(key, count))
        f.write("{} {} \r\n".format(key, count))
    f.close()

if __name__ == "__main__":
    main()