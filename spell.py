# based on http://norvig.com/spell-correct.html

import os
import re
import csv
from collections import Counter

NEWLINE = '\n'
SKIP_FILES = {'cmds'}
CORPUS_PATH  = 'corpus/'

def read_files(path):
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
        for file_name in file_names:
            if file_name not in SKIP_FILES:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    lines = []
                    f = open(file_path, encoding='latin-1')
                    for line in f:
                        lines.append(line)
                    f.close()
                    content = NEWLINE.join(lines)
                    yield file_path, content

def words(path):
    words = []
    for file_name, text in read_files(path):
        print("process data => "+ file_name)
        words += re.findall(r'\w+', text.lower())
    return words

WORDS = Counter(words(CORPUS_PATH))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) | known(edits1(word)) | known(edits2(word)) | known(edits1Expanded(word)) | {word})

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    # deletes    = [L + R[1:]               for L, R in splits if R]
    # transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    # replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    # return set(deletes + transposes + replaces + inserts)
    return set(inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def edits1Expanded(word):
    return (e3 for e1 in edits1(word) for e2 in edits1(e1) for e3 in edits1(e2))
