# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import os
import pickle
import re

from PIL import Image


class SpecReader:
    def __init__(self):
        pass
        """
            Read png object from file_path.
        """

    def read_spec_from_png(self, file_path, save2txt=False):
        """
            Read image(png) into python and crop useful window and name it 'region'.
            :type file_path:
            :param save2txt:
            :return:
        """
        COLOR_LIMIT = (255, 0, 0, 255)
        COLOR_SPECTRUM = (0, 255, 255, 255)
        CROP_BOX = (321, 734, 2300, 2138)
        HEIGHT_DB = 120.0

        im = Image.open(file_path)

        try:
            assert im.size[0] == 3197
            assert im.size[1] == 2455
        except AssertionError:
            pass

        region = im.crop(CROP_BOX)
        region_data = list(region.getdata())  # get RGB value for each pixel
        width = region.size[0]
        height = region.size[1]
        pixels_per_dB = height / HEIGHT_DB

        """
            According to RGB value of pixels, select pixels of limit named limit_list
            and spectrum named peak_value_list. Since region.getdata() get pixels line by line,
            so the limit_list and peak_list are not lined in frequency sequence. Thus sort() is
            used to sort. Besides, we only care about the max spectrum point for each frequency
            point, thus pick_max_point() is applied.
        """
        limit_list = []
        peak_list = []

        # Extract spectrum pixel and limit pixel from png seperately according RGB value
        for n in range(len(region_data)):
            if region_data[n] == COLOR_LIMIT:
                limit_list.append((n % width, n // width))
            elif region_data[n] == COLOR_SPECTRUM:
                peak_list.append((n % width, n // width))

        peak_list.sort()
        limit_list.sort()

        s = set([])
        peak_list = filter(lambda x: False if x[0] in s else s.add(x[0]) or True, peak_list)

        # "Transfer spectrum from pixel data to regular data, x-axis is MHz, y-axis is dB"
        decimal_spectrum = [(10 ** (xy[0] / 1300.0) * 30, (46 - (xy[1] - 632) / pixels_per_dB)) for xy in peak_list]

        # Write decimal_spectrum to a txt file
        if save2txt:
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
        files = [f for f in os.listdir(dir_path) if re.search(re_str, f)]
        try:
            files.sort(key=lambda n:int(n.split("_")[1].split('.')[0]))
        except IndexError:
            print("Png files not named corrected.")
        for file in files:
            file_path = os.path.join(dir_path, file)
            if re.search(re_str, file):
                print("Reading spectrum data from " + file)
                try:
                    decimal_specs.append(self.read_spec_from_png(file_path, save2txt=True))
                except AssertionError:
                    print("Png size not corrected! File path" + file_path)
        return decimal_specs

if __name__ == "__main__":
    pngset = SpecReader()
    x = pngset.gather_specs(ur'E:\SeaGit\SmecEmcReport\testdata\MPS1_P1_CAN\data', re_str='P1_.+\.png')
    with open(ur'E:\SeaGit\SmecEmcReport\testdata\MPS1_P1_CAN\data' + ur'\decimal_specs.pkl', 'wb') as f:
        pickle.dump(x, f)
