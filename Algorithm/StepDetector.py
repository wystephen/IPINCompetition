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

import array


class StepDetector:
    def __init__(self):
        self.counter = 0
        self.condidate_list = list()
        self.condidate_value = list()

        self.miu_alpha = 10.0
        self.sigma_alpha = 1.0
        self.alpha = 11.0

        self.alpha_p = 10.0
        self.alpha_v = 10.0

        self.last_index = 0
        self.last_type = 0
        self.last_time_p = -1.0
        self.last_time_v = -1.0

        self.Thp = 0.5
        self.Thv = 0.5

        self.p_interval_list = list()
        self.v_interval_list = list()

        self.acc_buffer = array.array('d')

    def detect_condidate(self, acc):
        if np.linalg.norm(acc[1, :]) > max(np.linalg.norm(acc[0, :]), np.linalg.norm(acc[2, :])) and \
                np.linalg.norm(acc[1, :]) > self.miu_alpha + self.sigma_alpha / self.alpha:
            return 1
        elif np.linalg.norm(acc[1, :]) < min(np.linalg.norm(acc[0, :]), np.linalg.norm(acc[2, :])) and \
                np.linalg.norm(acc[1, :]) < self.miu_alpha - self.sigma_alpha / self.alpha:
            return -1
        else:
            return 0

    def update_peak(self, acc, data_time):
        self.alpha_p = np.linalg.norm(acc[1, :])
        if len(self.p_interval_list) < 3:
            self.Thp = data_time - self.last_time_p - 0.1
        else:
            self.p_interval_list.append(data_time - self.last_time_p)
            self.Thp = data_time - self.last_time_p - np.std(np.asarray(self.p_interval_list))
            if len(self.p_interval_list) > 5:
                self.p_interval_list.pop(0)

        self.last_time_p = data_time

    def update_valley(self, acc, data_time):
        self.alpha_v = np.linalg.norm(acc[1, :])
        if len(self.v_interval_list) < 3:
            self.Thv = data_time - self.last_time_v - 0.1
        else:
            self.v_interval_list.append(data_time - self.last_time_v)
            self.Thv = data_time - self.last_time_v - np.std(np.asarray(self.v_interval_list))
            if len(self.v_interval_list) > 5:
                self.v_interval_list.pop(0)

        self.last_time_v = data_time

    def step_detection(self, acc, data_index, data_time):
        tmp_flag = self.detect_condidate(acc)
        step_flag = False

        if tmp_flag is 1:  # peak
            if self.last_index is 0:  # initial first step
                self.last_type = tmp_flag  # set to peak
                self.update_peak(acc, data_time)

            elif self.last_type is -1 and data_time - self.last_time_p > self.Thp:
                self.last_type = tmp_flag
                self.update_peak(acc, data_time)
                self.miu_alpha = 0.5 * (self.alpha_v + self.alpha_p)

            elif self.last_type is 1 and data_time - self.last_time_p < self.Thp \
                    and np.linalg.norm(acc[1, :]) > self.alpha_p:
                self.update_peak(acc, data_time)

        elif tmp_flag is -1:
            if self.last_type is 1 and data_time - self.last_time_v > self.Thv:
                self.last_type = -1
                self.update_valley(acc, data_time)
                self.counter += 1
                step_flag = True
                self.miu_alpha = 0.5 * (self.alpha_p + self.alpha_v)
            elif self.last_type is -1 and data_time - self.last_time_v < self.Thv \
                    and np.linalg.norm(acc[1, :]) < self.alpha_v:
                self.update_valley(acc, data_time)

        if step_flag:
            if self.counter > 1:
                all_acc = np.frombuffer(self.acc_buffer, dtype=np.float).reshape([-1, 3])

                self.sigma_alpha = np.std(np.linalg.norm(all_acc, axis=1))
                self.acc_buffer = array.array('d')

        else:
            self.acc_buffer.append(acc[1, 0])
            self.acc_buffer.append(acc[1, 1])
            self.acc_buffer.append(acc[1, 2])

        return step_flag


def test_simple_data():
    data = np.loadtxt('/home/steve/Data/pdr_imu.txt', delimiter=',')
    step_detector = StepDetector()

    acc = np.zeros([data.shape[0], 4])
    acc[:, 0] = data[:, 0]
    acc[:, 1:] = data[:, 2:5]

    t_alpha = 0.4
    for i in range(1, acc.shape[0]):
        acc[i, 1:] = t_alpha * acc[i, 1:] + (1.0 - t_alpha) * acc[i - 1, 1:]

    plt.figure()
    for i in range(1, 4):
        plt.plot(acc[:, 0], acc[:, i])

    step_flag = np.zeros(acc.shape[0])
    for i in range(1, acc.shape[0] - 1):
        if step_detector.step_detection(acc[i - 1:i + 2, 1:], i, acc[i, 0]):
            step_flag[i] = 10.0
    plt.plot(acc[:, 0], step_flag, '-+r')
    plt.grid()
    plt.show()


def test_ipin_data():
    file_name = '/home/steve/Data/IPIN2017Data/Track3/01-Training/CAR/logfile_CAR_R02-2017_S4.txt'

    ll = LogLoader(file_name)

    acc = np.zeros([ll.acce.shape[0], 4])
    acc[:, 0] = ll.acce[:, 0]
    acc[:, 1:] = ll.acce[:, 2:5]

    t_alpha = 0.2
    for i in range(1, acc.shape[0]):
        acc[i, 1:] = t_alpha * acc[i, 1:] + (1.0 - t_alpha) * acc[i - 1, 1:]

    # show time interval
    plt.figure()
    plt.plot(acc[1:, 0] - acc[:-1, 0])
    time_interval_array = acc[1:, 0] - acc[:-1, 0]

    # print(np.mean(time_interval_array),
    #       np.std(time_interval_array))

    #
    step_detector = StepDetector()

    plt.figure()
    for i in range(1, 4):
        plt.plot(acc[:, 0], acc[:, i])
    plt.plot(acc[:, 0], np.linalg.norm(acc[:, 1:], axis=1), 'r-')

    pv_flag = np.zeros(acc.shape[0])
    step_flag = np.zeros(acc.shape[0])
    for i in range(1, acc.shape[0] - 1):
        pv_flag[i] = step_detector.detect_condidate(acc[i - 1:i + 2, 1:])
        if step_detector.step_detection(acc[i - 1:i + 2, 1:], i, acc[i, 0]):
            step_flag[i] = 10.0
    plt.plot(acc[:, 0], pv_flag, 'r*')
    plt.plot(acc[:, 0], step_flag, 'y-+')

    plt.grid()

    plt.show()


if __name__ == '__main__':
    test_simple_data()
