#!/usr/bin/env python3

# scanlan.py
# 20210123

# see about using the following to get the ip address
# /sbin/ifconfig | grep broadcast | awk '{print $2}'
# ip addr | grep brd | grep inet | awk '{print $2}'

import os
import socket

def main():
    print()
    print(f'Network Devices: {get_my_net_ip()}')
    print()
    write_temp_file()
    process_temp_file()

def get_my_net_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    cmd = 'ip addr > ipaddr.txt'
    os.system(cmd)
    f = open('ipaddr.txt')
    lines = f.readlines()
    f.close()
    for line in lines:
        if IPAddr in line:
            net = line.split()[1]
            ipparts = net.split('.')
            netip = ipparts[0] + '.' + ipparts[1] + '.' + ipparts[2] + '.'
            netip += '0' + ipparts[3][ipparts[3].find('/'):]  
    os.remove('ipaddr.txt')
    return netip 

def write_temp_file():
    net = get_my_net_ip()
    cmd = f'sudo nmap -sn {net} >> temp.txt'
    os.system(cmd)

def process_temp_file():
    hostname = ''
    macaddress = ''
    devicelist = []
    device = []
    ifile = open('temp.txt', 'r')
    for line in ifile:
        if line.startswith('Nmap'):
            host = line.replace('Nmap scan report for ', '').rstrip('\n').split()
            if len(host) < 2:
                host_name = ''
                host_ip = host[0].strip('()')
            else:
                host_name = host[0]
                host_ip = host[1].strip('()')
            device.append(host_name)
            device.append(host_ip)
        if line.startswith('MAC'):
            macaddress = line.replace('MAC Address: ', '').rstrip('\n')
            device.append(macaddress)
        if len(macaddress) > 0:
            print_device(device)
            device = []
            host = ''
            macaddress = ''
    ifile.close()
    os.remove('temp.txt')

def print_device(devicelist):
    print(f'{devicelist[0]:24} {devicelist[1]:16} {devicelist[2]}')

if __name__ == '__main__':
    main()
