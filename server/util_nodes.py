# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 03:12:35 2022

@author: Yen
"""

import socket
import json


def display_msg_from_server(server):
    msg = server.recv(1024)
    #print(msg.decode())

class Publisher:
    def __init__(self, topic):
        host = '127.0.0.1'
        port = 1000
        self.topic = topic
        self.client_side_socket = socket.socket()
        print('Waiting for connection')
        try:
            self.client_side_socket.connect((host, port))
            print('succeed!')
        except socket.error as e:
            print("There is an error occurred in Publisher Node")
            print(str(e))
        display_msg_from_server(self.client_side_socket)
        self.client_side_socket.send('publisher'.encode())
        display_msg_from_server(self.client_side_socket)
        self.client_side_socket.send(topic.encode())
        display_msg_from_server(self.client_side_socket)
    def send(self, data):
        json_data = json.dumps(data)
        self.client_side_socket.send(json_data.encode())
        display_msg_from_server(self.client_side_socket)
        
class Subscriber:
    def __init__(self, topic):
        host = '127.0.0.1'
        port = 1000
        self.topic = topic
        self.client_side_socket = socket.socket()
        print('Waiting for connection')
        try:
            self.client_side_socket.connect((host, port))
            print('succeed!')
        except socket.error as e:
            print(print("There is an error occurred in Subscriber Node"))
            print(str(e))
        display_msg_from_server(self.client_side_socket)
        self.client_side_socket.send('subscriber'.encode())
        display_msg_from_server(self.client_side_socket)
        self.client_side_socket.send(self.topic.encode())
        display_msg_from_server(self.client_side_socket)
    def get(self):
        self.client_side_socket.send('ready to get data. pls send'.encode())
        data = self.client_side_socket.recv(1024)
        data_json = data.decode()
        return_data = json.loads(data_json)
        return return_data
    
class ServerCloser:
    def __init__(self):
        host = '127.0.0.1'
        port = 1000
        self.client_side_socket = socket.socket()
        print('Waiting for connection to close server')
        try:
            self.client_side_socket.connect((host, port))
            print('succeed!')
        except socket.error as e:
            print(print("There is an error occurred in Subscriber Node"))
            print(str(e))
        display_msg_from_server(self.client_side_socket)
        self.client_side_socket.send('close'.encode())
    
