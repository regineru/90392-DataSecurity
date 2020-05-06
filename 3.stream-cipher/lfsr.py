#!/usr/bin/env python

'''
Linear Feedback Shift register (LFSR)
'''

__version__ = "0.0.1"

def parity(x):
    '''Returns the parity bit (bool) of the input `x` (int)'''
    return bool(sum(int(b) for b in '{:b}'.format(x)) % 2)

def reverse(x, n):
    '''Reverses the order of the `n` (int) bits in the input `x` (int)'''
    return int('{:0{}b}'.format(x, n)[::-1], 2)


class LFSR(object):
    '''
    Class implementing a Linear Feedback Shift Register (LFSR)
    
    Attributes
    ----------
    poly: list of int,
        feedback polynomial expressed as list of integers corresponding to
        the degrees of the non-zero coefficients.
    state: int, bytes,
        state of the shift register. bytes are considered little endian.
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
        poly: list of int/bool, string,
            feedback polynomial expressed as list of integers corresponding to
            the degrees of the non-zero coefficients, or as list of 0/1
            coefficients in the form of list of bools or string.
        state: int, list of int/bool, string, optional (default=None)
            shift register initial state expressed as integer or as bit
            sequence in the form of list of bool or string.
            If None, state is set to all ones.
        '''
        if hasattr(poly, '__iter__') and len(poly) > 1:
            if all(int(p) in (0, 1) for p in poly):
                length = len(poly)
                _poly = sum([int(p) << i for i, p in enumerate(poly)])
            elif all(type(p) is int for p in poly):
                length = max(poly)
                _poly = sum([2**p for p in poly])
            else:
                raise TypeError('input type is not supported')
        else:
            raise TypeError('input type is not supported')

        self._statemask = (1 << length) - 1
        self._outmask = 1 << (length-1)
        
        if state is None:
            state = self._statemask
            
        self._poly = _poly >> 1
        self._len = length
        self.state = state
        self._feedback = parity(self._state & self._poly) 
        self._output = bool(self._state & self._outmask)

    @property
    def len(self):
        return self._len
    
    @len.setter
    def len(self, val):
        raise AttributeError('Denied')
    
    @property
    def poly(self):
        poly_bin = '{:0{}b}'.format(self._poly, len(self))[::-1]
        poly = [0] + [i+1 for i, b in enumerate(poly_bin) if int(b) > 0]
        return list(reversed(poly))
    
    @poly.setter
    def poly(self, poly):
        raise AttributeError('Denied')

    @property
    def state(self):
        return reverse(self._state, self.len)
    
    @state.setter
    def state(self, state):
        if isinstance(state, int):
            _state = state
        elif isinstance(state, (bytes, bytearray)):
            _state = int.from_bytes(state, byteorder='little')
        elif hasattr(state, '__iter__')\
            and all(int(p) in (0, 1) for s in state):
            _state = sum([int(s) << i for i, s in enumerate(state)])
        else:
            raise TypeError('input type is not supported')
        self._state = reverse(_state & self._statemask, len(self))

    @property
    def output(self):
        return self._output
    
    @output.setter
    def output(self, val):
        raise AttributeError('Denied')

    @property
    def feedback(self):
        return self._feedback
    
    @feedback.setter
    def feedback(self, feedback):
        if not (type(feedback) is bool):
            raise TypeError('feedback must be bool')
        self._feedback = feedback
        
    def __str__(self):
        poly_str = ' + '.join(
            [('x^'+str(d) if d > 1 else 'x' if d == 1 else '1') 
             for d in self.poly])
        output = None if self.output is None else int(self.output)
        _str = 'poly: "{}", state: 0x{:0{}x}, output: {}'\
            .format(poly_str, self.state, (self.len+1)//4, output)
        return _str
        
    def __repr__(self):
        return 'LSFR({})'.format(self.__str__())
    
    def __len__(self):
        return self.len
    
    def __iter__(self):
        return self
    
    def __next__(self):
        '''Execute a LFSR step and returns the output bit (bool)'''
        self._state = ((self._state << 1) | self._feedback) & self._statemask
        self._output = bool(self._state & self._outmask)
        self._feedback = parity(self._state & self._poly) 
        return self._output
    
    def run_steps(self, N=1):
        '''
        Execute multiple LFSR steps.
        
        Parameters
        ----------
        N: int, optional (default=1)
            number of steps to execute.
        
        Output
        ------
        list of bool (len=N),
            LFSR output bit stream.
        '''
        return [next(self) for _ in range(N)]
   
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
        return self.run_steps(N=int(2**self.len) - 1)

    
def discrepancy(P, m, b, t):
    '''
    Compute discrepancy (bool) between the Polynomial `P` (int) with degree `m`
    (int) and the bit sequence `b` (list/string of 0/1) at time `t` (int)
    '''
    # select bits b_t, b_{t-1}, ..., b_{t-j} in reverse order
    bbits = b[t:t-m-1 if t > m else None:-1]
    # transform bits in integer
    bint = sum([1 << i for i, bit in enumerate(bbits) if bool(int(bit))])
    # compute discrepancy 
    d = parity(P & bint)
    return d

def berlekamp_massey(b, verbose=False):
    '''
    Find the shortest LFSR for a given binary sequence.
    
    Parameters
    ----------
    b: list/string of 0/1,
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
        print('t b d {:>{}} m {:>{}} r'.format('poly', lenP, 'Q', lenP))
        print('- - - {:{}} 0 {:{}} 1'.format(P, lenP, Q, lenP))
    
    for t in range(len(b)):
        # compute discrepancy
        d = discrepancy(P, m, b, t)
        if d:
            if 2*m <=t: # A
                P, Q = P^(Q<<r), P
                m, r = t+1-m, 0
            else: # B
                P = P^(Q<<r)
        r += 1
        
        if verbose:
            print(t, int(b[t]), int(d), '{:{}b}'.format(P, lenP), m, 
                  '{:{}b}'.format(Q, lenP), r)
            
    # convert poly from integer to list of degree of non-zero coefficients
    poly = [i for i, p in enumerate('{:b}'.format(P)[::-1]) if bool(int(p))]
    return list(reversed(sorted(poly)))


#code to execute if called from command-line
if __name__ == '__main__':    
    pass    #do nothing - code deleted