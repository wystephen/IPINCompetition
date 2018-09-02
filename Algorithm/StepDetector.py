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
        self.condidate_list = list()
        self.condidate_value = list()

        self.miu_alpha = 10.0
        self.sigma_alpha = 0.1
        self.alpha = 0.1

    def detect_condidate(self, acc):
        if np.linalg.norm(acc[1,:]) > max(np.linalg.norm(acc[0,:]),np.linalg.norm(acc[2,:])) and \
            np.linalg.norm(acc[1,:]) > self.miu_alpha + self.sigma_alpha / self.alpha:
            return 1
        elif np.linalg.norm(acc[1,:]) < min(np.linalg.norm(acc[0,:]),np.linalg.norm(acc[2,:])) and \
            np.linalg.norm(acc[1,:]) < self.miu_alpha - self.sigma_alpha / self.alpha:
            return -1
        else:
            return 0

    def update_peak(self,acc):




if __name__ == '__main__':
    file_name = '/home/steve/Data/IPIN2017Data/Track3/01-Training/CAR/logfile_CAR_R03-2017_S4.txt'

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
    step_detector = StepDetector()

    plt.figure()
    for i in range(1, 4):
        plt.plot(acc[:,0],acc[:,i])
    plt.plot(acc[:,0], np.linalg.norm(acc[:,1:],axis=1),'r-')

    pv_flag = np.zeros(acc.shape[0])
    for i in range(1,acc.shape[0]-1):
        pv_flag[i] = step_detector.detect_condidate(acc[i-1:i+2,1:])
    plt.plot(acc[:,0],pv_flag,'r*')

    plt.grid()



    plt.show()
