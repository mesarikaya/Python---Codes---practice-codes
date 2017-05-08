# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 12:00:24 2017

@author: sarikaya.me
"""

from functools import reduce

def find_all(sum_dig, digs):
  ps = parts(sum_dig, digs)
  return [len(ps), value(ps[0]), value(ps[-1])] if ps else []

def value(xs): return reduce(lambda a, b: 10*a + b, xs, 0)

def parts(sum_dig, digs, p=1):
  if sum_dig < p: return []
  if digs == 1: return [[sum_dig]] if sum_dig < 10 else []
  a = []
  for i in range(p, 10):
    xss = parts(sum_dig - i, digs - 1, i)
    print("xss is: ", xss)
    if xss:
      for xs in xss: a.append([i] + xs)
    print(a)
  return a


import time
start = time.time()
print(find_all(10, 4))
end = time.time()
print(end - start)