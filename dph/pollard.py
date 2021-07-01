#!/usr/bin/python
# -*- coding: utf-8 -*-

from .config import *


MAX_RETRIES = 3


__all__ = [ 'MAX_RETRIES', 'pollard' ]


def pollard(G, H, P, a=1, b=1):
    Q = (P - 1) // 2

    def xab(x, a, b):
        xsub = x % 3

        if xsub == 0:
            x = (x * G) % P
            a = (a + 1) % Q
        if xsub == 1:
            x = (x * H) % P
            b = (b + 1) % Q
        if xsub == 2:
            x = (x * x) % P
            a = (a * 2) % Q
            b = (b * 2) % Q

        return (x, a, b)

    x = G * H
    X = x
    A = a
    B = b

    if Config.debug:
        w1 = len(str(P))
        w2 = len(str(Q))
        fmts = f''.join([
            'i'.rjust(w1),
            ' ',
            ' ',
            'x'.rjust(w1),
            ' ',
            'a'.rjust(w2),
            ' ',
            'b'.rjust(w2),
            ' ',
            ' ',
            'X'.rjust(w1),
            ' ',
            'A'.rjust(w2),
            ' ',
            'B'.rjust(w2),
            ])
        print('-' * len(fmts))
        print(fmts)
        print('-' * len(fmts))
        fmts = f''.join([
            f'{{:{w1}d}}',
            f' ',
            f' ',
            f'{{:{w1}d}}',
            f' ',
            f'{{:{w2}d}}',
            f' ',
            f'{{:{w2}d}}',
            f' ',
            f' ',
            f'{{:{w1}d}}',
            f' ',
            f'{{:{w2}d}}',
            f' ',
            f'{{:{w2}d}}',
            ])

    for _ in range(1, P):
        x, a, b = xab(x, a, b)
        X, A, B = xab(X, A, B)
        X, A, B = xab(X, A, B)
        if Config.debug:
            print(fmts.format(_, x, a, b, X, A, B))
        if x == X:
            break

    result = ((a - A) * pow(B - b, -1, Q)) % Q
    if pow(G, result, P) == H:
        return result
    result += Q
    if pow(G, result, P) == H:
        return result

    raise ValueError


def _main():
    from gmpy2 import mpz
    import math
    import random
    import sys

    if len(sys.argv) != 4:
        print('Usage: pollard g h p')
        print()
        print('  Solve the discrete logarithm using Pollard Rho\'s algorithm for discrete logarithms.')
        print()
        print('  i.e. Find an integer x s.t. g^x = h (mod p).')
        sys.exit(0)

    g = mpz(sys.argv[1])
    h = mpz(sys.argv[2])
    p = mpz(sys.argv[3])

    a = mpz(1)
    b = mpz(1)

    w1 = 1 + int(math.log10(MAX_RETRIES))
    w2 = 1 + int(math.log10(p))

    err_fmts = f'Attempt #{{:{w1}}} failed -- retrying with a = {{:{w2}}}, b = {{:{w2}}}...'

    for i in range(MAX_RETRIES):
        try:
            x = pollard(g, h, p, a, b)
            if Config.debug:
                print()
            print(f'x = {x}')
            break
        except ValueError:
            a = mpz(random.randint(1, p))
            b = mpz(random.randint(1, p))
            if Config.debug:
                print()
            print(err_fmts.format(i, a, b))
    else:
        print()
        print(f'Maximum number of attempts reached. Failed to solve {g}^x = {h} (mod {p}).')
        sys.exit(1)


if __name__ == '__main__':
    _main()
