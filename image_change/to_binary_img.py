from PIL import Image

im = Image.open(r"unicorn_other_side(frame152).jpg")
px = im.load()
for x in range(im.width):
    for y in range(im.height):
        if sum(px[x, y]) > 80*3:
            px[x, y] = (255, 255, 255)
        else:
            px[x, y] = (0, 0, 0)

<<<<<<< HEAD:to_binary_img.py
im.save("unicorn_other_side.out.jpg")
=======
im.save("binary_unicorn3.jpg")
>>>>>>> af43b9b... -:image_change/to_binary_img.py

"""import os

import cv2
from PIL import Image

a = 1
for i in range(0, 89):
    img = cv2.imread('unicorn_imgs/' + 'frame' + str(i) + '.jpg', 2)
    ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    bw = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite('binary_uni/' + str(a) + '.jpg', bw_img)
    a += 1
"""