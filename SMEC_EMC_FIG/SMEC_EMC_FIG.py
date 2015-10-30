from PIL import Image
import pickle


class EmcSpectrumPng:

    COLOR_LIMIT = (255,0,0,255)
    COLOR_SPECTRUM = (0,255,255,255)
    CROP_BOX = (321,734,2300,2138)
    HEIGHT_DB = 140

    def __init__(self, file_path):
        self.im = Image.open(file_path)
    #TODO:
        

    "Read image into python and crop useful window and name it 'region'."

    region = im.crop(CROP_BOX)
    region_data = list(region.getdata())
    width = region.size[0]
    height = region.size[1]
    pixels_per_dB = height / HEIGHT_DB

    #region.show()

    data_list = []
    red_list = []
    blue_list = []
    #for n in range(len(region_data)):
    #    if region_data[n] == RED:
    #        red_list.append((n % width, n // width))
    #    elif region_data[n] == BLUE:
    #        blue_list.append((n % width, n // width))

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
            if x not in x_list:
                x_list.append(x)
                xy_max_list.append((x,y))
        return xy_max_list

    blue_list = pickMaxPoints(blue_list)        

    for (x,y) in blue_list:
        region.putpixel((x,y),RED)

    for (x,y) in red_list:
        region.putpixel((x,y),(0,255,0,255))

    raw_spectrum = [(10**(xy[0]/1300)*30,(46 - (xy[1]-632)/pixels_per_dB)) for xy in blue_list]

    with open("blue_list.txt","w") as f:
        for xy in blue_data_dB:
            f.write(str(xy[0])+"\t"+str(xy[1])+"\n")

    region.show()
