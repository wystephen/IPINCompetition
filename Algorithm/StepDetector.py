# -*- coding:utf-8 -*-
# carete by steve at  2018 / 09 / 02　下午3:00
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
import scipy as sp
import numpy as np

from AuxiliaryTool.LogLoader import LogLoader


class StepDetector:
    def __init__(self):
        self.counter = 0


if __name__ == '__main__':
    file_name = '/home/steve/Data/IPIN2017Data/Track3/01-Training/CAR/logfile_CAR_R02-2017_S4.txt'

    ll = LogLoader(file_name)

    acc = np.zeros([ll.acce.shape[0], 4])
    acc[:, 0] = ll.acce[:, 0]
    acc[:, 1:] = ll.acce[:, 2:5]

    # show time interval
    plt.figure()
    plt.plot(acc[1:, 0] - acc[:-1, 0])
    time_interval_array = acc[1:,0]-acc[:-1,0]

    # print(np.mean(time_interval_array),
    #       np.std(time_interval_array))

    #

    plt.figure()
    for i in range(1, 4):
        plt.plot(acc[:,0],acc[:,i])
    plt.grid()



    plt.show()
