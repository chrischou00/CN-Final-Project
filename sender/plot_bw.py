#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import math
import sys
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    dir_names = [
        f for f in os.listdir('.')
        if f.startswith('results-') and os.path.isdir(f)
    ]
    plt.figure(figsize=(20, 10))
    for dir_name in dir_names:
        print("ploting on file: ")
        print(dir_name+'\n')
        files = [i for i in os.listdir(dir_name) if i.startswith('cwnd-')]
        bursts = {}
        for fname in files:
            full_path = os.path.join(dir_name, fname)
            period, burst = tuple(map(float, fname[5:-4].split('-')))
            bursts.setdefault(burst, [])
            with open(full_path) as f:
                lines = f.readlines()
                bwidth=0
                count=0
                if(burst==0.1):
                    for l in lines:
                        if(l!=[] and l[:5]=='[SUM]' and l[-9:-1]=='receiver'):
                            id, interval, iunit, transfer, tunit, bandwidth, bunit, host = l.split()
                            if(bunit=='Mbits/sec'):
                                bwidth += float(bandwidth)*1000.0
                            elif(bunit=='bits/sec'):
                                bwidth += float(bandwidth)/1000.0
                            else:
                                bwidth += float(bandwidth)
                            count+=1
                if(burst==0.15):
                    for l in lines:
                        if(l!=[] and l[-9:-1]=="receiver"):
                            id1, id2, interval, iunit, transfer, tunit, bandwidth, bunit, host= l.split()
                            if(bunit=='Mbits/sec'):
                                bwidth += float(bandwidth)*1000.0
                            elif(bunit=='bits/sec'):
                                bwidth += float(bandwidth)/1000.0
                            else:
                                bwidth += float(bandwidth)
                            count+=1
                if(count==0):
                    count=1
                    bwidth=0
                normalized_rate = bwidth/count/1500.0
                bursts[burst].append((period, normalized_rate))
        for burst in bursts:
            if(burst==0.1):
                plt.plot(
                    *zip(*sorted(bursts[burst])), label='UDP attack burst time =  {}ms'.format(burst))
                plt.title('Five Aggregated TCP Connections Throughput', fontsize=24)

            if(burst==0.15):
                plt.plot(
                    *zip(*sorted(bursts[burst])), label='UDP attack burst time =  {}ms'.format(burst))
                plt.title('Single TCP Connection Throughput', fontsize=24)

        plt.xlim(0,5)
        plt.xlabel('Periods (s)',fontsize=20)
        plt.ylabel('Normalized Throughput',fontsize=20)
        plt.legend(loc=4, fontsize=18)
        plt.savefig('{}_cwnd.png'.format(dir_name), bbox_inches='tight')
        plt.clf()


if __name__ == '__main__':
    main()
