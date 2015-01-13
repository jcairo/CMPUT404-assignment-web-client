#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

# this is more the response obj
class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host, port))
        return None

    # get response code
    def get_code(self, data):
        return None

    # get response headers
    def get_headers(self, data):
        return None
    
    # get response body
    def get_body(self, data):
        return None

    def build_request(self, url, method="GET", args=None):
        if method != 'GET' or method != 'POST':
            # raise error
            pass

        url_components = urlparse.urlparse(url) 
        path = url_components.path
        if method == 'GET' and args is not None:
            path += '?' + urllib.urlencode(args)
        domain = url_components.netloc
        headers = method + ' ' + path + '?' + ' ' + 'HTTP/1.1\r\n'    
        headers += 'Host: ' + domain + '\r\n'
        headers += 'Connection: ' + 'close\r\n'
        if method == "GET":
            request = headers
        elif method == "POST" and args is not None:
            headers += 'Content-Type: ' + 'x-www-form-urlencoded\r\n'
            body = urllib.urlencode(args)
            headers += 'Content-Length: ' + str(len(byte(body)))
            headers += '\r\n'
            request = headers + body
        return request
    
    def parse_host_and_port(self, url):
        url_components = urlparse.urlparse(url)
        try:
            host, port = url_components.netloc.split(':')
        except ValueError as e:
            host = url_components.netloc
            port = 80
        return host, port

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            print (str(buffer))
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        host, port = self.parse_host_and_port(url)
        request = self.build_request(url, "GET", args)
        self.connect(host, port)
        self.connection.sendall(request)
        raw_response = self.recvall(self.connection)
        self.connection.close()
        code = self.get_code(raw_response)
        body = self.get_body(raw_response)
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        host, port = self.parse_host_and_port(url)
        request = self.build_request(url, "POST", args)
        self.connect(host, port)
        self.connection.send(request)
        raw_response = self.recvall(self.connection)
        self.connection.close()
        code = self.get_code(raw_response)
        body = self.get_body(raw_response)
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
