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
                tss = []
                lengths = []
                for l in f.readlines()[:-1]:
                    ts, dst, src, length, snd_nxt, snd_una, snd_cwnd, ssthresh, snd_wnd, srtt, rcv_wnd = l.split(
                    )
                    # Measure only send flow.
                    if dst[:-5] == '10.0.0.2':
                        tss.append(float(ts))
                        lengths.append(float(length)/128.0)
                total_length = np.sum(lengths)/tss[-1]
                normalized_rate = total_length/1.5/1024.0
                bursts[burst].append((period, normalized_rate))
        for burst in bursts:
            if(burst==0.1):
                plt.plot(
                    *zip(*sorted(bursts[burst])), label='UDP attack burst time =  {}ms'.format(burst))
                plt.title('Five Aggregated TCP Connections Throughput')

            if(burst==0.15):
                plt.plot(
                    *zip(*sorted(bursts[burst])), label='UDP attack burst time=  {}ms'.format(burst))
                plt.title('Single TCP Connection Throughput')

        plt.xlim(0,5)
        plt.xlabel('Periods (s)')
        plt.ylabel('Normalized Throughput')
        plt.legend(loc='best')
        plt.savefig('{}_cwnd.png'.format(dir_name), bbox_inches='tight')
        plt.clf()


if __name__ == '__main__':
    main()
