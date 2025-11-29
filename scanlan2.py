#!/usr/bin/env python3

# scanlan.py
# 20210123

# see about using the following to get the ip address
# /sbin/ifconfig | grep broadcast | awk '{print $2}'
# ip addr | grep brd | grep inet | awk '{print $2}'

import os
import socket
import subprocess

def main():
    print(f'Network Devices: {get_my_net_ip()}')
    print()
    write_temp_file()
    process_temp_file()

def get_my_net_ip():
    cmd = 'ip addr | grep brd | grep inet | awk \'{print $2}\' > ipaddr.txt'
    os.system(cmd)
    with open('ipaddr.txt', 'r') as f:
        netip = f.read()
    os.remove('ipaddr.txt')
    return netip

def write_temp_file():
    print('write_temp_file()')
    net = get_my_net_ip()
    cmd = f'sudo nmap -sn {net} > temp.txt'
    os.system(cmd)

def process_temp_file():
    print('process_temp_file()')
    device = []
    host_ip = ''
    macaddress = ''
    name = ''
    ifile = open('temp.txt', 'r')
    for line in ifile:
        print('test', line)
        if line.startswith('Nmap'):
            host_ip = line.split()[-1]
        if line.startswith('MAC'):
            macaddress = line.split()[-2]
            name = line.split()[-1]
        if len(host_ip) > 0 and len(macaddress) > 0:
            device.append(host_ip)
            device.append(name)
            device.append(macaddress)
            print_device(device)
            device = []
            host_ip = ''
            macaddress = ''
            name = ''
    #os.remove('temp.txt')

def print_device(devicelist):
    print(f'{devicelist[0]:24} {devicelist[1]:16} {devicelist[2]}')

if __name__ == '__main__':
    main()
