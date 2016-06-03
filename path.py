# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:55:43 2015

@author: 妥明翔
"""
# import Queue

from collections import deque
from settings import *

class Queue:
    """模拟对列"""

    def __init__(self):
        self.q = deque()

    def empty(self):
        return self.q.__len__() == 0

    def put(self, item):
        self.q.appendleft(item)

    def get(self):
        return self.q.pop()

    def size(self):
        return self.q.__len__()

def is_free(x, y, G):
    if x >= 1 and x <= WD and y >= 1 and y <= HT and G[y][x] >= 0:
        return True
    return False


def BFS(x, y, G):
    global WD, HT
    stack = Queue()
    tmp_x = tmp_y = 0
    tmp_arr = [0, 0]
    distance = 1
    tag = [[0 for col in range(WD + 1)] for row in range(HT + 1)]
    G[y][x] = 0
    tag[y][x] = 1
    if is_free(x, y - 1, G):
        stack.put([x, y - 1])
        G[y - 1][x] = distance
        tag[y - 1][x] = 1
    if is_free(x - 1, y, G):
        stack.put([x - 1, y])
        G[y][x - 1] = distance
        tag[y][x - 1] = 1
    if is_free(x, y + 1, G):
        stack.put([x, y + 1])
        G[y + 1][x] = distance
        tag[y + 1][x] = 1
    if is_free(x + 1, y, G):
        stack.put([x + 1, y])
        G[y][x + 1] = distance
        tag[y][x + 1] = 1
    while not stack.empty():
        tmp_arr = stack.get()
        x, y = tmp_arr[0], tmp_arr[1]
        if is_free(x, y - 1, G) and (not tag[y - 1][x]):
            stack.put([x, y - 1])
            G[y - 1][x] = G[y][x] + 1
            tag[y - 1][x] = 1
        if is_free(x - 1, y, G) and (not tag[y][x - 1]):
            stack.put([x - 1, y])
            G[y][x - 1] = G[y][x] + 1
            tag[y][x - 1] = 1
        if is_free(x, y + 1, G) and (not tag[y + 1][x]):
            stack.put([x, y + 1])
            G[y + 1][x] = G[y][x] + 1
            tag[y + 1][x] = 1
        if is_free(x + 1, y, G) and (not tag[y][x + 1]):
            stack.put([x + 1, y])
            G[y][x + 1] = G[y][x] + 1
            tag[y][x + 1] = 1

    return G

