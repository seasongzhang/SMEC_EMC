import Image
import pickle

RED = (255,0,0,255)
BLUE = (0,255,255,255)

im = Image.open(r"d:\Workspace\Python27\SMEC_EMC_FIG\TestData\fig1.png")
im_data = list(im.getdata())
width = im.size[0]
height = im.size[1]

data_list = []
#red_list = []
#blue_list = []
#for n in range(len(im_data)):
#    if im_data[n] == RED:
#        #print im_data[n]
#        red_list.append((n % width, n / width))
#    elif im_data[n] == BLUE:
#        blue_list.append((n % width, n / width))

#with open("red_list.pkl",'wb') as f:
#    pickle.dump(red_list,f)
#with open("blue_list.pkl","wb") as f:
#    pickle.dump(blue_list,f)

with open("red_list.pkl",'rb') as f:
    red_list = pickle.load(f)
with open("blue_list.pkl","rb") as f:
    blue_list = pickle.load(f)

blue_list.sort()
red_list.sort()

def pickMaxPoints(xy_list):
    xy_max_list = []
    x_list = []
    for (x,y) in xy_list:
        cc = (x,y)
        if x not in x_list:
            x_list.append(x)
            xy_max_list.append((x,y))
    return xy_max_list

blue_list2 = pickMaxPoints(blue_list)        

for (x,y) in blue_list2:
    im.putpixel((x,y),RED)

for (x,y) in red_list:
    im.putpixel((x,y),(0,255,0,255))

with open("blue_list.txt","w") as f:
    for xy in blue_list2:
        f.write(str(xy[0])+"\t"+str(xy[1])+"\n")

im.show()
