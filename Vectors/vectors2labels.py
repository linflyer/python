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
VECTORS = '/Users/dima/Boston/Vectors/SemType/100K/pmc-w2v-100k.txt'
# VECTORS = '/Users/dima/Boston/Vectors/Models/PubMed-w2v.txt'

def read_cui_tui_map():
  """ """
  
  # key: word, value: set of tuis
  cui2tui = {}

  for line in open(CUI2TUI):
    if line.startswith('CUI'):
      continue # header
    cui, word, tui = line.strip().split('|')
    if not cui2tui.has_key(word):
      cui2tui[word] = set()
    cui2tui[word].add(tui)

  return cui2tui

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

def get_cui_semtype_map():
  """ """

  cui2tui = read_cui_tui_map()
  tui2semtype = read_tui_semtype_map()

  # key: word, value: set ofsemantic types
  cui2semtype = {}

  for cui, tuis in cui2tui.items():
    semtypes = set()
    for tui in tuis:
      semtype = tui2semtype[tui]
      semtypes.add(semtype)
    cui2semtype[cui] = semtypes

  return cui2semtype

def make_libsvm_vector(word2vec_vector):
  """Convert a list of numbers to a libsvm vector"""
  
  vector = []
  for index, value in enumerate(word2vec_vector):
    pair = "%s:%s" % (index + 1, value) # index must start from 1
    vector.append(pair)

  return ' '.join(vector)    

if __name__ == "__main__":
  """Form a training set by mapping vectors to word semantic types"""

  cui2semtype = get_cui_semtype_map()

  print cui2semtype['ms']
  exit()
 
  for line in open(VECTORS):
    elements = line.split()
    word = elements[0]
    if cui2semtype.has_key(word):
      label_set = cui2semtype[word]
      if len(label_set) > 1:
        continue # skip polysemous words
      vector = make_libsvm_vector(elements[1:DIMENSIONS + 1])
      label = list(label_set)[0]
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
    if not cui2semtype.has_key(word):
      sampled_so_far = sampled_so_far + 1
      vector = libsvm_vector(elements[1:DIMENSIONS + 1])
      print NEGLABEL, vector
