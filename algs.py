# Author: Robby Costales
# Date: 2018-04-24
# Language: Python 3

# Purpose: File contains all dynamic programming algorithms

import time
import numpy as np
import sys
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

    return dpTable[-1][-1], alignment, dpTable



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

    return result, alignment, dpTable



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

    return dpTable[-1][-1], alignment, dpTable


def read_matrix(fileName):
    f = open(fileName, "r")

    matrix = []
    for i in range(5):
        x = f.readline()
        matrix.append(list(x.split(" ")))

    # get score matrix
    score_matrix = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(int(matrix[i+1][j+1].replace("\n", "")))
        score_matrix.append(row)

    # get mtags
    mtags = {}
    for i in range(4):
        mtags[matrix[i+1][0]] = i

    return score_matrix, mtags


def read_sequence(fileName):
    f = open(fileName, "r")

    # skip first line
    new = f.readlines()

    sequence = ""
    for line in new[1:]:
        line = line.replace("\n", "")
        sequence += line

    return sequence



if __name__ == "__main__":
    global mtags
    # get inputs
    align_type = sys.argv[1]
    seq_file_1 = "seqs/" + sys.argv[2]
    seq_file_2 = "seqs/" + sys.argv[3]
    score_file = "scores/" + sys.argv[4]
    gp = float(sys.argv[5])

    u = read_sequence(seq_file_1)
    v = read_sequence(seq_file_2)
    m, mtags = read_matrix(score_file)

    if align_type == "global":
        x = global_align(u, v, m, gp)
    elif align_type == "local":
        x = local_align(u, v, m, gp)
    elif align_type == "affine":
        ap = float(sys.argv[6])
        x = affine_align(u, v, m, gp, ap)
    else:
        raise

    print (x[0])
    # print (np.matrix(x[1])) # uncomment to print the alignment
    # print (np.matrix(x[2])) # uncomment to print dynamic programming table
