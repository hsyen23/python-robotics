# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 17:56:52 2022

@author: Yen
"""

import socket
from util_threads import *
from util_nodes import *

server_side_socket = socket.socket()
host = '127.0.0.1'
port = 1000
thread_count = 0
client_num = 20

try:
    server_side_socket.bind((host,port))
except socket.error as err:
    print(str(err))

print('Socket is listening...')
server_side_socket.listen(client_num)

topics = {}

serverThread = ServerThread(server_side_socket, topics)
serverThread.start()

def printAllTopics():
    print("Topic List:")
    print("----------------------")
    for (key, value) in topics.items():
        print(key)
    print("----------------------")

def close():
    print("command to close server")
    serverCloser = ServerCloser()
    topics = {}
    