# -*- coding:utf-8 -*-
import os
import re
from subprocess import PIPE,Popen

def shell(command,out=True,err=True):#封装,具有阻塞性
    '''
       这里command可以为arp -a等带参数的命令,但是如果Popen()不加shell=True
       就不能使用带参数的命令否则会引发OSError，但是好像可以通过给command传递一个列表
       来实现带参数的命令:['arp','-a']
    '''
    proc=Popen(command,shell=True,stdout=PIPE,stderr=PIPE,stdin=PIPE)#开启子进程
    #可以使用proc.terminate()结束子进程
    result=''
    if out:
        result+=proc.stdout.read()
    if err:
        result+=proc.stderr.read()
    return  result

def get_internet_ip_prefix():
    '''返回无线网卡IP前二位字符串,或者逻辑值False'''
    ipprefix = None
    DN = open(os.devnull, 'w')  
    proc = Popen(['/sbin/ip', 'route'], stdout=PIPE, stderr=DN)
    def_route = proc.communicate()[0].split('\n')#[0].split()
    for line in def_route:
        if 'wlan' in line and 'default via' in line:
            line = line.split()
            inet_iface = line[4]
            ipprefix = line[2][:2] # Just checking if it's 192, 172, or 10
            return ipprefix
    return False

def getip(interface='eth0'):#得到指定网卡的IP地址
    result=shell("ifconfig",err=False)
    m=re.search('inet (.*)  netmask',result[result.find(interface):])
    if m!=None:
        return m.group(1)
    else:
        return ''




if __name__=='__main__':
    print shell('arp -a')
