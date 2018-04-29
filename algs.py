# Author: Robby Costales
# Date: 2018-04-24
# Language: Python 3

# Purpose: File contains all dynamic programming algorithms

import time
import numpy as np
# local


def global_align(u, v, m, gp):
    """
    Finds global alignment of two strings, u and v

    Args:
        u, v : strings
        m : scoring matrix
        gp : gap penalty (horiz / vert)

    Returns:
        score (float), alignment (str), dpTable (2d list)
    """
    global mtags

    # make strings uppercase
    u = u.upper()
    v = v.upper()

    rows = len(u)
    cols = len(v)

    # +1 is for the base cases
    dpTable = [[None for j in range(cols+1)] for i in range(rows+1)]

    # direction where each value came from
    dirTable = [[None for j in range(cols+1)] for i in range(rows+1)]

    # initialize base cases
    for i in range(rows+1):
        dirTable[i][0] = "north"
        dpTable[i][0] = gp*i
    for j in range(cols+1):
        dirTable[0][j] = "west"
        dpTable[0][j] = gp*j
    dirTable[0][0] = None

    # dynamic programming
    for i in range(1, rows+1):
        for j in range(1, cols+1):
            # get string values for matrix
            char1 = u[i-1]
            char2 = v[j-1]
            diagPen = m[mtags[char1]][mtags[char2]]

            # get directional values
            north = dpTable[i-1][j] + gp
            west = dpTable[i][j-1] + gp
            diag = dpTable[i-1][j-1] + diagPen

            vals = [north, west, diag]

            maxval = max(vals)
            dirTable[i][j] = maxval
            ind = vals.index(maxval)

            # get maximum
            if ind == 2:
                dpTable[i][j] = diag
                dirTable[i][j] = "diag"
            elif ind == 0:
                dpTable[i][j] = north
                dirTable[i][j] = "north"
            elif ind == 1:
                dpTable[i][j] = west
                dirTable[i][j] = "west"
            else:
                raise

    # get traceback
    path = []
    last = dirTable[-1][-1]
    inds = (-1, -1)
    while last != None:
        if last == "north":
            path.insert(0, "north")
            inds = (inds[0]-1, inds[1])
        elif last == "west":
            path.insert(0, "west")
            inds = (inds[0], inds[1]-1)
        elif last == "diag":
            path.insert(0, "diag")
            inds = (inds[0]-1, inds[1]-1)
        else:
            raise
        last = dirTable[inds[0]][inds[1]]

    # alignment
    alignment = []
    ucount = 0
    vcount = 0
    for val in path:
        if val == "diag":
            alignment.append((u[ucount], v[vcount]))
            ucount += 1
            vcount += 1
        elif val == "north":
            alignment.append((u[ucount], "-"))
            ucount += 1
        elif val == "west":
            alignment.append(("-", v[vcount]))
            vcount += 1

    return 0, alignment, dpTable



def local_align(u, v, m, gp):
    """
    Finds local alignment of two strings, u and v

    Args:
        u, v : strings
        m : scoring matrix
        gp : gap penalty (horiz / vert)

    Returns:
        score (float), alignment (str), dpTable (2d list)
    """
    global mtags

    result = 0
    resulti = (0, 0)

    # make strings uppercase
    u = u.upper()
    v = v.upper()

    rows = len(u)
    cols = len(v)

    # 0s on sides
    # traceback: find max, and keep finding max backwards till you reach a 0

    # +1 is for the base cases
    dpTable = [[None for j in range(cols+1)] for i in range(rows+1)]

    # direction where each value came from
    dirTable = [[None for j in range(cols+1)] for i in range(rows+1)]

    # initialize base cases
    for i in range(rows+1):
        dpTable[i][0] = 0
    for j in range(cols+1):
        dpTable[0][j] = 0
    dirTable[0][0] = None

    # dynamic programming
    for i in range(1, rows+1):
        for j in range(1, cols+1):
            # get string values for matrix
            char1 = u[i-1]
            char2 = v[j-1]
            diagPen = m[mtags[char1]][mtags[char2]]

            # get directional values
            north = dpTable[i-1][j] + gp
            west = dpTable[i][j-1] + gp
            diag = dpTable[i-1][j-1] + diagPen

            vals = [north, west, diag, 0]

            maxval = max(vals)
            dirTable[i][j] = maxval
            ind = vals.index(maxval)

            # get maximum
            if ind == 2:
                dpTable[i][j] = diag
                dirTable[i][j] = "diag"
            elif ind == 0:
                dpTable[i][j] = north
                dirTable[i][j] = "north"
            elif ind == 1:
                dpTable[i][j] = west
                dirTable[i][j] = "west"
            elif ind == 3:
                dpTable[i][j] = 0
                dirTable[i][j] = None
            else:
                raise

            # check if maximum found
            if maxval > result:
                result = maxval
                resulti = (i, j)

    # get traceback
    path = []
    last = dirTable[resulti[0]][resulti[1]]
    inds = (resulti[0], resulti[1])
    while last != None:
        if last == "north":
            path.insert(0, "north")
            inds = (inds[0]-1, inds[1])
        elif last == "west":
            path.insert(0, "west")
            inds = (inds[0], inds[1]-1)
        elif last == "diag":
            path.insert(0, "diag")
            inds = (inds[0]-1, inds[1]-1)
        else:
            raise

        last = dirTable[inds[0]][inds[1]]

    # alignment
    alignment = []
    ucount = inds[0]
    vcount = inds[1]

    for i in range(ucount):
        alignment.append((u[i], "-"))
    for j in range(vcount):
        alignment.append(("-", v[i]))

    for val in path:
        if val == "diag":
            alignment.append((u[ucount], v[vcount]))
            ucount += 1
            vcount += 1
        elif val == "north":
            alignment.append((u[ucount], "-"))
            ucount += 1
        elif val == "west":
            alignment.append(("-", v[vcount]))
            vcount += 1

    return 0, alignment, dpTable



def affine_align(u, v, m, gp, ap):
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
    global mtags

    # make strings uppercase
    u = u.upper()
    v = v.upper()

    rows = len(u)
    cols = len(v)

    # +1 is for the base cases
    dpTable = [[None for j in range(cols+1)] for i in range(rows+1)]

    # direction where each value came from
    dirTable = [[None for j in range(cols+1)] for i in range(rows+1)]

    # initialize base cases
    dpTable[0][0] = 0
    for i in range(rows):
        dpTable[i+1][0] = gp+i*ap
    for j in range(cols):
        dpTable[0][j+1] = gp+j*ap

    # dynamic programming
    for i in range(1, rows+1):
        for j in range(1, cols+1):
            # get string values for matrix
            char1 = u[i-1]
            char2 = v[j-1]
            diagPen = m[mtags[char1]][mtags[char2]]

            # get directional values
            if dirTable[i-1][j]=="north":
                north = dpTable[i-1][j] + ap
            else:
                north = dpTable[i-1][j] + gp

            if dirTable[i][j-1]=="west":
                west = dpTable[i][j-1] + ap
            else:
                west = dpTable[i][j-1] + gp

            diag = dpTable[i-1][j-1] + diagPen

            vals = [north, west, diag]

            maxval = max(vals)
            dirTable[i][j] = maxval
            ind = vals.index(maxval)

            # get maximum
            if ind == 2:
                dpTable[i][j] = diag
                dirTable[i][j] = "diag"
            elif ind == 0:
                dpTable[i][j] = north
                dirTable[i][j] = "north"
            elif ind == 1:
                dpTable[i][j] = west
                dirTable[i][j] = "west"
            else:
                raise

    # get traceback
    path = []
    last = dirTable[-1][-1]
    inds = (-1, -1)
    while last != None:
        if last == "north":
            path.insert(0, "north")
            inds = (inds[0]-1, inds[1])
        elif last == "west":
            path.insert(0, "west")
            inds = (inds[0], inds[1]-1)
        elif last == "diag":
            path.insert(0, "diag")
            inds = (inds[0]-1, inds[1]-1)
        else:
            raise
        last = dirTable[inds[0]][inds[1]]

    # alignment
    alignment = []
    ucount = 0
    vcount = 0
    for val in path:
        if val == "diag":
            alignment.append((u[ucount], v[vcount]))
            ucount += 1
            vcount += 1
        elif val == "north":
            alignment.append((u[ucount], "-"))
            ucount += 1
        elif val == "west":
            alignment.append(("-", v[vcount]))
            vcount += 1

    return 0, alignment, dpTable


if __name__ == "__main__":

    global mtags
    mtags = {"C":0, "T":1, "A":2, "G":3}

    # u and v are sequences
    u = "AAAGAATTCA"
    v = "AAATCA"

    # m is the scoring matrix
    # ORDER: C, T, A, G
    m = [[1, -1, -1, -1],
        [-1, 1, -1, -1],
        [-1, -1, 1, -1],
        [-1, -1, -1, 1]]

    # gp is gap penalty
    gp = -1
    # ap is affine penalty (only for affine)
    ap = -0.1

    # do global align
    x = global_align(u, v, m, gp)

    # do local align
    y = local_align(u, v, m, gp)

    # do global w/ affine gap weights
    z = affine_align(u, v, m, gp, ap)
