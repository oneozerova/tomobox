import os
import random
import pygame as pg

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from os.path import isfile, join

cubeVertices = ((1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1))
cubeQuads = ((0, 3, 6, 4), (2, 5, 6, 3), (1, 2, 5, 7), (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))


class VoxelMap:
    def __init__(self, n=5, bmap=None):
        self.n = n
        if bmap is None:
            self.bmap = [[[False for _ in range(n)] for _ in range(n)] for _ in range(n)]
        else:
            self.bmap = bmap

    def drawSphere(self):
        r = self.n // 3
        r2 = r * r
        n2 = self.n // 2
        for i in range(self.n):
            ii = (i - n2) * (i - n2)
            for j in range(self.n):
                jj = (j - n2) * (j - n2)
                for k in range(self.n):
                    kk = (k - n2) * (k - n2)
                    self.bmap[i][j][k] = (ii + jj + kk) <= r2
        print(self.bmap)


    def draw(self):
        for i in range(self.n):
            for j in range(self.n):
                for k in range(self.n):
                    if not self.bmap[i][j][k]:
                        continue
                    glBegin(GL_QUADS)
                    for cubeQuad in cubeQuads:
                        for cubeVertex in cubeQuad:
                            glVertex3fv([
                                (cubeVertices[cubeVertex][0] + (i - self.n // 2)),
                                (cubeVertices[cubeVertex][1] + (j - self.n // 2)),
                                (cubeVertices[cubeVertex][2] + (k - self.n // 2))
                            ])
                    glEnd()

def draw_main():
    voxels = VoxelMap(12)
    voxels.drawSphere()
    pg.init()
    display = (640, 640)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)

    glClearColor(0.0, 0.0, 0.0, 0.0)

    glTranslatef(0.0, 0.0, -50)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glRotatef(5, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        voxels.draw()
        pg.display.flip()
        pg.time.wait(10)
draw_main()

