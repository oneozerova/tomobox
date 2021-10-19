import functools
import operator

import imageio
import numpy
import scipy as scipy
import scipy.misc
import numpy as np
import math
import random
from pygame.locals import *
import math

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import cv2

img_arr = cv2.imread('80p_unicorn.jpg', 1)

"""imgArray = numpy.array(img_resized) 
cv2.imwrite("test.png",imgArray)
#converts array to image again
"""

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

position = []

string_num = 1
pixel_num = 1

#string its y!
#print(string_num, pixel_num//string_num)

for string in img_arr:
    for pixel in string:
        if int(int(pixel[0])+int(pixel[1])+int(pixel[2])) != 0:
            position.append([pixel_num//string_num+pixel_num, string_num])
            print(pixel_num//string_num+pixel_num, string_num) #x and y
        pixel_num += 1
    string_num += 1
    pixel_num = 1

def Main_cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        glColor3fv((1, 1, 1))
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])

    glEnd()
print(position)
