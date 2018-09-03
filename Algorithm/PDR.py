# -*- coding:utf-8 -*-
# carete by steve at  2018 / 09 / 02　上午11:35
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
import scipy as sp

from AuxiliaryTool.LogLoader import LogLoader
from Algorithm.StepDetector import StepDetector
from Algorithm.StepLengthEstimator import StepLengthEstimatorV


def test_simple_data():
    data = np.loadtxt('/home/steve/Data/pdr_imu.txt', delimiter=',')
    step_detector = StepDetector(5.0, 2.0)
    step_estimator = StepLengthEstimatorV()

    acc = np.zeros([data.shape[0], 4])
    acc[:, 0] = data[:, 0]
    acc[:, 1:] = data[:, 2:5]
    gyr = np.zeros([data.shape[0], 4])
    mag = np.zeros([data.shape[0], 4])

    gyr[:, 0] = data[:, 0]
    gyr[:, 1:] = data[:, 5:8]

    mag[:, 0] = data[:, 0]
    mag[:, 1:] = data[:, 8:11]

    t_alpha = 0.2
    for i in range(1, acc.shape[0]):
        acc[i, 1:] = t_alpha * acc[i, 1:] + (1.0 - t_alpha) * acc[i - 1, 1:]

    plt.figure()
    # for i in range(1, 4):
    #     plt.plot(acc[:, 0], acc[:, i])
    plt.plot(acc[:, 0], np.linalg.norm(acc[:, 1:], axis=1))

    step_flag = np.zeros(acc.shape[0])

    import array

    pos_array = array.array('d')
    last_pos_x = 0.0
    last_pos_y = 0.0



    import math
    for i in range(1, acc.shape[0] - 1):
        if step_detector.step_detection(acc[i - 1:i + 2, 1:], i, acc[i, 0]):
            step_flag[i] = step_estimator.step_length_estimate(step_detector.miu_alpha * 2.0) + 10.0
            step_length = step_estimator.step_length_estimate(step_detector.miu_alpha * 2.0)
            # if i < 10:
            if np.linalg.norm(mag[i,1:3]) < 0.1:
                mag[i,1:] = mag[i-1,1:]
            else:
                alpha = 0.2
                mag[i,1:] = alpha * mag[i,1:] + (1.0 - alpha) * mag[i,1:]
            simple_ori = math.atan2(mag[i,2],mag[i,1])
            # else:
            #     simple_ori = math.atan2(np.mean(mag[i-10:i+1,2]),np.mean(mag[i-10:i+1,1]))

            last_pos_x  += step_length * math.cos(simple_ori)
            last_pos_y += step_length * math.sin(simple_ori)
            pos_array.append(last_pos_x)
            pos_array.append(last_pos_y)


    plt.plot(acc[:, 0], step_flag, '-+r')

    plt.grid()

    plt.figure()
    plt.title('trace')
    pos = np.frombuffer(pos_array,dtype=np.float).reshape([-1,2])
    plt.plot(pos[:,0],pos[:,1],'--+')
    plt.grid()

    plt.figure()
    plt.subplot(211)
    plt.title('gyr')
    for i in range(1,4):
        plt.plot(gyr[:,0],gyr[:,i])
    plt.subplot(212)
    plt.title('mag')
    for i in range(1,4):
        plt.plot(mag[:,0],mag[:,i],'+',label=str(i))
    plt.legend()



    plt.show()


if __name__ == '__main__':
    test_simple_data()
