import math
from collections import Counter

# label rules
def entropy_rule(label: str) -> float:
  if len(label) == 0:
    return 0.0

  counts = Counter(label)
  entropy = 0.0
  for count in counts.values():
    prob = count / len(label)
    entropy += -(prob * math.log2(prob))
  
  return entropy

def digit_count_rule(label: str) -> float:
  if len(label) == 0:
    return 0.0

  digit_count = sum(char.isdigit() for char in label)
  digit_ratio = digit_count / len(label)
  return digit_ratio / 0.25

def consonant_run_rule(label: str) -> float:
  if len(label) == 0:
    return 0.0

  vowels = ['a', 'e', 'i', 'o', 'u']
  vowel_count = sum(1 for char in label if char in vowels)
  vowel_ratio = vowel_count / len(label)
  consonant_ratio = 1 - vowel_ratio 

  max_run = 0
  curr_run = 0
  for char in label:
    if char.isalpha() and char not in vowels:
      curr_run += 1
      max_run = max(max_run, curr_run)
    else:
      curr_run = 0
  
  run_score = max_run/ 4
  vowel_score = consonant_ratio / 0.85

  return max(vowel_score, run_score)

def character_set_rule(label: str) -> float:
  if len(label) == 0:
    return 0.0
  if label.startswith('xn--'):
    return 1.0
  valid_chars = 'abcdefghijklmnopqrstuvwxyz0123456789-_'
  invalid_chars = sum(1 for char in label if char not in valid_chars)
  return invalid_chars / len(label)


# helper function for going through all labels
def worst_label_score(domain: str, rule) -> float:
  labels = domain.split(".")
  if not labels:
    return 0.0
  return max(rule(label) for label in labels)

# domain rules
def length_rule(domain: str) -> float:
  labels = domain.split(".")
  max_label_len = 0
  for label in labels:
    max_label_len = max(max_label_len, len(label))
  return max(len(domain) / 30, max_label_len / 25)

def label_count_rule(domain: str) -> float:
  return (len(domain.split(".")) / 4)