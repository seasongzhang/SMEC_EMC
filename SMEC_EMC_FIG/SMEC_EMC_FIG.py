from __future__ import print_function
from PIL import Image
import pickle
import os,re
import numpy
import matplotlib.pyplot as pl
#pl.rcParams['font.sans-serif'] = ['SimHei'] # For plotting Chinese characters



class EmcSpecPng:

    COLOR_LIMIT = (255,0,0,255)
    COLOR_SPECTRUM = (0,255,255,255)
    GREEN = (0,255,0,255)
    CROP_BOX = (321,734,2300,2138) #
    HEIGHT_DB = 120.0

    def __init__(self, file_path):
        self.file_path = file_path
        self.im = Image.open(self.file_path)
    #TODO:
    
    def size_check(self):
        assert self.im.size[0] == 3197
        assert self.im.size[1] == 2455
        
    def read_data(self):
        "Read image(png) into python and crop useful window and name it 'region'."

        region = self.im.crop(EmcSpecPng.CROP_BOX)
        region_data = list(region.getdata()) # get RGB value for each pixel
        width = region.size[0] 
        height = region.size[1]
        pixels_per_dB = height / EmcSpecPng.HEIGHT_DB

        #region.show()
        
        """According to RGB value of pixels, select pixels of limit named limit_list
        and spectrum named peak_value_list. Since region.getdata() get pixels line by line,
        so the limit_list and peak_list are not lined in frequency sequence. Thus sort() is 
        used to sort. Besides, we only care about the max spectrum point for each frequency 
        point, thus pick_max_point() is applied.
        """
        data_list = []
        limit_list = []
        peak_list = []

        #for n in range(len(region_data)):
        #    if region_data[n] == EmcSpecPng.COLOR_LIMIT:
        #        limit_list.append((n % width, n // width))
        #    elif region_data[n] == EmcSpecPng.COLOR_SPECTRUM:
        #        peak_list.append((n % width, n // width))

        #with open("limit_list.pkl",'wb') as f:
        #    pickle.dump(limit_list,f)
        #with open("peak_list.pkl","wb") as f:
        #    pickle.dump(peak_list,f)

        with open("limit_list.pkl",'rb') as f:
            limit_list = pickle.load(f)
        with open("peak_list.pkl","rb") as f:
            peak_list = pickle.load(f)

        peak_list.sort()
        limit_list.sort()

        def pick_max_point(xy_list):
            xy_max_list = []
            x_list = []
            for (x,y) in xy_list:
                if x not in x_list:
                    x_list.append(x)
                    xy_max_list.append((x,y))
            return xy_max_list

        peak_list = pick_max_point(peak_list)        

        for (x,y) in peak_list:
            region.putpixel((x,y), EmcSpecPng.GREEN)

        for (x,y) in limit_list:
            region.putpixel((x,y), EmcSpecPng.GREEN)

        "Transfer spectrum from pixel data to regular data, x-axis is MHz, y-axis is dB"
        self.raw_spectrum = [(10**(xy[0]/1300.0)*30,(46 - (xy[1]-632)/pixels_per_dB)) for xy in peak_list]
        
    def dump2txt(self):
        with open(os.path.splitext(self.file_path)[0] + ".txt", "w") as f:
            for sp in self.raw_spectrum:
                print('%(freq).2f %(dB).2f' % {'freq':sp[0],'dB':sp[1]},file=f,sep='')

    def dump2fig(self):
        pl.figure()
        fig_name = os.path.splitext(self.file_path)[0] + "_plot.png"
        #data_len = len(self.raw_spectrum[0])
        plot_data = numpy.transpose(self.raw_spectrum)
        plot_data = list(plot_data)
        pl.semilogx(plot_data[0],plot_data[1],basex = 10)
        pl.title("AAA")
        pl.xlim(plot_data[0][0],plot_data[0][-1])
        pl.ylim(-20,100)
        pl.axhline(y=46, xmin=0, xmax=0.8846, color = 'r')
        pl.axhline(y=53, xmin=0.8846, xmax=1, color = 'r')
        pl.axvline(x=230, ymin=0.55, ymax=0.6083, color = 'r')
        pl.xlabel("Frequency")
        pl.ylabel("Level")
        pl.grid(b=True,which='both')
        pl.savefig(fig_name)

if __name__ == "__main__":
    dir_path = u"E:\Tasks\EMC\P1_Test"
    files = os.listdir(dir_path)
    for file in files:
        file_path = os.path.join(dir_path,file)
        if re.search(u"P1_1.png",file):
            print("Processing "+file)
            png = EmcSpecPng(file_path)
            try:
                png.size_check()
            except AssertionError:
                print("Png size not corrected!")
            else:
                png.read_data()
                #png.dump2txt()
                png.dump2fig()
