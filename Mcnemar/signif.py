#!/usr/bin/python -B                                                                      

import math
from scipy import stats

"""

Compute a contingency table as described in 
wikipedia article for McNemar test. Then compute
McNemar test statistic and its probability.

   test2
t   + -
e + a b
s - c d
t
1

"""

def contingency(correct1, incorrect1, correct2, incorrect2):
  """Make a contingency table. See wikipedia article for details."""

  a = len(correct1.intersection(correct2))
  b = len(correct1.intersection(incorrect2))
  c = len(incorrect1.intersection(correct2))
  d = len(incorrect1.intersection(incorrect2))

  chisquare = math.pow(abs(b - c) - 1, 2) / (b + c)
  prob = stats.chisqprob(chisquare, 1)
  
  print 'chisquare value: %5.3f' % chisquare
  print 'probability by chance: %5.3f%%' % (prob * 100)

  # significant if prob < 5%
  return prob

def read(filename):
  """Return sets of correctly and incorrectly classified instances"""
  
  correct = set()
  incorrect = set()
  for index, line in enumerate(open(filename)):
    if line.strip() == 'correct':
      correct.add(index)
    if line.strip() == 'incorrect':
      incorrect.add(index)
  
  return correct, incorrect

def main():
  """ """

  correct1, incorrect1 = read('before.txt')
  correct2, incorrect2 = read('after.txt')
  contingency(correct1, incorrect1, correct2, incorrect2)
      
if __name__ == "__main__":

  main()
