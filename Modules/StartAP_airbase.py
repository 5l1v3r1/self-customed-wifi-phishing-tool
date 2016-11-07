# -*- coding:utf-8 -*-
from common import shell
from color import *
import os
from subprocess import PIPE,Popen

class StartAP(object):
    '''
       描述开启能够正常上网的AP热点
    '''
    def check(self):
        if not os.path.isfile('/etc/dhcp/dhcpd.conf'):
           install = raw_input('['+T+'*'+W+'] isc-dhcp-server not found in /etc/dhcp/dhcpd.conf, install now? [y/n] ')
           if install == 'y':
               os.system('apt-get install isc-dhcp-server')##需要填写
               #如果失败,修复更新源，重新安装
           else:
               sys.exit('['+R+'-'+W+'] isc-dhcp-server not found in /etc/dhcp/dhcpd.conf')

    def __init__(self,a_iface='eth0',ap_iface='wlan0',wifiname='FreeWifi',channel=6):
        '''
           a_iface 一个可以正常上网的网卡接口,推荐eth0
           ap_iface 产生AP热点的网卡
           wifiname AP热点名称
           channel AP所在的频道
        '''
        self.a_iface=a_iface
        self.ap_iface=ap_iface
        self.wifiname=wifiname
        self.channel=channel
        self.airbase_proc=''


    def __ProduceAP(self):
        shell('airmon-ng check kill')#这一步可能会杀掉用于正常上网的无线网卡接口
        shell('airmon-ng start '+self.ap_iface,err=False)
        airbase_c="airbase-ng -e "+"'"+self.wifiname+"'"+" -c "+str(self.channel)+" "+self.ap_iface+"mon"
        self.airbase_proc=Popen(airbase_c,shell=True,stdout=PIPE,stderr=PIPE)#不会输出到当前终端里
        print '['+B+'+'+W+']'+'airbase is running and you are able to find AP('+self.wifiname+')'
        
    def __ReadyWorkAfterProduceAP(self):
        print '[+]Waiting for completing configuration'
        shell('ifconfig at0 192.168.2.254 netmask 255.255.255.0')
        shell('ifconfig at0 up')
        shell('routers add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.2.254')
        shell('echo 1 > /proc/net/ipv4/ip_forward')
        shell('iptables -t nat -A POSTROUTING -o '+self.a_iface+' -j MASQUERADE')
        
    def __dhcp_conf(self):
        f=open('/etc/dhcp/dhcpd.conf','w')
        f.write('authoritative;'+'\n')#拒绝不正确的IP地址的要求
        f.write('default-lease-time 700;'+'\n')#默认租约
        f.write('max-lease-time 8000;'+'\n')#最大默认租约
        f.write('option routers 192.168.2.254;'+'\n')#默认路由
        f.write('option domain-name "'+self.wifiname+'";'+'\n')#给予一个域名
        f.write('subnet 192.168.2.0 netmask 255.255.255.0{'+'\n')
        f.write(' range 192.168.2.101 192.168.2.200;'+'\n')
        f.write('}'+'\n')

    def __StartDhcpServer(self):
        result=shell('sudo /etc/init.d/isc-dhcp-server start')
        if result.find('Starting isc-dhcp-server (via systemctl)')!=-1:
            print '[+]DHCP server(isc-dhcp-server) start successfully!'
            print '[+]Now you can use AP('+self.wifiname+') normally:-)'
        else:
            print '[-]DHCP server(isc-dhcp-server) failed to start!'
            print 'Error:\n'+R+result+W+'\n'
            
    def __exit(self):
        try:
            while 1:
                if raw_input("Press x|X for ending airbase-ng:").lower()=='x':
                    self.airbase_proc.terminate()
                    break
        except KeyboardInterrupt:
            pass

    def __heal(self):
        pass

    def run(self):
        self.check()
        print "["+O+"+"+W+"]Starting fishing AP"
        self.__ProduceAP()
        self.__ReadyWorkAfterProduceAP()
        self.__dhcp_conf()
        self.__StartDhcpServer()
        self.__exit()
        self.__heal()

if __name__=='__main__':
    ap=StartAP()
    ap.run()
















        
        
        
        
        
    
        


















        
        
        
        
        
