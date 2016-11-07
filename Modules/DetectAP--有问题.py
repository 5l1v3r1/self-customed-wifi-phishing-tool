# -*- coding: utf-8 -*-
import time
from scapy.all import *
from threading import Thread, Lock
from color import *

#运行错误说开启的线程的channel_hop不知道hop_daemon_running,Popen等

class DetectAP(object):
    count =0 # APs的key值
    APs = {} # 用于记录发现的AP
    hop_daemon_running = True #这值无需用户设置,用于判断是否停止修改网卡监听频道
    lock=Lock() #threading里面导入的lock
    
    DN = open(os.devnull, 'w') #握草,一个作者的风格,Popen需要
    
    def __init__(self,mon_iface):
        '''
          mon_iface 是已经开启监听的网卡接口,字符串
        '''
        self.mon_iface = mon_iface
        pass
    
    def channel_hop(self,mon_iface):
        ##每过一秒变换监听网卡的监听频道(1~11)
        chan = 0
        err = None
        while hop_daemon_running:  ##程序开头对此变量初始化赋值为True
            try:
                err = None
                if chan > 11:
                    chan = 0
                chan = chan+1
                channel = str(chan)
                iw = Popen(['iw', 'dev', mon_iface, 'set', 'channel', channel], stdout=DN, stderr=PIPE)
                for line in iw.communicate()[1].split('\n'):
                    if len(line) > 2: # iw dev shouldnt display output unless there's an error
                        with lock:
                            err = '['+R+'-'+W+'] Channel hopping failed: '+R+line+W+'\n    \
Try disconnecting the monitor mode\'s parent interface (e.g. wlan0)\n    \
from the network if you have not already\n'
                            break
                time.sleep(1)
            except KeyboardInterrupt:
                sys.exit()
                
    def sniffing(self,interface, cb):
        '''This exists for if/when I get deauth working
        so that it's easy to call sniff() in a thread'''
        sniff(iface=interface, prn=cb, store=0)
        
    def targeting_cb(self,pkt):
        if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
            try:
                ap_channel = str(ord(pkt[Dot11Elt:3].info))
            except Exception:
                return
            essid = pkt[Dot11Elt].info
            mac = pkt[Dot11].addr2
            if len(APs) > 0:
                for num in APs:
                    if essid in APs[num][1]:
                        return
            count += 1
            APs[count] = [ap_channel, essid, mac]
            target_APs()

    def copy_AP(self):  #想用户询问想选择的AP,并返回用户选择AP的channel 频道,esssid 名称,mac物理地址
        copy = None
        while not copy:
            try:
                copy = raw_input('\n['+G+'+'+W+'] Choose the ['+G+'num'+W+'] of the AP you wish to copy: ')
                copy = int(copy)
            except Exception:
                copy = None
                continue
        channel = APs[copy][0]
        essid = APs[copy][1]
        if str(essid) == "\x00":
            essid = ' '
        mac = APs[copy][2]
        return channel, essid, mac
    
    def Start(self):
        time.sleep(3)
        hop = Thread(target=self.channel_hop, args=(self.mon_iface,))
        hop.daemon = True
        hop.start()
        self.sniffing(self.mon_iface, self.targeting_cb)
        channel, essid, ap_mac = self.copy_AP()
        hop_daemon_running = False    #关闭channel_hop
        return channel, essid, ap_mac  #返回用户从发现的AP中选择的一个AP的频道,名称,mac地址


if __name__=='__main__':
    #这个脚本暂时没有让选择的接口处于监听模式的功能,使用前请使用下面的命令确保wlan0处于监听模式
    #ifconfig wlan0 down
    #iwconfig wlan0 mode monitor
    #ifconfig wlan0 up
    ChooseAP=DetectAP('wlan0')
    print ChooseAP.Start()













            
