#!/usr/bin/python
# -*- coding: utf-8 -*-

from .util import product

from gmpy2 import *


__all__ = [ 'crt' ]


def crt(a, p):
    N = product(*p)
    n = [divexact(N, pi) for pi in p]
    u = list(map(lambda a, b: pow(a, -1, b), n, p))
    return sum(map(product, a, n, u)) % N


def _main():
    global _DEBUG

    import sys

    if len(sys.argv) != 3:
        print('Usage: crt a1,a2[,...[,ak]]] p1,p2[,...[,pk]]]')
        print()
        print('  Solve a system of linear equations using the Chinese Remainder Theorem.')
        print()
        print('  i.e. Find an integer x (mod N), where N = p1 * p2 * ... * pk, s.t.')
        print()
        print('  x = a1 (mod p1)')
        print('  x = a2 (mod p2)')
        print('  ...')
        print('  x = ak (mod pk)')
        sys.exit(0)

    a = list(map(mpz, sys.argv[1].split(',')))
    p = list(map(mpz, sys.argv[2].split(',')))

    x = crt(a, p)

    print(f'x = {x}')


if __name__ == '__main__':
    _main()
