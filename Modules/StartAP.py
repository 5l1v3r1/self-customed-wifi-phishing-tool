# -*- coding:utf-8 -*-
import os
import sys
import time 
from common import get_internet_ip_prefix
from subprocess import PIPE,Popen
from color import *

class StartAP(object):  #根据__init__传递的变量
    '''
    '''
    def check(self):#必须有self
        if not os.path.isfile('/usr/sbin/hostapd'):
            install = raw_input('['+T+'*'+W+'] isc-dhcp-server not found in /usr/sbin/hostapd, install now? [y/n] ')
            if install == 'y':
                os.system('apt-get -y install hostapd')
            else:
                sys.exit('['+R+'-'+W+'] hostapd not found in /usr/sbin/hostapd')
                
    def __init__(self,ap_iface,channel,essid):  
        '''
           ap_iface 一张无线网卡接口,字符串
           channel 频道,字符串
           essid  AP名称,字符串
        '''
        self.ap_iface=ap_iface
        self.channel=channel
        self.essid=essid

        self.ipprefix=get_internet_ip_prefix() #self.ipprefix可能是字符串也可能是False

    def dhcp_conf(self):
        config = ( # disables dnsmasq reading any other files like /etc/resolv.conf for nameservers
                  'no-resolv\n'
                  # Interface to bind to
                  'interface=%s\n'
                  # Specify starting_range,end_range,lease_time
                  'dhcp-range=%s\n'
                  'address=/#/10.0.0.1'
                )
        if self.ipprefix == '19' or self.ipprefix == '17' or not self.ipprefix:
            with open('/tmp/dhcpd.conf', 'w') as dhcpconf:
                # subnet, range, router, dns
                dhcpconf.write(config % (self.ap_iface, '10.0.0.2,10.0.0.100,12h'))
        elif self.ipprefix == '10':
            with open('/tmp/dhcpd.conf', 'w') as dhcpconf:
                dhcpconf.write(config % (self.ap_iface, '172.16.0.2,172.16.0.100,12h'))
        return '/tmp/dhcpd.conf'
    
    def dhcp(self,dhcp_conf_file):
        os.system('echo > /var/lib/misc/dnsmasq.leases')
        DN = open(os.devnull, 'w')
        dhcp = Popen(['dnsmasq', '-C', dhcp_conf_file], stdout=PIPE, stderr=DN)
        Popen(['ifconfig', self.ap_iface, 'mtu', '1400'], stdout=DN, stderr=DN)
        if self.ipprefix == '19' or self.ipprefix == '17' or not self.ipprefix:
            Popen(['ifconfig', self.ap_iface, 'up', '10.0.0.1', 'netmask', '255.255.255.0'], stdout=DN, stderr=DN)
            os.system('route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.1')
        else:
            Popen(['ifconfig', self.ap_iface, 'up', '172.16.0.1', 'netmask', '255.255.255.0'], stdout=DN, stderr=DN)
            os.system('route add -net 172.16.0.0 netmask 255.255.255.0 gw 172.16.0.1')

    def start_ap(self):
        print '['+T+'*'+W+'] Starting the fake access point...'
        config = ('interface=%s\n'
                  'driver=nl80211\n'
                  'ssid=%s\n'
                  'hw_mode=g\n'
                  'channel=%s\n'
                  'macaddr_acl=0\n'
                  'ignore_broadcast_ssid=0\n'
                )
        with open('/tmp/hostapd.conf', 'w') as dhcpconf:
            dhcpconf.write(config % (self.ap_iface, self.essid, self.channel))
        DN = open(os.devnull, 'w')
        Popen(['hostapd', '/tmp/hostapd.conf'], stdout=DN, stderr=DN)
        try:
            time.sleep(6) # Copied from Pwnstar which said it was necessary?
        except KeyboardInterrupt:
            print R+"I just sleep 6 seconds to wait for everything ready!"+W

    def run(self):
        self.check()
        self.dhcp(self.dhcp_conf())
        self.start_ap()
        
        

if __name__=='__main__':
    AP=StartAP('wlan0','1','FakeAP')
    AP.run()
    #测试结果:真的出现FakeAP,但是只运行这个脚本生成的AP无法连接
    











            
        
    
