# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:55:43 2015

@author: 妥明翔
"""

class Queue:
    """模拟对列"""
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items)==0

    def push(self, item):
        self.items.insert(0,item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


UNDEFINED = 59*35+1
WD=10
HT=10

def is_free(x,y,G):
    if x>=1 and x<=WD and y>=1 and y<=HT and G[x][y]>=0:
        return True
    return False


def DFS(x,y,G,tag):
    global WD,HT
    stack=Queue()
    tmp_x=tmp_y=0
    tmp_arr=[0,0]
    distance=1
    tag = [[0 for col in range(WD+1)] for row in range(HT+1)]
    G[x][y]=0
    tag[x][y]=1
    if is_free(x,y-1,G):
        stack.push([x,y-1])
        G[x][y-1]=distance
        tag[x][y-1]=1
    if is_free(x-1,y,G):
        stack.push([x-1,y])
        G[x-1][y]=distance
        tag[x-1][y]=1
    if is_free(x,y+1,G):
        stack.push([x,y+1])
        G[x][y+1]=distance
        tag[x][y+1]=1
    if is_free(x+1,y,G):
        stack.push([x+1,y])
        G[x+1][y]=distance
        tag[x+1][y]=1
    while not stack.isEmpty():
        tmp_arr=stack.pop()
        x,y=tmp_arr[0],tmp_arr[1]
        if is_free(x,y-1,G) and (not tag[x][y-1]):
            stack.push([x,y-1])
            G[x][y-1]=G[x][y]+1
            tag[x][y-1]=1
        if is_free(x-1,y,G) and (not tag[x-1][y]):
            stack.push([x-1,y])
            G[x-1][y]=G[x][y]+1
            tag[x-1][y]=1
        if is_free(x,y+1,G) and (not tag[x][y+1]):
            stack.push([x,y+1])
            G[x][y+1]=G[x][y]+1
            tag[x][y+1]=1
        if is_free(x+1,y,G) and (not tag[x+1][y]):
            stack.push([x+1,y])
            G[x+1][y]=G[x][y]+1
            tag[x+1][y]=1

    return G

def create_longest_path(x,y,G,wd,ht):
    '''
    :param x:
    :param y:
    :param G:
    :return:点（x,y）上下左右可行的最小点
    '''
    tag = [[0 for col in range(wd+1)] for row in range(ht+1)]
    l1=[]
    tmp_x,tmp_y=x,y
    while G[x][y]!=0:
        step=-1
        if G[x][y]==0:#没有到目标的路径
            break
        if y-1>=1 and G[x][y-1]!=-1 and G[x][y-1]!=UNDEFINED and (not tag[x][y-1]) and G[x][y-1]>step:
            step=G[x][y-1]
            tmp_x,tmp_y=x,y-1
            tag[x][y-1]=1
        if x-1>=1 and G[x-1][y]!=-1 and G[x-1][y]!=UNDEFINED and (not tag[x-1][y]) and G[x-1][y]>step:
            step=G[x-1][y]
            tmp_x,tmp_y=x-1,y
            tag[x-1][y]=1
        if y+1<=ht and G[x][y+1]!=-1 and G[x][y+1]!=UNDEFINED and (not tag[x][y+1]) and G[x][y+1]>step:
            step=G[x][y+1]
            tmp_x,tmp_y=x,y+1
            tag[x][y+1]=1
        if x+1<=wd and G[x+1][y]!=-1  and G[x+1][y]!=UNDEFINED and (not tag[x+1][y]) and G[x+1][y]>step:
            step=G[x+1][y]
            tmp_x,tmp_y=x+1,y
            tag[x+1][y]=1

        x,y=tmp_x,tmp_y
        l1.append([tmp_x,tmp_y])
        tag[tmp_x][tmp_y]=1
    return l1

def create_shortst_path(x,y,G, wd,ht):
    '''
    :param x:
    :param y:
    :param G:
    :return:点（x,y）上下左右可行的最小点
    '''
    l1=[]
    tmp_x,tmp_y=x,y
    while G[x][y]!=0:
        step=G[x][y]
        if G[x][y] == 0:#没有到目标的路径
            break;
        if y-1>=1 and G[x][y-1]<step and G[x][y-1]!=-1:
            step=G[x][y-1]
            tmp_x,tmp_y=x,y-1
        if x-1>=1 and G[x-1][y]<step and G[x-1][y]!=-1:
            step=G[x-1][y]
            tmp_x,tmp_y=x-1,y
        if y+1<=ht and G[x][y+1]<step and G[x][y+1]!=-1:
            step=G[x][y+1]
            tmp_x,tmp_y=x,y+1
        if x+1<=wd and G[x+1][y]<step and G[x+1][y]!=-1:
            step=G[x+1][y]
            tmp_x,tmp_y=x+1,y

        x,y=tmp_x,tmp_y
        l1.append([tmp_x,tmp_y])
    return l1

G = [[UNDEFINED for col in range(WD+1)] for row in range(HT+1)]
for i in range(2,10):
    G[i][5]=-1

for i in range(5,10):
    G[2][i]=-1
    G[9][i]=-1

tag = [[0 for col in range(WD+1)] for row in range(HT+1)]

G = DFS(4,6,G,tag)

l2=create_longest_path(8,3,G,WD,HT)
l1=create_shortst_path(8,3,G,WD,HT)



a=1
print G


