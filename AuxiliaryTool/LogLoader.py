# -*- coding:utf-8 -*-
# carete by steve at  2018 / 09 / 01　下午4:52
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


import numpy as np

import  array


class LogLoader:
    def __init__(self, file_name):
        file = open(file_name)

        file_lines = file.readlines()

        posi_array = array.array('d')


        for line in file_lines:
            if line[0] is '%':
                continue
            if 'POSI' in line:
                print(line)
                unit = line.split(';')
                print(unit[1:])
                for i in range(1,len(unit)):

                    posi_array.append(float(unit[i]))


        self.posi = np.frombuffer(posi_array,dtype=np.float).reshape([-1,6])

    def set_ref_frame(self,long):


if __name__ == '__main__':
    file_name = '/home/steve/Data/IPIN2017Data/Track3/01-Training/CAR/logfile_CAR_R01-2017_A5.txt'

    ll = LogLoader(file_name)


    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(ll.posi[:,2],ll.posi[:,3],'--*')
    plt.grid()
    plt.show()

