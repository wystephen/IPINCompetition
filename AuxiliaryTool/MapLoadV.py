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

import os

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
                  os.listdir(self.file_dir))


        # Load picture and parameters
        self.picture_info_list = list() # name of map picture : '*.jpg'
        self.picture_list = list() # picture (numpy.narray)
        self.para_array_list = list() # parameters ( latidude( in degrees), longitude(in degrees), rotation(in degrees), scale(meters/pixel))



