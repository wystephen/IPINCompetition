# -*- coding:utf-8 -*-
# carete by steve at  2018 / 09 / 01　下午4:24
'''
                   _ooOoo_ 
                  o8888888o 
                  88" . "88 
                  (| -_- |) 
                  O\  =  /O 
               ____/`---'\____ 
             .'  \\|     |//  `. 
            /  \\|||  :  |||//  \ 
           /  _||||| -:- |||||-  \ 
           |   | \\\  -  /// |   | 
           | \_|  ''\---/''  |   | 
           \  .-\__  `-`  ___/-. / 
         ___`. .'  /--.--\  `. . __ 
      ."" '<  `.___\_<|>_/___.'  >'"". 
     | | :  `- \`.;`\ _ /`;.`/ - ` : | | 
     \  \ `-.   \_ __\ /__ _/   .-` /  / 
======`-.____`-.___\_____/___.-`____.-'====== 
                   `=---=' 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
         佛祖保佑       永无BUG 
'''


import matplotlib.pyplot as plt
import numpy as np

import os

from scipy.misc import imread

class MapLoader:
    def __init__(self, file_dir):
        if file_dir[-1] == '/':
            self.file_dir = file_dir
        else:
            self.file_dir = file_dir + '/'


        # Read calibration file which contained picture name and relative parameters.
        self.calib_file_name  = 'None'

        for file_name in os.listdir(self.file_dir):
            if '.cal' in file_name:
                self.calib_file_name = self.file_dir + file_name

        if self.calib_file_name is 'None':
            print('Can not find out a calib file for build up image, the file dir is :\n',
                  self.file_dir,
                  '\n the files in such directory are:\n',
                  os.listdir(self.file_dir),
                  'current value of self.calib_file_name is :\n',
                  self.calib_file_name)


        # Load picture and parameters
        self.picture_info_array = np.loadtxt(self.calib_file_name,comments='%',dtype=np.str).transpose().reshape([-1,7])
        '''
        % A building is composed of several floors. Each floor has 6 calibration data:
        % 1) the filename of the bitmap
        % 2) the floor number (e.g. -2, 0, 3)
        % 3) the Building number (e.g. 1, 2, 3)
        % 4) Latidude (in degrees) of image center, 
        % 5) Longitude (in degrees) of image center, 
        % 6) Rotation (in degrees) of image to be aligned to the geometric north
        % 7) Scale (meters/pixel).

        '''
        print(self.picture_info_array)

        self.picture_list = list() # picture (numpy.narray)

        for i in range(self.picture_info_array.shape[0]):
            tmp_pic = imread(self.file_dir + self.picture_info_array[i,0])
            self.picture_list.append(tmp_pic)







if __name__ == '__main__':
    # ml = MapLoader('/home/steve/Data/IPIN2017Data/Track3/Map/CAR')
    # ml = MapLoader('/home/steve/Data/IPIN2017Data/Track3/Map/UJITI')
    ml = MapLoader('/home/steve/Data/IPIN2017Data/Track3/Map/UJIUB')
    print(ml.picture_info_array)

    # plt.figure()
    # plt.imshow(ml.picture_list[0])
    # plt.show()
    for i, pic in enumerate(ml.picture_list):
        plt.figure(i+1)
        plt.imshow(pic)
    plt.show()




