import os

from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

def main():
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 2
    prefix_length = 7

    # create object
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)

    # load dictionary
    dictionary_path = os.path.join(os.path.dirname(__file__), "corpus/dictionary/dictionary.txt")
    # dictionary_path = os.path.join(os.path.dirname(__file__), "corpus/symspellpy/frequency_dictionary_en_82_765.txt")
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return

    # lookup suggestions for single-word input strings
    input_term = "bangeeet"  # misspelling
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_edit_distance_dictionary)
    max_edit_distance_lookup = 2
    suggestion_verbosity = Verbosity.CLOSEST  # TOP, CLOSEST, ALL
    suggestions = sym_spell.lookup(input_term, suggestion_verbosity, max_edit_distance_lookup)
    # display suggestion term, term frequency, and edit distance
    for suggestion in suggestions:
        print("{}, {}, {}".format(suggestion.term, suggestion.distance, suggestion.count))

    # # lookup suggestions for multi-word input strings (supports compound splitting & merging)
    # input_term = ("Malam dok,saya rini dari TSM.saya sekarang lg hamil 9bln,HPLnya 2 minggu lagi.sekarang saya mengalami wasir trs ada agak2 bercak darah gitu.Apakah berbahaya")
    # # max edit distance per lookup (per single word, not per whole input string)
    # max_edit_distance_lookup = 2
    # suggestions = sym_spell.lookup_compound(input_term, max_edit_distance_lookup)
    # # display suggestion term, edit distance, and term frequency
    # for suggestion in suggestions:
    #     print("{}, {}, {}".format(suggestion.term, suggestion.distance, suggestion.count))

if __name__ == "__main__":
    main()