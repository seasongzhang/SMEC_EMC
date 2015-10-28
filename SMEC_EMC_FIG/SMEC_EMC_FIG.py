import Image

im = Image.open(r"E:\Workspace\Python27\SMEC_EMC_FIG\TestData\fig1.png")
width = im.size[0]
height = im.size[1]

count = 0

for h in range(height):
    for w in range(width):
        pixel = im.getpixel((w,h))
        if not pixel == (0,0,0,0):
            print pixel


pass
#im.show()

