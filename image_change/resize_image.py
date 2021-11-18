from PIL import Image

img = Image.open('images/binary_unicorn4.jpg')
new_img = img.resize((80, 80))
new_img.save("images/80p_unicorn4.jpg", "JPEG", optimize=True)
