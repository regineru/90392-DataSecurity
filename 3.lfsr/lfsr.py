import math
from functools import reduce
from operator import xor
from itertools import islice


def bin_to_int(fist_bin):
  return int("".join(str(x) for x in fist_bin), 2)

def int_to_bin(int_numb, N):
  binary = [1 if digit == '1' else 0 for digit in bin(int_numb)[2:]]
  return [0 for i in range(N - len(binary))] + binary



def lfsr_generator(poly, state=None):  
  if state is None: 
    s = [True for i in range(max(poly)+1)]
  else: 
    s = [i == '1' for i in state] #Gir True for i==1 ikkesant
  p = [False for i in range(max(poly)+1)]
  for i in range(len(p)):
    if i in poly:
      p[i] = True
  p.reverse()
  p.pop()
  while True: 
    b = s[0]
    anded = []
    for i in range(len(p)):
      anded.append(s[i] and p[i])
      fb = reduce(xor, anded)
    s.pop(0)
    s.append(fb)  
    yield b

"""
lfsr = lfsr_generator([3,1,0], state="111")
for b in islice(lfsr, 8):
    print(f'{b:d}', end='')
"""


"""
==============================
"""
import numpy as np

def berlekamp_massey(bits):
  N = len(bits)
  P = [0 for i in range(N)]
  P[N-1] = 1
  m = 0
  Q = [0 for i in range(N)]
  Q[N-1] = 1 
  r = 1

  for t in range(N):
    anded = []
    x_r = [0 for i in range(N)]

    #check negative indexing
    for j in range(m+1):

      P_inverted = P[::-1]
      anded.append(P_inverted[j] and bits[t-j])
      d = reduce(xor, np.array(anded))

    if d == 1: 
      if 2 * m <= t:
        R = P
        x_r[N-r-1] = 1
        Qx_r = bin_to_int(Q) * bin_to_int(x_r)
        P_int = bin_to_int(P)
        P_int = np.bitwise_xor(P_int, Qx_r)

        P = int_to_bin(P_int, N)
        Q = R
        m = t + 1 - m
        r = 0
      else: 
        x_r[N-r-1] = 1
        Qx_r = bin_to_int(Q) * bin_to_int(x_r)
        P_int = bin_to_int(P)
        P_int = np.bitwise_xor(P_int, Qx_r)

        P = int_to_bin(P_int, N)

    r = r + 1

  return P[::-1][:m+1]

def bin_to_int(fist_bin):
  return int("".join(str(x) for x in fist_bin), 2)

def int_to_bin(int_numb, N):
  binary = [1 if digit == '1' else 0 for digit in bin(int_numb)[2:]]
  return [0 for i in range(N - len(binary))] + binary

def print_poly(polynomial): 
    if polynomial[0] == 1:
        result = '1 + '
    else: 
        result = ''
    for idx,i in enumerate(polynomial[1:]):
        if i == 1: 
            result += 'x^{}'.format(idx+1)
            if idx != (len(polynomial)-2):
                result += ' + '
    return result

"""
bit = [1, 0, 1, 0, 0, 1, 1, 1]
poly = berlekamp_massey(bit)
print('Final poly: ', print_poly(poly))
"""

"""
==============================
"""

class LFSR(object): 

    def __init__(self, poly, state=None):

        self.length = max(poly) 
        self.output = None
        self.feedback = 0

        #self.poly = self.p
        self.poly = [False for i in range(max(poly)+1)]
        for i in range(len(self.poly)):
            if i in poly:
                self.poly[i] = True
        self.poly.reverse()
        self.poly.pop()

        if state is None: 
            self.state = [True for i in range(max(poly))]
        else: 
          if type(state) is int:
            self.state = int_to_bin(state, max(self.poly))
          self.state = [True if digit == 1 else False for digit in self.state]
    
    def __iter__(self): 
        return self

    def __next__(self): 
        anded = []
        for i in range(len(self.poly)):
          anded.append(self.state[i] and self.poly[i])
        self.feedback = reduce(xor, anded)
        self.output = self.state[0]
        self.state.pop(0)
        self.state.append(self.feedback)
        return self.output

    def run_steps(self, N=1): 
        list_of_bool = []
        for i in range(N):
          list_of_bool.append(self.__next__())
        return list_of_bool 
    
    def cycle(self, state=None): 
        N = (2**self.length)-1
        list_of_bool = self.run_steps(N)
        return list_of_bool

    def __str__(self, list):
      for b in islice(list, 8):
        print(f'{b:d}', end='')

"""
lfsr = LFSR([3, 1], state=0x5)
bitstream = lfsr.cycle()
print(bitstream)
bm_poly = berlekamp_massey(bitstream)
print(print_poly(bm_poly))
"""