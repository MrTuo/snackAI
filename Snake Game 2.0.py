# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:55:43 2015

@author: 妥明翔
"""
from Tkinter import *
import random
import path

# 窗口大小（所有大小必须为10的整数倍）
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 600

# 得分label高度
LABEL_HEIGHT = 40

# 游戏区域大小
FIELD_HEIGHT = WINDOW_HEIGHT - LABEL_HEIGHT
FIELD_WIDTH = WINDOW_WIDTH

# 像素大小
BLOCK_SIZE = 10

# 蛇
SNAKE_COLOR = "blue"
# 墙
WALL_COLOR = "red"
# 食物
FOOD_COLOR = "orange"

#区域矩阵的行列数
WD = FIELD_WIDTH/10
HT=FIELD_HEIGHT/10

UNDEFINED = WD*HT

class snack_game:
    def __init__(self):
        # 属性：
        self.direct = "left"
        self.dead = False
        self.eatten = False
        self.speed = 200
        # step_count用于统计蛇走过的步数，主要用于为每个蛇身小方块设置唯一的tag
        # 下面两个tag分别记录蛇头和蛇尾小方块的tag。
        self.step_conut = 0
        self.head_tag = 2
        self.tail_tag = 0

        # 随机生成食物的坐标(生成在窗口的上半部分)
        self.food_x = random.randrange(
            BLOCK_SIZE, FIELD_WIDTH - BLOCK_SIZE * 2, BLOCK_SIZE)
        self.food_y = random.randrange(BLOCK_SIZE, FIELD_HEIGHT / 2 - BLOCK_SIZE, BLOCK_SIZE)
        # 随机生成蛇头坐标（生成在窗口的下半部分,靠右5步，不然一出来就死了OTZ）
        self.snack_x = random.randrange(BLOCK_SIZE * 5, FIELD_WIDTH - BLOCK_SIZE * 5, BLOCK_SIZE)
        self.snack_y = random.randrange(FIELD_HEIGHT / 2, FIELD_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        # 分数
        self.score = 0
        # 蛇身长度
        # self.len = 3
        # 记录蛇身的所有坐标,最长为全屏幕
        self.X = [[0, 0]] * 3

        for i in range(3):
            self.X[i] = [self.snack_x + BLOCK_SIZE * i, self.snack_y]

        '''
        G记录整个游戏区域矩阵，保存的数据为空区域为0，蛇身区域为-1,
        生成到目标地点路径后，目标区域为0,其余区域除蛇身外均为到0的最短距离，蛇身为-1
        '''
        self.G=[[0 for col in range(WD+1)] for row in range(HT+1)]

    '''View 模块'''

    def draw_wall(self):
        # 左方墙
        self.bg.create_rectangle(0, 0, BLOCK_SIZE, FIELD_HEIGHT, fill=WALL_COLOR, tags="wall")
        # 右方墙
        self.bg.create_rectangle(FIELD_WIDTH - BLOCK_SIZE, 0, FIELD_WIDTH, FIELD_HEIGHT, fill=WALL_COLOR, tags="wall")
        # 上方墙
        self.bg.create_rectangle(0, 0, FIELD_WIDTH, BLOCK_SIZE, fill=WALL_COLOR, tags="wall")
        # 下方墙
        self.bg.create_rectangle(0, FIELD_HEIGHT - BLOCK_SIZE, FIELD_WIDTH, FIELD_HEIGHT, fill=WALL_COLOR, tags="wall")

    def get_random_food(self):
        '''
        随机生成食物的坐标，要求不能与蛇体重合。（待优化，后期会很慢）
        '''
        valid = 1
        while valid == 1:
            self.food_x = random.randrange(BLOCK_SIZE, FIELD_WIDTH - 2 * BLOCK_SIZE, BLOCK_SIZE)
            self.food_y = random.randrange(BLOCK_SIZE, FIELD_HEIGHT - 2 * BLOCK_SIZE, BLOCK_SIZE)
            for i in self.X:
                if self.food_x == i[0] and self.food_y == i[1]:
                    valid = 1
                    break
            valid = 0

    def draw_food(self):
        self.bg.delete("food")
        self.food = self.bg.create_rectangle(
            self.food_x, self.food_y, self.food_x + BLOCK_SIZE, self.food_y + BLOCK_SIZE, fill=FOOD_COLOR, tags="food")

    def draw_snack(self):
        self.bg.delete('snake' + str(self.tail_tag - 1))
        '''
        for i in self.X:
            self.snack = self.bg.create_rectangle(
                i[0], i[1], i[0] + BLOCK_SIZE, i[1] + BLOCK_SIZE, fill=SNAKE_COLOR, tags="snack")
        '''
        self.bg.create_rectangle(self.X[0][0], self.X[0][1], self.X[0][0] + BLOCK_SIZE, self.X[0][1] + BLOCK_SIZE,
                                 fill=SNAKE_COLOR, tags='snake' + str(self.head_tag))

    def score_label(self):
        self.label.destroy()
        if self.eatten == True:
            self.score += 10

        self.label = Label(self.frame2, text="Score: " + str(self.score))
        self.label.pack()

    def draw_gameover(self):
        self.bg.delete("snack")
        self.bg.delete("food")
        self.over = self.bg.create_text((FIELD_WIDTH / 2 - BLOCK_SIZE * 2, FIELD_WIDTH / 3 + 2 * BLOCK_SIZE),
                                        text="           Game Over!\n         Your score is "
                                             + str(self.score) + "\n\n", font='Helvetica -30 bold')

    #                                    +"Press \"Enter \"to continue.\n"\
    #                                    +"      Press \"Esc\" to exit."
    #

    '''Module 模块'''

    def is_eatten(self):
        self.eatten = False
        if self.X[0] == [self.food_x, self.food_y]:
            self.eatten = True

    def is_dead(self):
        self.dead = False
        if (self.X[0][0] not in range(BLOCK_SIZE, FIELD_WIDTH - 2 * BLOCK_SIZE + 1)) or (
            self.X[0][1] not in range(BLOCK_SIZE, FIELD_HEIGHT - 2 * BLOCK_SIZE + 1)):
            self.dead = True
        else:
            for i in range(1, self.head_tag - self.tail_tag + 1):
                if self.X[i] == self.X[0]:
                    self.dead = True
                    break

    def change_X(self):
        # 修改蛇身数组
        if self.direct == 'left':
            self.X.insert(0, [self.X[0][0] - BLOCK_SIZE, self.X[0][1]])
        elif self.direct == 'up':
            self.X.insert(0, [self.X[0][0], self.X[0][1] - BLOCK_SIZE])
        elif self.direct == 'right':
            self.X.insert(0, [self.X[0][0] + BLOCK_SIZE, self.X[0][1]])
        elif self.direct == 'down':
            self.X.insert(0, [self.X[0][0], self.X[0][1] + BLOCK_SIZE])
        if self.eatten == False:
            self.tail_tag += 1
            self.X.pop()
        self.head_tag += 1



    '''Control 模块'''

    def control(self, event):

        if event.keycode == 37 and self.direct != 'right':
            self.direct = 'left'
        elif event.keycode == 38 and self.direct != 'down':
            self.direct = 'up'
        elif event.keycode == 39 and self.direct != 'left':
            self.direct = 'right'
        elif event.keycode == 40 and self.direct != 'up':
            self.direct = 'down'
        # 调整蛇的速度
        elif event.keycode == 87:
            self.speed -= 25
        elif event.keycode == 83:
            self.speed += 25

    '''自动游戏&手动游戏'''
    #手动游戏函数
    def normal_play(self):
        self.change_X()
        self.draw_snack()
        self.is_eatten()
        if self.eatten == True:
            self.get_random_food()
            self.draw_food()

    #自动游戏函数
    def init_G(self):
        '''
        初始化G，food->0;snake->-1;empty->UNDEFINED
        :return:
        '''
        G = [[UNDEFINED for col in range(WD+1)] for row in range(HT+1)]
        G[self.food_x][self.food_y]=0;
        for i in self.X:
            G[i[0]/10][i[1]/10]=-1;

    def virtual_play_path(self):
        '''
        模拟到达食物，产生l1，之后搜索蛇头到蛇尾是否有路径，有则返回l1，否则返回空
        :return:
        '''
        pass

    def AI_play(self):
        '''
        自动游戏主函数
        :return:
        '''
        head_x,head_y=self.X[0][0]/10,self.X[0][1]/10
        self.init_G()
        path.DFS(head_x,head_y,self.G)
        l2=path.create_shortst_path(head_x,head_y)
        if self.have_path(head_x,head_y):


    def make_path_move(self,l):
        '''
        根据给定路径l，更新G
        :param l:
        :return:
        '''

    def make_one_move(self,l):
        '''
        走出路径l的第一步，更新G
        :param l:
        :return:
        '''

    def make_possible_move(self):
        '''
        在没有可选路径的时候，尝试走出一步，更新G
        :return:
        '''

    def have_path(self,target_x,target_y):
        '''
        判断到目标位置是否有路
        :return:true ：有路 ；false：无路
        '''

    def main(self, mod):

        self.window = Tk()
        self.window.geometry()
        self.window.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.window.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.window.title("Snake game")

        self.frame1 = Frame(self.window, relief=GROOVE)
        self.frame2 = Frame(self.window, relief=RAISED, height=LABEL_HEIGHT, width=WINDOW_WIDTH)
        self.bg = Canvas(self.frame1, width=WINDOW_WIDTH, height=WINDOW_HEIGHT - LABEL_HEIGHT, bg="white")

        self.label = Label(self.frame2, text="Score: " + str(self.score))

        self.frame1.pack()
        self.frame2.pack(fill=BOTH)
        self.label.pack(side=LEFT)
        self.bg.pack(fill=BOTH)
        self.bg.bind('<Key>', self.control)
        self.bg.focus_set()
        self.draw_wall()
        # self.draw_food()
        # 初始化蛇
        for i in xrange(3):
            self.snack = self.bg.create_rectangle(
                self.X[i][0], self.X[i][1], self.X[i][0] + BLOCK_SIZE, self.X[i][1] + BLOCK_SIZE, fill=SNAKE_COLOR,
                tags='snake' + str(2 - i))

        self.draw_food()
        while self.dead == False:
            if mod == 1:
                self.normal_play()
            elif mod == 2:
                self.AI_play()

            self.score_label()
            self.is_dead()

            self.bg.after(self.speed)
            self.bg.update()
        else:
            self.draw_gameover()

        self.window.mainloop()


snack_game = snack_game()
snack_game.main(1)
