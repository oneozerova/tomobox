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


def set_vertices():
    x_value_change = random.randrange(-10, 10)
    y_value_change = random.randrange(-10, 10)
    z_value_change = random.randrange(-10, 10)

    new_vertices = []

    for vert in verticies:
        new_vert = []

        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change

        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert)

    return new_vertices


def Cube(verticies):
    glBegin(GL_QUADS)

    for surface in surfaces:
        x = 0

        for vertex in surface:
            x += 1
            glColor3fv((1, 1, 1))
            glVertex3fv(verticies[vertex])

    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def Main_cube():
    drawText(140, 120, "cube")
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

def drawText(x, y, text):
    font = pygame.font.SysFont('arial', 64)
    textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    # glTranslatef(5.0, 5.0, -30) x and y !!! HERE
    glTranslatef(random.randrange(-3, 3), random.randrange(-3, 3), -40)
    # glRotatef(0, 0, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glRotatef(1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Main_cube()
        # glTranslatef(5.0, 5.0, 0.0)
        pygame.display.flip()
        pygame.time.wait(10)


main()
