# !/bin/env python3

import numpy as np

NUM = 10                        # TODO

def A(n, k):
    if (k > n):
        raise ValueError('n >= k')
    ret = 1
    for i in range(n, n-k, -1):
        ret *= i
    return ret

def C(n, k):
    if (k > n):
        raise ValueError('n >= k')
    if (k > n/2):
        return C(n, n-k)
    else:
        return int(A(n, k) / A(k, k))

def main(args=None):
    params_mat = np.matrix(
        [
            [C(k, i) if k >= i else 0 for i in range(1, NUM+1)]
            for k in range(1, NUM+1)
        ])
    belta_mat = np.matrix([i**NUM for i in range(1, NUM+1)]).getT()
    result = params_mat.getI() * belta_mat
    print("K items repeatable all selection N times (N >= k, N = {0:d}):".format(NUM))
    k = 1
    for r in result:
        print("a({0:d}, {1:d}) = {2:d},".format(NUM, k, int(np.round(r))))
        k += 1
    print()

main()
