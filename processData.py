#!/usr/bin/python
# -*- coding: utf-8 -*-


class ProcessData:
    def __init__(self):
        self.time = 0
        self.version = ''
        self.serverId = ''
        self.userId = ''
        self.commitTime = ''
        self.type = ''
        self.content = ''

    def process(self, name, content):
        arr = name.split('_')
        self.time = arr[0]
        self.version = arr[1][1:]
        self.serverId = arr[2]
        self.userId = arr[3]
        self.commitTime = arr[4]
        self.type = arr[5]
        self.content = content
