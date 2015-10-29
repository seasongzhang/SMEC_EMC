import Image

RED = (255,0,0,255)
BLUE = (0,255,255,255)

im = Image.open(r"E:\Workspace\Python27\SMEC_EMC_FIG\TestData\fig1.png")
im_data = im.getdata()
width = im.size[0]
height = im.size[1]
data_list = []

red_list = []
blue_list = []
for n in range(len(im_data)):
    if im_data[n] == RED:
        #print im_data[n]
        red_list.append((n / width, n % width))
    elif im_data[n] == BLUE:
        blue_list.append((n / width, n % width))

for (x,y) in blue_list:
    im.putpixel((x/2,y/2),RED)

im.show()
        #data_set = set(data_list)

#im.show()
count = 0
print im.format,im.size,im.mode

pixel_set = []

#for h in range(height):
#    for w in range(width):
#        pixel = im.getpixel((w,h))
#        if pixel not in pixel_set:
#            pixel_set.append(pixel)
#            print pixel

#print pixel_set


pass
#im.show()

