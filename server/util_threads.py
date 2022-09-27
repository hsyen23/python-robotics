# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 17:16:06 2022

@author: Yen
"""

import threading


class SubscriberThread(threading.Thread):
    def __init__(self, client, data, belonged_list):
        threading.Thread.__init__(self)
        self.client = client
        self.data = data
        self.belonged_list = belonged_list
    def run(self):
        try:
            # wait for response
            self.client.recv(1024)
            self.client.send(self.data)
        except ConnectionResetError:
            print('one client lose its connection. Delete it from server')
            self.client.close()
            self.belonged_list.remove(self.client)
            print('client has been deleted')


class topic_object:
    def __init__(self, topic_name):
        self.topic = topic_name
        self.client_list = []
        
    def add_client(self, client):
        self.client_list.append(client)
    def send2clients(self, data):
        # create new thread for each client to do it
        for each_client in self.client_list:
            new_subscriber_thread = SubscriberThread(each_client, data, self.client_list)
            new_subscriber_thread.start()


class PublisherThread(threading.Thread):
    def __init__(self, threadID, client, topics):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client = client
        self.topics = topics
    def run(self):
        self.client.send('waiting for topic name'.encode())
        topic_name = self.client.recv(1024)
        topic_name = topic_name.decode()
        print('Thread-{} started as publisher for "{}"'.format(self.threadID, topic_name))
        # check whether this topic exist
        if topic_name not in self.topics:
            # establish new object which connect to all subscriber
            new_topic_object = topic_object(topic_name)
            self.topics[topic_name] = new_topic_object
        # here we just need to wait publisher send data and then send it to all subscriber
        self.client.send("{} topic is ready to send data".format(topic_name).encode())
        while True:
            try:
                data = self.client.recv(1024)
                self.topics[topic_name].send2clients(data)
                self.client.send('data has been send to subscriber...\nwait for next data'.encode())
            except ConnectionResetError:
                print('one publisher lose its connection. Close its connection and thread.')
                self.client.close()
                break
        print('Thread-{} finished'.format(self.threadID))



class ServerThread(threading.Thread):
    def __init__(self, socket, topics):
        threading.Thread.__init__(self)
        self.socket = socket
        self.thread_count = 0
        self.topics = topics
        
    def closeAllConnections(self):
        for (key, value) in self.topics.items():
            for client in value.client_list:
                client.close()
                
    def run(self):
        print("Thread-{} started as Server Thread".format(self.thread_count))
        self.thread_count += 1
        while True:
            client, address = self.socket.accept()
            print('Connected to: {}:{}'.format(address[0], address[1]))
            client.send('server connected!'.encode())
            node_type = client.recv(1024)
            node_type = node_type.decode()
            # here we know node type
            if node_type == 'publisher':
                thread_object = PublisherThread(self.thread_count, client, self.topics)
                thread_object.start()
                self.thread_count += 1
            elif node_type == 'subscriber':
                client.send('what is topic name'.encode())
                # check topic name
                subscribed_topic = client.recv(1024)
                subscribed_topic = subscribed_topic.decode()
                if subscribed_topic not in self.topics:
                    new_topic_object = topic_object(subscribed_topic)
                    self.topics[subscribed_topic] = new_topic_object
                self.topics[subscribed_topic].add_client(client)
                client.send('ready to receive data'.encode())
                print('"{}" subscriber is created'.format(subscribed_topic))
            elif node_type == 'close':
                break
            else:
                print('node type is not correct!\ndisconnect {}:{}'.format(address[0], address[1]))
                client.close()
        print("Server is closing...")
        self.socket.close()
        self.closeAllConnections()
        print("Server is closed")