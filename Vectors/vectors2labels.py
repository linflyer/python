#!/usr/bin/python -B                                                                      

"""
Map word2vec vectors to labels stored in a '|' separated file.
Output vectors in libsvm format ready for training/testing.
"""

NEGLABEL = 6
NEGEXAMPLES = 2000
DIMENSIONS = 200
LABELS = '/Users/dima/Boston/Vectors/SemType/pmc-vocab-100k-labels.txt'
VECTORS = '/Users/dima/Boston/Vectors/SemType/pmc-w2v-100k.txt'
TOINT = {'AnatomicalSiteMention':1, 
         'DiseaseDisorderMention':2, 
         'MedicationMention':3, 
         'ProcedureMention':4, 
         'SignSymptomMention':5}

def read_labels():
  """Read label file into a dictionary"""

  # key: word, value = set of semantic types
  label_lookup = {} 

  for line in open(LABELS):
    word, label = line.strip().split('|')
    if not label_lookup.has_key(word):
      label_lookup[word] = set()
    label_lookup[word].add(label)

  return label_lookup

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
