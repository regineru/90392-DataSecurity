#!/usr/bin/env python

'''
implementation of Linear Feedback Shift register (LFSR) and associated
function and algorithms.

Classes
-------
LFSR:
    implementation of a Linear Feedback Shift Register (LFSR).
BerlekampMassey:
    implementation of the Berlekamp-Massey algorithm as streaming algorithm.


Functions
---------
parity(x): 
    computes parity bit for an integer number
reverse(x, nbit=None): 
    reverse the bit order of an integer number
int_to_sparse(integer): 
    transform an integer in is sparse representation
sparse_to_int(sparse): 
    transform a sparse representation of an integer into the integer number
bits_to_int(bits):
    transform a sequence of bits into its integer representation
berlekamp_massey(bits, verbose=False):
    apply the Brlekamp-Massey Algorithm to a bit sequence.

'''

import math
from operator import xor
from functools import reduce
from itertools import compress
from itertools import islice


__version__ = "0.0.2"


def parity(integer):
    ''' compute the parity bit of an integer `x` (int) '''
    return bool(sum(int(b) for b in f'{integer:b}') % 2)


def reverse(x, nbit=None):
    ''' reverse the bit order of the input `x` (int) represented with `nbit` 
    (int) bits (e.g., nbit: 5, x: 13=0b01101 -> output: 22=0b10110) '''
    if nbit is None:
        nbit = math.ceil(math.log2(x))
    return int(f'{x:0{nbit}b}'[::-1][:nbit], 2)


def int_to_sparse(integer):
    ''' transform an integer into the list of indexes corresponding to 1
    in the binary representation (sparse representation)'''
    sparse = [i for i, b in enumerate(f'{integer:b}'[::-1]) if bool(int(b))]
    return sparse


def sparse_to_int(sparse):
    ''' transform a list of indexes (sparse representation) in an integer whose
    binary representation has 1s at the positions corresponding the indexes and 
    0 elsewhere '''
    integer = sum([2**index for index in sparse])
    return integer


def bits_to_int(bits):
    ''' transform a bit sequence (str of 1/0 or list of bool) into an int '''
    integer = sum(1 << i for i, bit in enumerate(bits) if bool(int(bit)))
    return integer

def int_to_bits(integer, nbit=None):
    ''' transform an integer into a bit sequence (list of bool) '''
    if nbit is None:
        nbit = math.ceil(math.log2(integer))
    integer &= (1 << nbit) - 1
    string = f'{integer:0{nbit}b}'[::-1]
    list_of_bool = [bool(int(b)) for b in string]
    return list_of_bool


class LFSR(object):
    '''
    Class implementing a Linear Feedback Shift Register (LFSR)
    
    Attributes
    ----------
    poly: list of int,
        feedback polynomial expressed as list of integers corresponding to
        the degrees of the non-zero coefficients.
    state: int,
        state of the shift register.
    output: bool,
        last shift register output,
    length: int,
        length of the shift register as well as  maximum degree of the feedback
        polynomial.
    
    Methods
    -------
    run_steps(self, N=1)
        Execute multiple LFSR steps
    cycle(self, state=None)
        Execute a full cycle.
    '''
    
    def __init__(self, poly, state=None):
        '''
        Parameters
        ----------
        poly: list of int,
            feedback polynomial expressed as list of integers corresponding to
            the degrees of the non-zero coefficients.
        state: int, optional (default=None)
            shift register initial state.
            If None, state is set to all ones.
        '''
        length = max(poly)
        self._length = length
        self._poly = sparse_to_int(poly) >> 1 # p0 is omitted (always 1)
        
        self._statemask = (1 << length) - 1
        if state is None:
            state = self._statemask
        self.state = state
        
        self._outmask = 1 << (length-1)
        self._output = bool(self._state & self._outmask)
        
        self._feedback = parity(self._state & self._poly) 

    # ==== state ====
    @property
    def state(self):
        # state is re-reversed before being read
        return reverse(self._state, len(self))
    @state.setter
    def state(self, state):
        if not isinstance(state, int):
            raise TypeError('input type is not supported')
#         # ensure seed is in the range [1, 2**m-1]
#         if (state < 1) or (state > len(self)):
#             state = 1 + state % (2**len(self)-2)
        self._state = reverse(state & self._statemask, len(self))

    # ==== length ====
    @property
    def length(self):
        return self._length
    @length.setter
    def length(self, val):
        raise AttributeError('Denied')
    
    # ==== poly ====
    @property
    def poly(self):
        return int_to_sparse((self._poly << 1) | 1)[::-1]
    @poly.setter
    def poly(self, poly):
        raise AttributeError('Denied')

    # ==== output ====
    @property
    def output(self):
        return self._output
    @output.setter
    def output(self, val):
        raise AttributeError('Denied')

    # ==== feedback ====
    @property
    def feedback(self):
        return self._feedback
    @feedback.setter
    def feedback(self, feedback):
        self._feedback = bool(feedback)
    
    
    def __str__(self):
        poly = ' + '.join([
            (f'x^{d}' if d > 1 else ('x' if d==1 else '1')) 
            for d in self.poly
        ])
        string = ', '.join([
            f'poly: "{poly}"',
            f'state: 0x{self.state:0{(self.length+1)//4}x}',
            f'output: {None if self.output is None else int(self.output)}'
        ])
        return string
        
    def __repr__(self):
        return f'LSFR({str(self)})'
    
    def __len__(self):
        return self.length
    
    def __iter__(self):
        return self
    
    def __next__(self):
        '''Execute a LFSR step and returns the output bit (bool)'''
        self._state = ((self._state << 1) | self._feedback) & self._statemask
        self._output = bool(self._state & self._outmask)
        self._feedback = parity(self._state & self._poly) 
        return self._output
    
    def run_steps(self, n=1):
        '''
        Execute multiple LFSR steps.
        
        Parameters
        ----------
        n: int, optional (default=1)
            number of steps to execute.
        
        Output
        ------
        list of bool (len=n),
            LFSR output bit stream.
        '''
        return [next(self) for _ in range(n)]
   
    def cycle(self, state=None):
        '''
        Execute a full LFSR cycle (LFSR.len steps).
        
        Parameters
        ----------
        state: int or list of int or bools, optional (default=None)
            shift register state. If None, state is kept as is.
        
        Output
        ------
        list of bool (len=2**myLFSR.len - 1),
            LFSR output bit stream.
        '''
        if state is not None:
            self.state = state
        return self.run_steps(n=int(2**len(self)) - 1)


def berlekamp_massey(bits, verbose=False):
    '''
    Find the shortest LFSR for a given binary sequence.
    
    Parameters
    ----------
    bits: list/string of 0/1,
        stream of bits.
        
    Return
    ------
    list of int,
        linear feedback polynomial expressed as list of the exponents related
        to the non-zero coefficients
    '''
    
    # variables initialization
    P, m = 0x1, 0
    Q, r = 0x1, 1
    
    if verbose:
        from math import log2
        lenP = 1 + int(log2(len(b)+1))
        print(f'  t b d {"poly":>{lenP}} m {"Q":>{lenP}} r')
        print(f'  - - - {P:{lenP}b} 0 {Q:{lenP}b} 1')
    
    for t in range(len(bits)):
        
        # compute discrepancy
        d = parity(P & bits_to_int(bits[t-m:t+1][::-1]))
        
        if d:
            if 2*m <= t: # A                
                P, Q = P^(Q<<r), P
                m, r = t+1-m, 0
            else: # B
                P = P^(Q<<r)
        r += 1
        
        if verbose:
            print(f'{t:3d} {bits[t]} {d:d} {P:{lenP}b} {m} {Q:{lenP}b} {r}')
            
    # convert poly from integer to list of degree of non-zero coefficients
    poly = int_to_sparse(P)[::-1]
    return poly


class BerlekampMassey():
    '''
    Berlekamp-Massey Algorithm. 
    The algorithm finds the shortest LFSR for a given binary sequence.
    
    This class returns a function whose call method takes one bit at a time as 
    input and returns the feedback polynomial of the shortest LFSR capable of 
    generating the sequence of all bits received up to the last one.
    
    Attributes
    ----------
    poly: list of int,
        feedback polynomial expressed as list of integers corresponding to
        the degrees of the non-zero coefficients.
    
    Methods
    -------
    __call__(bit):
        update and return the polynomial of the shortest LFSR for the observed 
        bit sequence.
    discrepancy():
        compute the discrepancy bit that is 0 (False) if the polynomial `poly` 
        explain the observed bit sequence, or 1 (True) otherwise.
    '''
    
    def __init__(self):
        ''' class constructor '''
        # init algorithm's internal variables
        self.P, self.m = 0x1, 0
        self.Q, self.r = 0x1, 1
        # init an empty sequence of bits
        self.bits = 0 # self.bits = []
        self.tau = 0
    
    # ==== poly ====
    @property
    def poly(self):
        return int_to_sparse(self.P)[::-1]
    @poly.setter
    def poly(self, val):
        raise AttributeError('Denied')

    def discrepancy(self):
        b = self.bits & ((1 << (self.m + 1)) - 1)
        d = parity(self.P & b)
        return d
    
    def __call__(self, bit):
        '''
        Update the feedback polynomial characterizing the shortest LFSR capable 
        of generating the sequence of all bits received.
    
        Parameters
        ----------
        bit: bool, int, or 0/1 str
            input bit
        
        Return
        ------
        poly: list of int,
            feedback polynomial expressed as list of integers corresponding to
            the degrees of the non-zero coefficients.
        '''
        # append
        self.bits = (self.bits << 1) | int(bit)  # self.bits.append(bit)
        if self.discrepancy():
            if 2*self.m <= self.tau: # A                
                self.P, self.Q = self.P ^ (self.Q << self.r), self.P
                self.m, self.r = self.tau + 1 - self.m, 0
                self.bits &= (1<<self.m) - 1  # self.bits = self.bits[-self.m:]
            else: # B
                self.P = self.P ^ (self.Q << self.r)
        self.r += 1
        self.tau += 1
        
        return self.poly


#code to execute if called from command-line
if __name__ == '__main__':    
    pass    #do nothing - code deleted