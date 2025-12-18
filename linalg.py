# linalg.py

import math

def MdotM(A, B):
    res = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                res[i][j] += A[i][k] * B[k][j]
    return res


def MdotV(M, V):
    res = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            res[i] += M[i][j] * V[j]
    return res


class Point:
    def __init__(self, p):
        self.x, self.y, self.z = p


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def construct(p1, p2):
        return Vector(
            p2.x - p1.x,
            p2.y - p1.y,
            p2.z - p1.z
        )


def getN(v1, v2):
    return Vector(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )

