#!/usr/bin/python
# -*- coding: utf-8 -*-

from gmpy2 import *


__all__ = [ 'babygiant' ]


def babygiant(G, H, P):
    m = isqrt(P) + 1
    table = {pow(G, j, P) : j for j in range(m)}
    ginvm = pow(G, -m, P)
    y = H
    for i in range(m):
        if y in table:
            return i * m + table[y]
        y = (y * ginvm) % P
    return None


def _main():
    global _DEBUG

    import sys

    if len(sys.argv) != 4:
        print('Usage: babygiant g h p')
        print()
        print('  Solve the discrete logarithm using the Baby-step giant-Step algorithm.')
        print()
        print('  i.e. Find an integer x s.t. g^x = h (mod p).')
        sys.exit(0)

    g = mpz(sys.argv[1])
    h = mpz(sys.argv[2])
    p = mpz(sys.argv[3])

    x = babygiant(g, h, p)

    print(f'x = {x}')


if __name__ == '__main__':
    _main()
