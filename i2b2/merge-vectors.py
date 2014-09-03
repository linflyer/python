#!/usr/bin/python -B                                     

"""
Some patients have vectors in multiple patient files. 
Make a single vector for those patients but summing the individual ones.
"""

import glob

patient_files = "/Users/dima/Boston/Data/Phenotype/T2D/Pei/trial3/*_pt.txt"

def patients_in_multiple_files():
  """List of patient num(s) that have vectors in multiple files"""

  patient2vector = {}
  for file in glob.glob(patient_files):
    for line in open(file):
      if line[0].isdigit():
        elements = line.strip().split(',')
        patient_num = elements[0]
        if(patient2vector.has_key(patient_num)):
          print patient_num
          # print file
          # print patient2vector[patient_num]
          # print line.strip()
          # print
        else:
          patient2vector[patient_num] = line.strip()

def batches_with_same_patients():
  """ """

  patient2batch = {}
  for file in glob.glob(patient_files):
    for line in open(file):
      if line[0].isdigit():
        elements = line.strip().split(',')
        patient_num = elements[0]
        if(patient2batch.has_key(patient_num)):
          patient2batch[patient_num].append(file)
        else:
          patient2batch[patient_num] = [file]

  batches_containing_same_patients = set()
  for key in patient2batch.keys():
    if len(patient2batch[key]) > 1:
      batches_containing_same_patients.update(patient2batch[key])

  print batches_containing_same_patients

def sum(vector1, vector2):
  """Sum two vectors represented as lists. Element 0 is patient_num."""

  if(vector1[0] != vector2[0]):
    print 'patient_num mismatch!'
    return

  result = [vector1[0]]
  for element1, element2 in zip(vector1[1:], vector2[1:]):
    result.append(element1 + element2)

  return result

if __name__ == "__main__":

  batches_with_same_patients()
