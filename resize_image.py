from PIL import Image

img = Image.open('binary_unicorn.jpg')
new_img = img.resize((80, 80))
new_img.save("80p_unicorn.jpg", "JPEG", optimize=True)
