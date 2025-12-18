# -*- coding: utf-8 -*-

import linalg
import math
from PIL import Image, ImageDraw


class Figure:
    def __init__(self):
        self.points = [
            (0.0, 0.0, 0.0),
            (45.0, 0.0, 0.0),
            (45.0, 45.0, 0.0),
            (0.0, 45.0, 0.0),
            (0.0, 0.0, 90.0)
        ]

        self.faces = [
            (0, 1, 2, 3), 
            (1, 2, 4),  
            (2, 3, 4)  
        ]

        self.colors = [
            (200, 200, 0),  
            (150, 150, 150), 
            (0, 90, 200)  
        ]


def transform(M, figure):
    f = Figure()
    f.faces = figure.faces
    f.colors = figure.colors
    f.points = [None] * len(figure.points)

    for i in range(len(figure.points)):
        vec = [figure.points[i][0], figure.points[i][1], figure.points[i][2], 1]
        x, y, z, _ = linalg.MdotV(M, vec)
        f.points[i] = (x, y, z)
    return f


def isIn(face, points, x, y):  #попадает ли пиксель в грань
    n = len(face)
    last_sign = 0
    for i in range(n):
        p1 = points[face[i]]
        p2 = points[face[(i + 1) % n]]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        p_dx = x - p1[0]
        p_dy = y - p1[1]
        cross = dx * p_dy - dy * p_dx
        if cross != 0:
            current_sign = 1 if cross > 0 else -1
            if last_sign == 0:
                last_sign = current_sign
            elif last_sign != current_sign:
                return False
    return True


def getZ(face, points, x, y): #вычисление глубины
    p1 = linalg.Point(points[face[0]])
    p2 = linalg.Point(points[face[1]])
    p3 = linalg.Point(points[face[2]])
    v1 = linalg.Vector.construct(p1, p3)
    v2 = linalg.Vector.construct(p1, p2)
    N = linalg.getN(v1, v2)
    if N.z != 0:
        d = -(N.x * p1.x + N.y * p1.y + N.z * p1.z)
        return -(N.x * x + N.y * y + d) / N.z
    return -10000


if __name__ == "__main__":
    img = Image.new('RGB', (300, 200), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    figure = Figure()

    scale = 2.0
    S = [
        [scale, 0, 0, 0],
        [0, scale, 0, 0],
        [0, 0, scale, 0],
        [0, 0, 0, 1]
    ]

    ay = 135 * math.pi / 180  #135
    Ry = [
        [math.cos(ay), 0, math.sin(ay), 0],
        [0, 1, 0, 0],
        [-math.sin(ay), 0, math.cos(ay), 0],
        [0, 0, 0, 1]
    ]

    ax = 10 * math.pi / 180 #10
    Rx = [
        [1, 0, 0, 0],
        [0, math.cos(ax), -math.sin(ax), 0],
        [0, math.sin(ax), math.cos(ax), 0],
        [0, 0, 0, 1]
    ]

    M_trans = [
        [1, 0, 0, 110],
        [0, -1, 0, 150],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

    m_temp1 = linalg.MdotM(Ry, S)
    m_temp2 = linalg.MdotM(Rx, m_temp1)
    M_final = linalg.MdotM(M_trans, m_temp2)

    f1 = transform(M_final, figure)

    w, h = img.size

    for y in range(h):
        for x in range(w):
            max_z = -10000
            pixel_color = None

            for i, face in enumerate(f1.faces):
                if isIn(face, f1.points, x, y):
                    z = getZ(face, f1.points, x, y)
                    if z > max_z:
                        max_z = z
                        pixel_color = f1.colors[i]

            if pixel_color:
                img.putpixel((x, y), pixel_color)


    img.save("img.png")
    print("done!")