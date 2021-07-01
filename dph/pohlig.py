#!/usr/bin/python
# -*- coding: utf-8 -*-

from .config import *
from .crt import crt
from .pollard import pollard

from gmpy2 import *


__all__ = [ 'pohlig' ]


def pohlig(G, H, P, factors):
    g = [pow(G, divexact(P - 1, f), P) for f in factors]
    h = [pow(H, divexact(P - 1, f), P) for f in factors]

    if Config.verbose:
        x = []
        total = len(factors)
        for i, (gi, hi) in enumerate(zip(g, h), start=1):
            print('Solving discrete logarithm {}/{}...'.format(str(i).rjust(len(str(total))), total))
            result = pollard(gi, hi, P)
            x.append(result)
            print(f'x = 0x{result.digits(16)}')
    else:
        x = [pollard(gi, hi, P) for gi, hi in zip(g, h)]

    return crt(x, factors)


def _main():
    import sys

    if len(sys.argv) != 5:
        print('Usage: pollard g h p f1[,f2[,...[,fk]]]')
        print()
        print('  Solve the discrete logarithm in a finite abelian group using the Pohlig-Hellman algorithm.')
        print()
        print('  i.e. Find an integer x s.t. g^x = h (mod p), where p - 1 = f1 * f2 * ... * fk.')
        sys.exit(0)

    g = mpz(sys.argv[1])
    h = mpz(sys.argv[2])
    p = mpz(sys.argv[3])

    factors = list(map(mpz, sys.argv[4].split(',')))

    x = pohlig(g, h, p, factors)
    if Config.verbose:
        print()

    print(f'x = {x}')


if __name__ == '__main__':
    _main()
