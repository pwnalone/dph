#!/usr/bin/python

from .config import *

from binascii import hexlify
from gmpy2 import *
import os


SMOOTHNESS = 30

FIELD_SIZE = 2048


__all__ = [ 'get_prime', 'get_b_smooth_prime', 'get_params' ]


def get_prime(state, bits):
    return next_prime(mpz_urandomb(state, bits) | (1 << (bits - 1)))

def get_b_smooth_prime(state, bits, smoothness):
    p = mpz(2)
    p_factors = [p]
    while p.bit_length() < bits - 2 * smoothness:
        factor = get_prime(state, smoothness)
        p_factors.append(factor)
        p *= factor

    bitcnt = (bits - p.bit_length()) // 2

    while True:
        fact_1 = get_prime(state, bitcnt)
        fact_2 = get_prime(state, bitcnt)
        tmpp = p * fact_1 * fact_2
        if tmpp.bit_length() < bits:
            bitcnt += 1
            continue
        if tmpp.bit_length() > bits:
            bitcnt -= 1
            continue
        if is_prime(tmpp + 1):
            p_factors.append(fact_1)
            p_factors.append(fact_2)
            p = tmpp + 1
            break

    p_factors.sort()

    return (p_factors, p)

def get_params(state, bits, smoothness):
    n = 0

    while n.bit_length() != bits:
        p_factors, p = get_b_smooth_prime(state, bits // 2, smoothness)
        q_factors, q = get_b_smooth_prime(state, bits // 2, smoothness)
        n = p * q

    # FIXME: Unfortunately, this doesn't seem to work too well...

#   while True:
#       size = n.bit_length()
#       if size < bits:
#           if p_factors[0] < q_factors[0]:
#               small = p_factors[0]
#               p = divexact(p - 1, small)
#               prime = 1
#               while not is_prime(p * prime + 1):
#                   prime = get_prime(state, small.bit_length() + 1)
#               p = p * prime + 1
#               p_factors[0] = prime
#               p_factors.sort()
#           else:
#               small = q_factors[0]
#               q = divexact(q - 1, small)
#               prime = 1
#               while not is_prime(q * prime + 1):
#                   prime = get_prime(state, small.bit_length() + 1)
#               q = q * prime + 1
#               q_factors[0] = prime
#               q_factors.sort()
#           continue
#       if size > bits:
#           if p_factors[-1] > q_factors[-1]:
#               large = p_factors[-1]
#               p = divexact(p - 1, large)
#               prime = 1
#               while not is_prime(p * prime + 1):
#                   prime = get_prime(state, large.bit_length() - 1)
#               p = p * prime + 1
#               p_factors[-1] = prime
#               p_factors.sort()
#           else:
#               large = q_factors[-1]
#               q = divexact(q - 1, large)
#               prime = 1
#               while not is_prime(q * prime + 1):
#                   prime = get_prime(state, large.bit_length() - 1)
#               q = q * prime + 1
#               q_factors[-1] = prime
#               q_factors.sort()
#           continue
#       break

    return (p_factors, p, q_factors, q, n)


def _main():
    import sys

    if len(sys.argv) > 3:
        print('Usage: paramgen [bits] [smoothness]')
        print()
        print('  Generate special parameters to inject a NOBUS backdoor into a Diffie-Hellman implementation.')
        print()
        print('Arguments:')
        print('  bits        The size (in bits) of the semi-prime Diffie-Hellman modulus [default: 2048]')
        print('  smoothness  The smoothness (in bits) of the factors forming `p - 1` and `q - 1`,')
        print('              where `p` and `q` are the prime factors of the semi-prime Diffie-Hellman')
        print('              modulus [default: 30]')
        sys.exit(0)

    field_size = int(sys.argv[1]) if len(sys.argv) > 1 else FIELD_SIZE
    smoothness = int(sys.argv[2]) if len(sys.argv) > 2 else SMOOTHNESS

    seed = int(hexlify(os.urandom(16)).decode(), 16)
    state = random_state(seed)

    p_factors, p, q_factors, q, n = get_params(state, field_size, smoothness)

    print(f'p = {p.digits(16)}')
    print()
    print(f'p_factors = [')
    for factor in p_factors:
        print(f'    {factor.digits(16)},')
    print(f']', end='\n\n')

    print(f'q = {q.digits(16)}')
    print()
    print(f'q_factors = [')
    for factor in q_factors:
        print(f'    {factor.digits(16)},')
    print(f']', end='\n\n')

    print(f'n = {n.digits(16)}')
    print()

    if Config.verbose:
        print(f'p ({p.bit_length()} bits)')
        print(f'q ({q.bit_length()} bits)')
        print(f'n ({n.bit_length()} bits)')


if __name__ == '__main__':
    _main()
