from ast import Num
import math
from functools import reduce
from tkinter import N, W, Y

# 质数判断
def divisors(integer):
  return [i for i in range(2, math.ceil(integer / 2 + 1)) if not integer % i] or '%d is prime' % integer

# 街区行走
def is_valid_walk(walk):
  # if (len(walk)!= 10):
  #   return False
  # info = {
  #  'w': 0,
  #  'e': 0,
  #  'n': 0,
  #  's': 0
  # }
  # for i in walk:
  #   info[i] += 1
  # w, e, n, s = info['w'], info['e'], info['n'], info['s']

  # if (w-e == 0 and n-s == 0):
  #   return True
  # else:
  #   return False

  return len(walk) == 10 and walk.count('n') == walk.count('s') and walk.count('e') == walk.count('w')

# 除重(连续的几个)
def unique_in_order(iterable):
  tag = None
  list = []
  for i in iterable:
    if (tag != i):
      list.append(i)
      tag = i
  return list
    
# 简单二进制
def binary_array_to_number(arr):
  arr.reverse()
  sum = 0
  for idx, val in enumerate(arr):
    sum += val * 2 ** idx
  return sum

# 找到相同字符
def get_word_info(word):
  word_info = {}
  for i in set(word):
    word_info[i] = word.count(i)
  return word_info

def compare(word, aim_info):
  item = get_word_info(word)
  if (len(aim_info) != len(item)):
    return False
  for k, v in aim_info.items():
    if (not k in item):
      return False
    if (item[k] != v):
      return False
  return True

def anagrams(word, words):
  aim_info = get_word_info(word)
  return [i for i in words if compare(i, aim_info)]

# 质数判断
def is_prime(n):
  for i in range(2, math.ceil( n // 2 + 1)):
    if (n % i == 0):
      return False
  return True

def next_prime(n):
  count = n + 1
  while(not is_prime(count)):
    count += 1
  return count

def prime_factors(n):
  prime_list = []
  count = 2   # 质因数
  factor = n  # 剩余数
  str_prime = ''
  while(not is_prime(factor)):
    if (factor % count == 0):
      prime_list.append(count)
      factor /= count
    else:
      count = next_prime(count)
  
  prime_list.append(int(factor))

  unique_list = sorted(set(prime_list))

  for i in unique_list:
    sum = prime_list.count(i) > 1 and ('**' + str(prime_list.count(i))) or ''
    str_prime += '({}{})'.format(i, sum)

  return str_prime

print(prime_factors(7775460))
