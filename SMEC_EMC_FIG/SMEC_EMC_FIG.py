# -*- coding: utf-8 -*-

from __future__ import print_function
from PIL import Image
import pickle
import os
import re


# import numpy
# import matplotlib.pyplot as pl

class SpecReader:
    COLOR_LIMIT = (255, 0, 0, 255)
    COLOR_SPECTRUM = (0, 255, 255, 255)
    GREEN = (0, 255, 0, 255)
    CROP_BOX = (321, 734, 2300, 2138)
    HEIGHT_DB = 120.0

    def __init__(self):
        pass
        """
            Read png object from file_path.
        """

    def read_spec_from_png(self, file_path, save2txt=False):
        """
            Read image(png) into python and crop useful window and name it 'region'.
            :param save2txt:
            :return:
        """
        im = Image.open(file_path)

        assert im.size[0] == 3197
        assert im.size[1] == 2455

        region = im.crop(SpecReader.CROP_BOX)
        region_data = list(region.getdata())  # get RGB value for each pixel
        width = region.size[0]
        height = region.size[1]
        pixels_per_dB = height / SpecReader.HEIGHT_DB

        # region.show()

        """
            According to RGB value of pixels, select pixels of limit named limit_list
            and spectrum named peak_value_list. Since region.getdata() get pixels line by line,
            so the limit_list and peak_list are not lined in frequency sequence. Thus sort() is
            used to sort. Besides, we only care about the max spectrum point for each frequency
            point, thus pick_max_point() is applied.
        """
        data_list = []
        limit_list = []
        peak_list = []

        # Extract spectrum pixel and limit pixel from png seperately according RGB value
        for n in range(len(region_data)):
            if region_data[n] == SpecReader.COLOR_LIMIT:
                limit_list.append((n % width, n // width))
            elif region_data[n] == SpecReader.COLOR_SPECTRUM:
                peak_list.append((n % width, n // width))

        # with open("limit_list.pkl",'wb') as f:
        #    pickle.dump(limit_list,f)
        # with open("peak_list.pkl","wb") as f:
        #    pickle.dump(peak_list,f)

        # with open("limit_list.pkl", 'rb') as f:
        #     limit_list = pickle.load(f)
        # with open("peak_list.pkl", "rb") as f:
        #     peak_list = pickle.load(f)

        peak_list.sort()
        limit_list.sort()

        def pick_max_point(xy_list):
            xy_max_list = []
            x_list = []
            for (x, y) in xy_list:
                if x not in x_list:
                    x_list.append(x)
                    xy_max_list.append((x, y))
            return xy_max_list

        peak_list = pick_max_point(peak_list)  # for each frequency, only keep the max value.

        # "Transfer spectrum from pixel data to regular data, x-axis is MHz, y-axis is dB"
        decimal_spectrum = [(10 ** (xy[0] / 1300.0) * 30, (46 - (xy[1] - 632) / pixels_per_dB)) for xy in peak_list]

        # Write decimal_spectrum to a txt file
        if save2txt == True:
            with open(os.path.splitext(file_path)[0] + ".txt", "w") as f:
                for sp in decimal_spectrum:
                    print('%(freq).2f %(dB).2f' % {'freq': sp[0], 'dB': sp[1]}, file=f, sep='')

        return decimal_spectrum

    def gather_specs(self, dir_path, re_str=u'.png'):
        """
            Gather all the spectrum data in dir_path.
        :return:
        """
        decimal_specs = []
        files = [f for f in os.listdir(dir_path) if re.match(re_str, f)]
        try:
            files.sort(key=lambda n:int(n.split("_")[1].split('.')[0]))
        except IndexError:
            print("Png files not named corrected.")
        for file in files:
            file_path = os.path.join(dir_path, file)
            if re.search(re_str, file):
                print("Processing " + file)
                try:
                    decimal_specs.append(self.read_spec_from_png(file_path, save2txt=True))
                except AssertionError:
                    print("Png size not corrected! File path" + file_path)
        return decimal_specs

if __name__ == "__main__":
    pngset = SpecReader()
    x = pngset.gather_specs(ur'E:\SeaGit\SMEC_EMC_FIG\testdata\MPS1_P1_CAN\data', re_str='P1_.+\.png')
    with open(ur'E:\SeaGit\SMEC_EMC_FIG\testdata\MPS1_P1_CAN\data' + ur'\decimal_specs.pkl', 'wb') as f:
        pickle.dump(x, f)
