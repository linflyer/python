#!/usr/bin/python -B           

"""
This script implements the boostrap test for measuring statistical signficance in
the difference between two F1 scores. The implementation is based on the paper:

A Comparison of Statistical Significance Tests for Information Retrieval Evaluation 
by Mark D. Smucker, James Allan, and Ben Carterette

We assume that the observed difference in F scores between two systems A and B
is a random sample from a distribution with zero mean (null hypothesis). We then
estimate the probability of obtaining the difference that we observed or larger 
given that the null hypothesis is true.

The input to this script is two files containing the test results for the two
systems. The results are stored one per line and each line is one of the following:

{tp, fp, tn, fn}

The script outputs the observed difference in F1 scores and the p value.
"""

from __future__ import division                                                           
import math, random
from scipy import stats

base = './'
filea = base + 'a.txt'
fileb = base + 'b.txt'
numsamples = 10000

def sample(list):
  """Sample len(list) list elements with replacement"""

  resample = []
  for _ in range(len(list)):
    resample.append(random.choice(list))

  return resample

def fscore(data):
  """Compute F1 score"""
  
  tp = data.count('tp')
  fp = data.count('fp')
  fn = data.count('fn')
  p = tp / (tp + fp)
  r = tp / (tp + fn)

  return 2 * p * r / (p + r)
  
if __name__ == "__main__":

  # read experiment outcomes for systems A and B
  data = [line.strip() for line in open(filea)]
  datb = [line.strip() for line in open(fileb)]

  # observed F scores and their difference F(B) - F(A)
  experimentfa = fscore(data)
  experimentfb = fscore(datb)
  experimentdiff = experimentfb - experimentfa

  # create bootstrap distribution of F(B) - F(A)
  bootdistrib = []
  for _ in range(numsamples):
    resamplea = sample(data)
    resampleb = sample(datb)
    fa = fscore(resamplea)
    fb = fscore(resampleb)
    bootdistrib.append(fb - fa)

  # shift bootstrap distribution so that its mean is zero
  shifted = []
  mean = sum(bootdistrib) / len(bootdistrib)
  for diff in bootdistrib:
    shifted.append(diff - mean)

  # compute fraction of samples where difference
  # is the same or larger than what we observed
  count = 0
  for diff in shifted:
    if diff >= experimentdiff:
      count = count + 1

  # calculate p value
  pvalue = count / numsamples
  print "F1(A)=%f, F1(B)=%f, F(B)-F(A)=%f, p=%f" % \
        (experimentfa, experimentfb, experimentdiff, pvalue)
