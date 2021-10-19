import math
import random
from pygame.locals import *

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

main_verticies = (
    (4, -4, -4),
    (4, 4, -4),
    (-4, 4, -4),
    (-4, -4, -4),
    (4, -4, 4),
    (4, 4, 4),
    (-4, -4, 4),
    (-4, 4, 4)
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


def Main_cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        glColor3fv((1, 1, 1))
        for vertex in surface:
            glVertex3fv(main_verticies[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(main_verticies[vertex])

    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(5.0, 5.0, -30) #x and y !!! HERE
    #glTranslatef(random.randrange(-3, 3), random.randrange(-3, 3), -40)
    # glRotatef(0, 0, 0, 0)

    # glTranslatef(0.0, 0.0, 1.0)
    # glTranslatef(0.0, 0.0, .50)
    glRotatef(1, 0, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Main_cube()
    # glTranslatef(5.0, 5.0, 0.0)
    pygame.display.flip()
    pygame.time.wait(10)


main()
