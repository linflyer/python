#!/usr/bin/python -B                                     

"""
Some patients have vectors in multiple patient files. 
Make a single vector for those patients but summing the individual ones.
"""

import glob

patient_files = "/Users/dima/Boston/Data/Phenotype/T2D/Pei/trial3/*_pt.txt"
labels = "/Users/dima/Boston/Data/Phenotype/T2D/Data/labels-original.txt"

def patients_in_multiple_files():
  """List of patient num(s) that have vectors in multiple files"""

  patient2vector = {}
  for file in glob.glob(patient_files):
    for line in open(file):
      if line[0].isdigit():
        elements = line.strip().split(',')
        patient_num = elements[0]
        if(patient2vector.has_key(patient_num)):
          print file
          print patient2vector[patient_num]
          print line.strip()
          print
        else:
          patient2vector[patient_num] = line.strip()

def batches_with_same_patients():
  """Find batches (*_pt.txt files) that have repeating patient vectors"""

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

def remove_repeating_patients_from_labels():
  """Some patients are labeled twice. Remove them."""

  # find duplicate patient_num(s)
  patients = set()
  double_annotated_patients = set()
  for line in open(labels):
    patient_num, label = line.strip().split(',')
    if patient_num in patients:
      double_annotated_patients.add(patient_num)
    else:
      patients.add(patient_num)

  # print non-duplicate patient_num(s) and labels
  for line in open(labels):
    patient_num, label = line.strip().split(',')
    if not patient_num in double_annotated_patients:
      print line.strip()

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

  remove_repeating_patients_from_labels()
