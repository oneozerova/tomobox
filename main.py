import random
import pygame as pg

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from os import listdir
from os.path import isfile, join


cubeVertices = ((1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1))
cubeQuads = ((0, 3, 6, 4), (2, 5, 6, 3), (1, 2, 5, 7), (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))


class VoxelMap:
    def __init__(self, n=32, bmap=None):
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

    @staticmethod
    def getRandomDot(n):
        return random.randint(0, n), random.randint(0, n), random.randint(0, n)

    @staticmethod
    def __mutate(bmap, pointTrue, pointFalse):
        if random.random() < 0.5:  # add
            bmap[pointFalse[0]][pointFalse[1]][pointFalse[2]] = True
        else:  # delete
            bmap[pointTrue[0]][pointTrue[1]][pointTrue[2]] = False

    def mutate(self):
        x, y, z = VoxelMap.getRandomDot(self.n)
        while True:
            while not self.bmap[x][y][z]:
                x, y, z = VoxelMap.getRandomDot(self.n)
            i = 1
            while True:
                n = 0
                results = []
                if x + i < self.n:
                    results.append(self.bmap[x + i][y][z])
                else:
                    n += 1
                    results.append(True)
                if 0 <= x - i:
                    results.append(self.bmap[x - i][y][z])
                else:
                    n += 1
                    results.append(True)
                if y + i < self.n:
                    results.append(self.bmap[x][y + i][z])
                else:
                    n += 1
                    results.append(True)
                if 0 <= y - i:
                    results.append(self.bmap[x][y - i][z])
                else:
                    n += 1
                    results.append(True)
                if z + i < self.n:
                    results.append(self.bmap[x][y][z + i])
                else:
                    n += 1
                    results.append(True)
                if 0 <= z - i:
                    results.append(self.bmap[x][y][z - i])
                else:
                    n += 1
                    results.append(True)
                if n == 6:
                    break
                if sum(results) != 6:
                    x = random.choice([j for j in range(6) if not results[j]])
                    bmap = [[[self.bmap[ii][jj][kk] for kk in range(n)] for jj in range(n)] for ii in range(n)]
                    if x == 0:
                        VoxelMap.__mutate(bmap, (x + i - 1, y, z), (x + i, y, z))
                    elif x == 1:
                        VoxelMap.__mutate(bmap, (x - i + 1, y, z), (x - i, y, z))
                    elif x == 2:
                        VoxelMap.__mutate(bmap, (x, y + i - 1, z), (x, y + i, z))
                    elif x == 3:
                        VoxelMap.__mutate(bmap, (x, y - i + 1, z), (x, y - i, z))
                    elif x == 4:
                        VoxelMap.__mutate(bmap, (x, y, z + i - 1), (x, y, z + i))
                    else:
                        VoxelMap.__mutate(bmap, (x, y, z - i + 1), (x, y, z - i))
                    return VoxelMap(self.n, bmap)
                i += 1

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


def getFiles(folder):
    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    indexfiles = [(int(file[len("frame"):-len(".jpg")]), file) for file in files]
    indexfiles.sort()
    return {(i * 360 // len(indexfiles)): indexfiles[i][1]
            for i in range(len(indexfiles))}


# degree2file = getFiles("imgs/cube/")
# print(degree2file)

def main():
    voxels = VoxelMap(12)
    voxels.drawSphere()
    pg.init()
    display = (640, 640)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 70.0)

    glClearColor(0.0, 0.0, 0.0, 0.0)

    # glShadeModel(GL_SMOOTH)
    #
    # glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    # glMaterialfv(GL_FRONT, GL_SHININESS, 50.0)
    # glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))
    #
    # glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    # glEnable(GL_DEPTH_TEST)

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


if __name__ == "__main__":
    main()
