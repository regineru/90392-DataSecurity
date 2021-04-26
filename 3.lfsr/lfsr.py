import math
from functools import reduce
from operator import xor
from itertools import islice

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
def berlekamp_massey(bits):
  return
"""

class LFSR(object): 

    def __init__(self, poly, state=None):

        self.length = max(poly) 
        self.output = None
        self.feedback = None

        #self.poly = self.p
        self.p = [False for i in range(max(poly)+1)]
        for i in range(len(self.p)):
            if i in poly:
                self.p[i] = True
        self.p.reverse()
        self.p.pop()

        #self.state = self.s
        if state is None: 
            self.s = [True for i in range(max(poly))]
        else: 
            self.s = [i == '1' for i in state]
            print('State:', self.s)
    
    def __iter__(self): 
        return self

    def __next__(self): 
        anded = []
        for i in range(len(self.p)):
          anded.append(self.s[i] and self.p[i])
        fb = reduce(xor, anded)
        self.output = self.s[0]
        self.s.pop(0)
        self.s.append(fb)
        return self.output

    def run_steps(self, N=1): 
        list_of_bool = []
        for i in range(N):
          print(self.__next__())
          list_of_bool.append(self.__next__())
        return list_of_bool 
    
    def cycle(self, state=None): 
        N = (2**self.length)-1
        list_of_bool = self.run_steps(N)
        return list_of_bool

    def __str__(self, list):
      for b in islice(list, 8):
        print(f'{b:d}', end='')

lfsr = LFSR([3, 1])
print(2*"\n",lfsr.cycle())
print("\n")


"""
class BerlekampMassey():
  return
"""