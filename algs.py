# Author: Robby Costales
# Date: 2018-04-24
# Language: Python 3

# Purpose: File contains all dynamic programming algorithms

import time
# local


def global_align(u, v, m, gp):
    """
    Finds global alignment of two strings, u and v

    Args:
        u, v : strings
        m : scoring matrix
        gp : gap penalty (horiz / vert)

    Returns:
        score (float), alignment (str)
    """

    return 0


def local_align(u, v, m, gp):
    """
    Finds local alignment of two strings, u and v

    Args:
        u, v : strings
        m : scoring matrix
        gp : gap penalty (horiz / vert)

    Returns:
        score (float), alignment (str)
    """

    return 0


def affine_align(u, v, m, gp):
    """
    Finds global alignment of two strings, u and v, using affine gap weights

    Args:
        u, v : strings
        m : scoring matrix
        gp : gap penalty (horiz / vert) initial
        ap : gap penalty after repeat (affine gap penalty)

    Returns:
        score (float), alignment (str)
    """

    return 0


if __name__ == "__main__":

    # u and v are sequences
    u = "AAAGAATTCA"
    v = "AAATCA"

    # m is the scoring matrix
    m = [[1, -1, -1, -1],
        [-1, 1, -1, -1],
        [-1, -1, 1, -1],
        [-1, -1, -1, 1]]

    # gp is gap penalty
    gp = 1
    # ap is affine penalty (only for affine)
    ap = 0

    # do global align
    x = global_align(u, v, m, gp)
    print(x[0])
    print(x[1])

    # do local align
    y = local_align(u, v, m, gp)
    print(y[0])
    print(y[1])

    # do global w/ affine gap weights
    z = affine_align(u, v, m, gp, ap)
    print(z[0])
    print(z[1])
