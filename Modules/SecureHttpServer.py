# -*- coding:utf-8 -*-
import SocketServer
import SimpleHTTPServer
import BaseHTTPServer
import ssl
import socket
from color import *

PEM='Modules/cert/server.pem' #PEM指定服务端认证的文件
#只适合从当前目录调用的路径!!

class SecureHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    Request handler for the HTTPS server. It responds to
    everything with a 301 redirection to the HTTP server.
    """
    def do_QUIT(self):
        """
        Sends a 200 OK response, and sets server.stop to True
        """
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def do_GET(self):
        self.send_response(301)
        self.send_header('Location', 'http://'+IP+':' + str(PORT))
        self.end_headers()

    def log_message(self, format, *args):
        return

class SecureHTTPServer(BaseHTTPServer.HTTPServer):
    """
    Simple HTTP server that extends the SimpleHTTPServer standard
    module to support the SSL protocol.

    Only the server is authenticated while the client remains
    unauthenticated (i.e. the server will not request a client
    certificate).

    It also reacts to self.stop flag.
    """
    def __init__(self, server_address, HandlerClass):
        SocketServer.BaseServer.__init__(self, server_address, HandlerClass)
        fpem = PEM
        self.socket = ssl.SSLSocket(
            socket.socket(self.address_family, self.socket_type),
            keyfile=fpem,
            certfile=fpem
        )

        self.server_bind()
        self.server_activate()

    def serve_forever(self,SSL_PORT):
        """
        Handles one request at a time until stopped.
        """
        print '[' + T + '*' + W + '] Starting HTTPS server at port ' + str(SSL_PORT)
        self.stop = False
        while not self.stop:
            self.handle_request()

def Start(SSL_IP="",SSL_PORT=443,IP='192.168.81.183',PORT=8080):
    '''
       ##这个脚本的作用是将上面监听到https GET请求全部以301跳转方式跳转到下面的监听IP和端口
       #访问这个443端口,浏览器会提示不安全
       
       SSL_IP指定 HTTPS绑定的网卡接口IP,""表示所有接口
       SSL_PORT HTTPS绑定的端口
       IP 不支持"",注意如果使用127.0.0.1那么从其他主机访问会被被跳转到访问主机的127.0.0.1
          指定跳转的HTTP服务器IP
       PORT 上述IP服务器使用的端口
       
    '''
    Handler = SecureHTTPRequestHandler
    httpd=SecureHTTPServer((SSL_IP, SSL_PORT), Handler)
    httpd.serve_forever(SSL_PORT)
    #-已取消--返回一个对象,使用该对象的方法.serve_forever()启用服务

if __name__=='__main__':
    PEM='cert/server.pem'
    Start()
    
    

























































