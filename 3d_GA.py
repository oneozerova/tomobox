import glob
import os
from os.path import isfile, join

import numpy
from PIL import Image
import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

cubeVertices = ((1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1))
cubeQuads = ((0, 3, 6, 4), (2, 5, 6, 3), (1, 2, 5, 7), (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))


class VoxelMap:
    def __init__(self, n, bmap=None):
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
        return self.bmap

    def draw(self):
        for i in range(self.n):
            for j in range(self.n):
                for k in range(self.n):
                    if not self.bmap[i][j][k]:
                        continue
                    glBegin(GL_QUADS)
                    if set_quarter(self, i, k) == 1:
                        glColor3fv((0, 1, 0))
                    elif set_quarter(self, i, k) == 2:
                        glColor3fv((0, 1, 1))
                    elif set_quarter(self, i, k) == 3:
                        glColor3fv((1, 0, 0))
                    else:
                        glColor3fv((1, 1, 0))
                    for cubeQuad in cubeQuads:
                        for cubeVertex in cubeQuad:
                            glVertex3fv([
                                (cubeVertices[cubeVertex][0] + (i - self.n // 2)),
                                (cubeVertices[cubeVertex][1] + (j - self.n // 2)),
                                (cubeVertices[cubeVertex][2] + (k - self.n // 2))
                            ])
                    glEnd()


def set_quarter(self, i, k):
    if i <= self.n // 2 and k <= self.n // 2:
        return 1
    elif i >= self.n // 2 and k <= self.n // 2:
        return 2
    elif i <= self.n // 2 and k >= self.n // 2:
        return 3
    else:
        return 4


def makeBlackWhite(img):
    pixelmap = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if sum(pixelmap[i, j]) > 255:
                pixelmap[i, j] = (255, 255, 255)
            else:
                pixelmap[i, j] = (0, 0, 0)


def makeBlackFrame(old_img, frameSize, imageSize):
    new_im = Image.new("RGB", (imageSize, imageSize))
    new_im.paste(old_img, (frameSize, frameSize))
    return new_im


def breadthFirstSearch(pxm, p, size, visited):  # pxm = img.load(), p = (i, j), size = img.size (60,60)
    buffer = [(p, p)]  # for example [((2, 3), (2, 3))] if p = (2, 3)
    visited[p] = True  # in 2nd string (from 0) and in 3rd column False replace with True
    n = 0
    while len(buffer) != 0:
        p0, p1 = buffer.pop()  # default index is -1
        # p0 = (2, 3), p1 = (2, 3); buffer is empty []
        n += 1
        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # coordinates
            p2 = (p1[0] + d[0], p1[1] + d[1])  # square verticles?: p2 = (1, 3); (3, 3); (2, 2); (2, 4)
            if 0 <= p2[0] < size[0] and 0 <= p2[1] < size[1] and visited[p2] == False and pxm[p1] == pxm[p2]:
                # 1 < 60 and 3 < 60 and (1, 3) == False and
                # pxm[(2, 3)] == pxm[(1, 3)] --> (255, 255, 255) == (255, 255, 255)
                buffer.append((p1, p2))  # [(2, 3), (1, 3)]
                visited[p2] = True
    return n


def breadthFirstFill(pxm, p, size, visited, color):
    buffer = [(p, p)]
    visited[p] = True
    while len(buffer) != 0:
        p0, p1 = buffer.pop()
        for d in [(-1, 0), (1, 0), (0, -1), (0, +1)]:
            p2 = (p1[0] + d[0], p1[1] + d[1])
            if 0 <= p2[0] < size[0] and 0 <= p2[1] < size[1] and visited[p2] == False and pxm[p1] == pxm[p2]:
                buffer.append((p1, p2))
                visited[p2] = True
        pxm[p1] = color


def removeIslands(image):  # image = image in frame
    size = image.size  # return amount of x pixels and y pixels as tuple
    pxm = image.load()
    visited = numpy.full(size, False)  # new array in shape of size (x, y) filled with False
    blackIslands = []
    whiteIslands = []
    for i in range(size[0]):  # for i in x
        for j in range(size[1]):  # for j in y
            if visited[i, j]:  # False
                continue
            k = breadthFirstSearch(pxm, (i, j), size, visited)
            if pxm[i, j] == (0, 0, 0):  # black
                blackIslands.append((k, i, j))
            else:
                whiteIslands.append((k, i, j))
    visited = numpy.full(size, False)
    blackIslands.sort()  # [(3, 38, 39), (3150, 0, 0)]
    for i in range(len(blackIslands) - 1):
        breadthFirstFill(pxm, (blackIslands[i][1], blackIslands[i][2]), size, visited,
                         (255, 255, 255))  # make them white
    whiteIslands.sort()  # [(1, 19, 38), (1, 34, 20), (445, 20, 32)]
    for i in range(len(whiteIslands) - 1):
        breadthFirstFill(pxm, (whiteIslands[i][1], whiteIslands[i][2]), size, visited, (0, 0, 0))  # make them black


def get_images(imageSize, frameSize):
    imageList = []
    for frame in glob.glob('images/frame*.jpg'):
        im = Image.open(frame).resize((imageSize - 2 * frameSize, imageSize - 2 * frameSize), Image.ANTIALIAS)
        makeBlackWhite(im)
        im = makeBlackFrame(im, frameSize, imageSize)
        removeIslands(im)
        imageList.append(im)
    return imageList


class Evolution:
    @staticmethod
    def mutation(sphere, numberMutants):  # ImageB = circle, 20
        size = (30, 30, 30)  # (30, 30, 30)
        borderBlackPixels = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        borderWhitePixels = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        for i in range(size[0]):
            for j in range(size[1]):
                for k in range(size[2]):
                    k = 0
                    a = 0
                    for d in [(-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, +1, 1), (-1, 0, -1), (1, 0, -1), (0, -1, -1),
                              (0, +1, -1)]:
                        i0 = i + d[0]
                        j0 = j + d[1]
                        k0 = k + d[2]
                        if 0 <= i0 < size[0] and 0 <= j0 < size[1] and 0 <= k0 < size[2] and sphere[i, j, k] != sphere[
                            i0, j0, k0]:
                            k += 1
                            a += d[0] + d[1] * 10
                    if k == 2 and a == 0 :  # two pixels on opposite sides
                        continue
                    if 1 <= k <= 3:
                        if pxmB[i, j] == (0, 0, 0):  # black
                            borderBlackPixels[k].append((i, j))  # black pixels surrounded by whites
                        else:
                            borderWhitePixels[k].append((i, j))
        for i, j in borderBlackPixels[4]:
            pxmB[i, j] = (255, 255, 255)  # change color if the pix is surrounded by only one color
        for i, j in borderWhitePixels[4]:
            pxmB[i, j] = (0, 0, 0)
        k = 0
        mutants = [imageB.copy() for i in range(numberMutants)]  # len(mutants) = 20
        a = borderBlackPixels[1] + borderBlackPixels[2] + borderBlackPixels[3]
        # a = [(15, 25), (15, 26), (15, 27), (15, 28), (15, 29), (15, 30), ... ]
        for i, j in random.sample(a, min(len(a), numberMutants // 2)):
            # random 10 or len(a) items from a
            # for example [(29, 45), (24, 16), (26, 15), (45, 31), (16, 37),
            # (24, 44), (36, 44), (45, 26), (15, 31), (32, 15)]
            mutants[k].putpixel((i, j), (255, 255, 255))  # add(replace) black to(with) white
            k += 1
        a = borderWhitePixels[1] + borderWhitePixels[2] + borderWhitePixels[3]
        for i, j in random.sample(a, min(len(a), numberMutants - numberMutants // 2)):
            mutants[k].putpixel((i, j), (0, 0, 0))
            k += 1
        return mutants  # 20 imgs of circle


def main():
    __imageSize = 60
    __frameSize = 1
    __mutants = 20
    get_images(__imageSize, __frameSize)
    voxels = VoxelMap(30)
    sphere = voxels.drawSphere()
    k = 0
    for i in range(2):
        for j in range(2):
            for k in range(2):
                print(len(sphere[i][j]))
                k += 1
    print(k)
    # result = Evolution.mutation(sphere, __mutants)
    pygame.init()
    display = (640, 640)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, -50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(10, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        voxels.draw()
        pygame.display.flip()
        pygame.time.wait(10)


main()

"""if __name__ == "__main__":
    __1filename = "images/frame0.jpg"
    __2filename = "images/frame76.jpg"
    __3filename = "images/frame152.jpg"
    __4filename = "images/frame228.jpg"
    __imageSize = 60
    __circleRadius = __imageSize // 4
    __frameSize = 1
    __epochs = 1000
    __mutants = 20
    originalImg1 = Image.open(__1filename)
    img = originalImg.resize((__imageSize - 2 * __frameSize, __imageSize - 2 * __frameSize), Image.ANTIALIAS)
    makeBlackWhite(img)
    img = makeBlackFrame(img, __frameSize, __imageSize)
    removeIslands(img)
    circleImg = makeCircle(__circleRadius, __imageSize)
    img.save("original.jpg")
    # circleImg.show()
    result = Evolution.run(img, circleImg, __epochs, __mutants)
result.save("result_final.jpg")"""
