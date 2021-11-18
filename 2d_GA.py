import random

import numpy
from PIL import Image


def makeBlackWhite(img):  # from rgb to binary
    pixelmap = img.load()  # image is a pixel array [x, y], for example img.load[25,24] = (100, 188, 187)
    for i in range(img.size[0]):  # for string(x)
        for j in range(img.size[1]):  # for column(y)
            if sum(pixelmap[i, j]) > 255:
                pixelmap[i, j] = (255, 255, 255)  # img.load[25, 24] = (255, 255, 255)
            else:
                pixelmap[i, j] = (0, 0, 0)


def makeBlackFrame(old_img, frameSize, imageSize):  # old_img is binary img, frameSize=1, imageSize=60
    new_im = Image.new("RGB", (imageSize, imageSize))  # new image (default is black)
    new_im.paste(old_img, (frameSize, frameSize))  # binary image(smaller size) + new img(bigger size) = img in frame
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


def makeCircle(radius, imageSize):  # radius = 15
    midi = imageSize // 2  # 30
    midj = imageSize // 2
    new_im = Image.new("RGB", (imageSize, imageSize))
    pxm = new_im.load()
    for i in range(imageSize):
        for j in range(imageSize):
            i0 = i - midi
            j0 = j - midj
            if i0 * i0 + j0 * j0 < radius * radius:
                pxm[i, j] = (255, 255, 255)
    return new_im


class Evolution:
    @staticmethod
    def mutation(imageB, numberMutants):  # ImageB = circle, 20
        size = imageB.size  # (60, 60)
        pxmB = imageB.load()
        borderBlackPixels = {1: [], 2: [], 3: [], 4: []}
        borderWhitePixels = {1: [], 2: [], 3: [], 4: []}
        for i in range(size[0]):
            for j in range(size[1]):
                k = 0
                a = 0
                for d in [(-1, 0), (1, 0), (0, -1), (0, +1)]:
                    i0 = i + d[0]
                    j0 = j + d[1]
                    if 0 <= i0 < size[0] and 0 <= j0 < size[1] and pxmB[i, j] != pxmB[i0, j0]:
                        k += 1
                        a += d[0] + d[1] * 10
                if k == 2 and a == 0:  # two pixels on opposite sides
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
        return mutants # 20 imgs of circle

    @staticmethod
    def getScore(imageA, imageB):
        size = imageA.size
        pxmA = imageA.load()
        pxmB = imageB.load()
        score = 0
        for i in range(size[0]):
            for j in range(size[1]):
                score += (pxmA[i, j] == pxmB[i, j])
        return score

    @staticmethod
    def evaluation(imageA, imagesB): # ImagesB = 20 img of circle
        return [Evolution.getScore(imageA, imageB) for imageB in imagesB]

    @staticmethod
    def run(imageA, imageB, epochs, numberMutants):  # ImageA = img(binary); ImageB = circle;
        # epochs = 1000, numberMutants = 20
        k = epochs // 10  # 100
        for epoch in range(epochs):
            mutants = Evolution.mutation(imageB, numberMutants)
            scores = Evolution.evaluation(imageA, mutants)
            bestScoreIndex = 0
            for scoreIndex in range(1, len(scores)):  # len(scores) = 20
                if scores[bestScoreIndex] < scores[scoreIndex]:
                    bestScoreIndex = scoreIndex
            imageB = mutants[bestScoreIndex]  # the best generated circle(ImageB)
            if (epoch + 1) % k == 0:
                removeIslands(imageB)
                imageB.save(f"2d_GA_imgs/result_epoch{epoch + 1}.jpg")
                print(f"Epoch {epoch + 1} is done")
        removeIslands(imageB)
        return imageB


if __name__ == "__main__":
    __filename = "2d_GA_imgs/test.jpeg"
    __imageSize = 60
    __circleRadius = __imageSize // 4
    __frameSize = 1
    __epochs = 1000
    __mutants = 20
    originalImg = Image.open(__filename)
    img = originalImg.resize((__imageSize - 2 * __frameSize, __imageSize - 2 * __frameSize), Image.ANTIALIAS)
    makeBlackWhite(img)
    img = makeBlackFrame(img, __frameSize, __imageSize)
    removeIslands(img)
    circleImg = makeCircle(__circleRadius, __imageSize)
    img.save("original.jpg")
    px = img.load()
    print(px[15, 12])
    # circleImg.show()
    #result = Evolution.run(img, circleImg, __epochs, __mutants)
   # result.save("result_final.jpg")