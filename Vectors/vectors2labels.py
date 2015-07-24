#!/usr/bin/python -B                                                                      

"""
Map word2vec vectors to labels stored in a '|' separated file.
Output vectors in libsvm format ready for training/testing.
"""

NEGLABEL = 4 
NEGEXAMPLES = 2000
DIMENSIONS = 200
CUI2TUI = '/Users/dima/Boston/DictLookup/cui2tui.txt'
TUI2SEMTYPE = '/Users/dima/Boston/DictLookup/tui2semtype.txt'
VECTORS = '/Users/dima/Boston/Vectors/SemType/pmc-w2v-200k.txt'

def read_cui_tui_map():
  """ """
  
  # key: word, value: set of tuis
  tui_lookup = {}

  for line in open(CUI2TUI):
    if line.startswith('CUI'):
      continue # header
    cui, word, tui = line.strip().split('|')
    if not tui_lookup.has_key(word):
      tui_lookup[word] = set()
    tui_lookup[word].add(tui)

  return tui_lookup

def read_tui_semtype_map():
  """ """

  # key: tui, value: semantic type
  tui2semtype = {}
  
  for line in open(TUI2SEMTYPE):
    if line.startswith('#'):
      continue # comments
    tui, semtype = line.strip().split('|')
    tui2semtype[tui] = semtype

  return tui2semtype

def libsvm_vector(word2vec_vector):
  """Convert a list of numbers to a libsvm vector"""
  
  vector = []
  for index, value in enumerate(word2vec_vector):
    pair = "%s:%s" % (index + 1, value) # index must start from 1
    vector.append(pair)

  return ' '.join(vector)    

if __name__ == "__main__":
  """Form a training set by mapping vectors to word semantic types"""

  label_lookup = read_labels()
  
  for line in open(VECTORS):
    elements = line.split()
    word = elements[0]
    if label_lookup.has_key(word):
      label_set = label_lookup[word]
      if len(label_set) > 1:
        continue # skip polysemous words
      vector = libsvm_vector(elements[1:DIMENSIONS + 1])
      label = TOINT[list(label_set)[0]]
      print label, vector

  # sample N words with no semantic type
  sampled_so_far = 0
  for line in open(VECTORS):
    elements = line.split()
    word = elements[0]

    if len(elements) < DIMENSIONS:
      continue # skip word2vec model header
    if sampled_so_far >= NEGEXAMPLES:
      break

    if not label_lookup.has_key(word):
      sampled_so_far = sampled_so_far + 1
      vector = libsvm_vector(elements[1:DIMENSIONS + 1])
      print NEGLABEL, vector
