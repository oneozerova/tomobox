import glob

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
    def __init__(self, n, bmap):
        self.n = n
        if bmap is None:
            self.bmap = [[[False for _ in range(n)] for _ in range(n)] for _ in range(n)]
        else:
            self.bmap = bmap

    def draw_sphere(self):
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
                    # glColor3fv((1, 1, 1))
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
    i = 1
    for frame in glob.glob('images/frame*.jpg'):
        im = Image.open(frame).resize((imageSize - 2 * frameSize, imageSize - 2 * frameSize), Image.ANTIALIAS)
        makeBlackWhite(im)
        im = makeBlackFrame(im, frameSize, imageSize)
        removeIslands(im)
        if i % 2 == 0:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        imageList.append(im)
        i+=1
    return imageList


class Evolution:
    @staticmethod
    def mutation(sphere, numberMutants):  # ImageB = sphere, 20
        # size = (15, 15, 15)  # (30, 30, 30)
        borderBlackPixels = {1: [], 2: [], 3: [], 4: []}
        borderWhitePixels = {1: [], 2: [], 3: [], 4: []}
        trial = 0
        for i in range(30):  # -30 30
            for j in range(30):
                for k in range(30):
                    m = 0
                    a = 0
                    for d in [(-1, 0), (1, 0), (0, -1), (0, +1)]:
                        i0 = i + d[0]
                        j0 = j + d[1]
                        if 0 <= i0 < 30 and 0 <= j0 < 30 and sphere[i0][j0][k] != sphere[i][j][k]: # -30 30
                            trial += 1
                            m += 1
                            a += d[0] + d[1] * 10
                    if m == 2 and a == 0:  # two voxels on opposite sides
                        continue
                    if 1 <= m <= 3:
                        if sphere[i][j][k] == False:  # black
                            borderBlackPixels[m].append((i, j, k))  # black pixels surrounded by whites
                        else:
                            borderWhitePixels[m].append((i, j, k))
        print(trial)
        for i, j, k in borderBlackPixels[4]:
            sphere[i][j][k] = True  # change color if the pix is surrounded by only one color
        for i, j, k in borderWhitePixels[4]:
            sphere[i][j][k] = False
        m = 0
        mutants = [sphere.copy() for i in range(numberMutants)]  # len(mutants) = 20
        a = borderBlackPixels[1] + borderBlackPixels[2] + borderBlackPixels[3]
        # a = [(15, 25), (15, 26), (15, 27), (15, 28), (15, 29), (15, 30), ... ]
        for i, j, k in random.sample(a, min(len(a), numberMutants // 2)):
            # random 10 or len(a) items from a
            # for example [(29, 45), (24, 16), (26, 15), (45, 31), (16, 37),
            # (24, 44), (36, 44), (45, 26), (15, 31), (32, 15)]
            mutants[m][i][j][k] = True  # add(replace) black to(with) white
            m += 1
        a = borderWhitePixels[1] + borderWhitePixels[2] + borderWhitePixels[3]
        for i, j, k in random.sample(a, min(len(a), numberMutants - numberMutants // 2)):
            mutants[m][i][j][k] = False
            m += 1
        return mutants  # 20 imgs of circle

    @staticmethod
    def getScore(sphere):
        image_list = get_images(60, 1)
        # size = imageA.size
        # pxmA = imageA.load()
        pxmB = sphere
        score = 0
        for i in range(30):  # -30 30
            for j in range(30):
                for k in range(30):
                    if i <= 15 and k <= 15:
                        pxmA = image_list[0].load()
                    elif i >= 15 and k <= 15:
                        pxmA = image_list[1].load()
                    elif i <= 15 and k >= 15:
                        pxmA = image_list[2].load()
                    else:
                        pxmA = image_list[3].load()
                    # px = image_list[0].load()
                    if pxmA[i, j] == (0, 0, 0):
                        px = False
                    else:
                        px = True
                    score += (px == pxmB[i][j][k])
        return score  # have to change (?)

    @staticmethod
    def evaluation(sphereS):  # ImagesB = 20 img of circle
        return [Evolution.getScore(sphere) for sphere in sphereS]

    @staticmethod
    def run(sphere, epochs, numberMutants):  # ImageA = img(binary); ImageB = circle;
        # epochs = 1000, numberMutants = 20
        k = epochs // 10  # 100
        for epoch in range(epochs):
            mutants = Evolution.mutation(sphere, numberMutants)
            scores = Evolution.evaluation(mutants)
            bestScoreIndex = 0
            for scoreIndex in range(1, len(scores)):  # len(scores) = 20
                if scores[bestScoreIndex] < scores[scoreIndex]:
                    bestScoreIndex = scoreIndex
            sphere = mutants[bestScoreIndex]  # the best generated circle(ImageB)
            if (epoch + 1) % k == 0:
                # removeIslands(imageB)
                # imageB.save(f"2d_GA_imgs/result_epoch{epoch + 1}.jpg")
                print(f"Epoch {epoch + 1} is done")
        # removeIslands(imageB)
        return sphere


def main():
    __imageSize = 30
    __frameSize = 1
    __epochs = 1000 # 1000 23:43 -- 0:48
    __mutants = 20
    image_list = get_images(__imageSize, __frameSize)
    im = image_list[0].load()
    voxels = VoxelMap(30, None)
    sphere = voxels.draw_sphere()
    result = Evolution.run(sphere, __epochs, __mutants)
    #print(result)
    pygame.init()
    display = (720, 720)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(60, (display[0] / display[1]), 1, 256.0)
    #gluPerspective(45, (display[0] / display[1]), 0.1, 70.0)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, -50)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(10, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        voxels = VoxelMap(30, result)
        voxels.draw()
        pygame.display.flip()
        pygame.time.wait(10)


main()
