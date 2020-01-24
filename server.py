#  coding: utf-8
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def send_404(self,path):
        status = b"HTTP/1.1 404 Not Found\r\n"
        content = "<!DOCTYPE html>\n<html>\n<title>404 Error</title>\n<body>The link is borken or the page is removed.\n</body>\n</html>\n"
        content_len = ("Content-Length: {}\r\n".format(str(len(content)))).encode()
        content_type = b"Content-Type: text/html; charset=UTF-8\r\n"
        body = content.encode()
        self.request.send(status + content_len+content_type + b'\r\n' + body)

    def send_405(self,split_data):
        status =b"HTTP/1.1 405 Method Not Allowed\r\n"
        content= "<!DOCTYPE html>\n<html>\n<body> The requested resource does not support http method '" + split_data + "'</body>\n</html>\n"
        content_len = ("Content-Length: {}\r\n".format(str(len(content)))).encode()
        content_type =b"Content-Type: application/json; charset=utf-8\r\n"
        body = content.encode()
        self.request.send(status + content_len + content_type + b'\r\n'+ body)

    def handle_file(self, path):
        try:
          status = b"HTTP/1.1 200 OK\r\n"
          if path[-4:] == ".css":
            content = open( "./www"+ path,'r').read()
            content_type = b"Content-Type: text/css; charset=UTF-8\r\n"
            content_len = ("Content-Length: {}\r\n".format(str(len(content)))).encode()
            body = content.encode()
            self.request.send(status + content_len + content_type + b'\r\n' + body)
          elif path[-5:] == ".html":
            content = open( "./www"+ path,'r').read()
            content_type = b"Content-Type: text/html; charset=UTF-8\r\n"
            content_len = ("Content-Length: {}\r\n".format(str(len(content)))).encode()
            body = content.encode()
            self.request.send(status + content_len + content_type + b'\r\n'+ body)

        except:
          self.send_404(path)

    def handle_deep_end(self,path):
        try:
          content = open( "./www"+path+'/index.html','r').read()
          status = b"HTTP/1.1 301 Moved Permanently\r\n"
          loc = "Location: http://127.0.0.1:8080"+ path+"/\r\n"
          location = loc.encode()

          body = content.encode()
          self.request.send(status + location + b'\r\n')

        except:
          self.send_404(path)

    def handle_path(self,path):
        try:
          # deal with ""
          content = open( "./www"+path+'index.html','r').read()
          status = b"HTTP/1.1 200 OK\r\n"
          content_len = ("Content-Length: {}\r\n".format(str(len(content)))).encode()
          content_type = b"Content-Type: text/html; charset=UTF-8\r\n"
          body = content.encode()
          self.request.send(status + content_len+ content_type + b'\r\n'+ body)

        except:
          self.handle_deep_end(path)

    def handle(self):

        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))
        if self.data:
            split_data = self.data.decode().split()
            #print(split_data)

            if split_data[0] == "GET":
                if split_data[1][-4:] == '.css' or split_data[1][-5:] == '.html':
                    self.handle_file(split_data[1])
                else:
                    self.handle_path(split_data[1])
            else:
                self.send_405(split_data[0])


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
