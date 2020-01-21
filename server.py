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

    def send_405(self):
        self.request.send("HTTP/1.1 405 Method Not Allowed".encode())

    def handle_file(self, request):
        try:
          status = b"HTTP/1.1 200 OK\r\n"
          if request[-4:] == ".css":
            content = open( "./www"+ request,'r').read()
            content_type = b"Content-Type: text/css;\r\n\r\n"
            content_len = ("Content-Length: {}\r\n".format(str(len(content)))).encode()
            body = content.encode()
            self.request.send(status + content_len+content_type + body)
          elif request[-5:] == ".html":
            content = open( "./www"+ request,'r').read()
            content_type = b"Content-Type: text/html;\r\n\r\n"
            content_len = ("Content-Length: {}\r\n".format(str(len(content)))).encode()
            body = content.encode()
            self.request.send(status + content_len+content_type + body)

        except:
          self.request.send("HTTP/1.1 404 Not Found".encode())

    def handle_deep_end(self,path):
        try:
          content = open( "./www"+path+'/index.html','r').read()
          status = b"HTTP/1.1 301 Moved Permanently\r\n"
          loc = "Location: http://127.0.0.1:8080"+ path+"/"
          location = loc.encode()

          body = content.encode()
          self.request.send(status + location)

        except:
          self.request.send("HTTP/1.1 404 Not Found".encode())

        pass
    def handle_path(self,path):
        try:
          content = open( "./www"+path+'index.html','r').read()
          status = b"HTTP/1.1 200 OK\r\n"
          content_len = ("Content-Length: {}\r\n".format(str(len(content)))).encode()
          content_type = b"Content-Type: text/html;\r\n\r\n"
          body = content.encode()
          self.request.send(status + content_len + content_type + body)

        except:
          self.handle_deep_end(path)

    def handle(self):

        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))

        split_data = self.data.decode().split()
        #print(split_data)

        if split_data[0] == 'GET':
            if split_data[1][-4:] == '.css' or split_data[1][-5:] == '.html':
                self.handle_file(split_data[1])
            else:
                self.handle_path(split_data[1])
        else:
            self.send_405()


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
