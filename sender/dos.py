#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import time
import subprocess
import signal
from paramiko import client
import sys
import numpy as np

class ssh:
    client = None
 
    def __init__(self, address, username, password):
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=True)
 
    def sendCommand(self, command):
        if(self.client):
            stdin, stdout, stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata
 
                    print(str(alldata, "utf8"))
        else:
            print("Connection not opened.")

def run_flow(ntcp, connection, cwnd_file=None):
    print('Starting receiver on server.')
    server_cmd = "./run_receiver.sh &"
    connection.sendCommand(server_cmd)
    print(server_cmd)
    # Wait for receiver to start listening.
    time.sleep(1.0)
    print('Starting sender on sender.')
    start = time.time()
    sender_cmd = './run_sender.sh -t server'
    if cwnd_file is not None:
        sender_cmd += ' -p {}'.format(cwnd_file)+' -n {}'.format(ntcp)
    print('TCP flow started on sender and server.')
    os.system(sender_cmd)
    return time.time() - start


def start_attack(period, burst, connection):
    attacker_cmd = 'python run_attacker.py --destination server'
    attacker_cmd += ' --period {}'.format(period)+' --burst {}'.format(burst)+' &'
    connection.sendCommand(attacker_cmd)
    print('UDP attack started from attacker to server.')
    print(attacker_cmd)
    return True

def stop_attack(connection):
    print('stop attacker')
    cmd = "./cleanup.sh"
    connection.sendCommand(cmd)

def stop_server(connection):
    print('stop server')
    cmd = "./cleanup.sh"
    connection.sendCommand(cmd)


def main():
    parser = argparse.ArgumentParser(description="TCP DoS simulator.")
    parser.add_argument(
        '--burst',
        '-b',
        help="Burst duration in seconds of each DoS attack.",
        type=float,
        default=0.15)
    parser.add_argument(
        '--suffix',
        '-s',
        help="Suffix for output directory",
        type=str,
        default='default')
    parser.add_argument(
        '--period',
        '-p',
        help="Seconds between low-rate DoS attacks, e.g. 0.5",
        type=float,
        default=0.5)
    parser.add_argument(
        '--nc',
        '-n',
        help="Number of TCP connections, e.g. 1",
        type=int,
        default=1)
    parser.add_argument(
        '--rto', '-r', help="rto_min value, in ms", type=int, default=1000)
    args = parser.parse_args()

    # Initialize kernel parameters.
    subprocess.check_call('sysctl -q -w net.ipv4.tcp_sack=0', shell=True)
    subprocess.check_call('sysctl -q -w net.ipv4.tcp_dsack=0', shell=True)
    subprocess.check_call('sysctl -q -w net.ipv4.tcp_fack=0', shell=True)
    subprocess.check_call('ethtool -K eth1 tso off gso off gro off', shell=True)
    server_connection = ssh("server","yz3647"," ")
    attacker_connection = ssh("attacker","yz3647"," ")

    stop_attack(connection=attacker_connection)
    stop_server(connection=server_connection)

    output_dir = 'results-{}'.format(args.suffix)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    time_file = os.path.join(output_dir, 't-{}-{}.txt'.format(
        args.period, args.burst))
    cwnd_file = os.path.join(output_dir, 'cwnd-{}-{}.txt'.format(
        args.period, args.burst))
    print("NUmber of TCP connection(s) = {}\n".format(args.nc))
    attack = start_attack(period=args.period, burst=args.burst, connection=attacker_connection)
    t = run_flow(args.nc, connection=server_connection,cwnd_file=cwnd_file)
    print('Sending completed in %.4f seconds.' % t)
    with open(time_file, 'w') as f:
        f.write(str(t) + '\n')

    stop_attack(connection=attacker_connection)
    stop_server(connection=server_connection)


if __name__ == '__main__':
    main()
