# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:55:43 2015

@author: 妥明翔
"""
from Tkinter import *
import random
import path
import copy
from settings import *


class snake_game:
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

        self.food_x = FIELD_WIDTH - 3 * BLOCK_SIZE
        self.food_y = FIELD_HEIGHT - 3 * BLOCK_SIZE

        self.snake_x = self.snake_y = 3 * BLOCK_SIZE
        # 分数
        self.score = 0
        # 蛇身长度
        # self.len = 3
        # 记录蛇身的所有坐标,最长为全屏幕
        self.X = [[0, 0]] * 3

        for i in range(3):
            self.X[i] = [self.snake_x + BLOCK_SIZE * i, self.snake_y]

        '''
        G记录整个游戏区域矩阵，保存的数据为空区域为0，蛇身区域为-1,
        生成到目标地点路径后，目标区域为0,其余区域除蛇身外均为到0的最短距离，蛇身为-1
        '''
        self.G = [[0 for col in range(WD + 1)] for row in range(HT + 1)]

        # 初始化开始界面
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
        # 初始化蛇
        for i in xrange(3):
            self.snake = self.bg.create_rectangle(
                self.X[i][0], self.X[i][1], self.X[i][0] + BLOCK_SIZE, self.X[i][1] + BLOCK_SIZE, fill=SNAKE_COLOR,
                tags='snake' + str(2 - i))

        self.draw_food()
        self.score_label()

    '''View 模块'''

    def draw_wall(self):
        # 左方墙
        self.bg.create_rectangle(0, 0, BLOCK_SIZE, FIELD_HEIGHT + BLOCK_SIZE, fill=WALL_COLOR, tags="wall")
        # 右方墙
        self.bg.create_rectangle(FIELD_WIDTH + BLOCK_SIZE, 0, FIELD_WIDTH + 2 * BLOCK_SIZE,
                                 FIELD_HEIGHT + 2 * BLOCK_SIZE, fill=WALL_COLOR, tags="wall")
        # 上方墙
        self.bg.create_rectangle(0, 0, FIELD_WIDTH + BLOCK_SIZE, BLOCK_SIZE, fill=WALL_COLOR, tags="wall")
        # 下方墙
        self.bg.create_rectangle(0, FIELD_HEIGHT + BLOCK_SIZE, FIELD_WIDTH + 2 * BLOCK_SIZE,
                                 FIELD_HEIGHT + 2 * BLOCK_SIZE, fill=WALL_COLOR, tags="wall")

    def get_random_food(self):
        '''
        随机生成食物的坐标，要求不能与蛇体重合。
        '''
        while 1:
            self.food_x = random.randrange(BLOCK_SIZE, FIELD_WIDTH + BLOCK_SIZE, BLOCK_SIZE)
            self.food_y = random.randrange(BLOCK_SIZE, FIELD_HEIGHT + BLOCK_SIZE, BLOCK_SIZE)

            food = [self.food_x, self.food_y];
            if not (food in self.X):
                break;

    def draw_food(self):
        self.bg.delete("food")
        self.food = self.bg.create_rectangle(
            self.food_x, self.food_y, self.food_x + BLOCK_SIZE, self.food_y + BLOCK_SIZE, fill=FOOD_COLOR, tags="food")

    def draw_snake(self):
        self.bg.delete('snake' + str(self.tail_tag - 1))
        self.bg.create_rectangle(self.X[0][0], self.X[0][1], self.X[0][0] + BLOCK_SIZE, self.X[0][1] + BLOCK_SIZE,
                                 fill=SNAKE_COLOR, tags='snake' + str(self.head_tag))
        self.bg.delete('head')
        self.bg.create_rectangle(self.X[0][0], self.X[0][1], self.X[0][0] + BLOCK_SIZE, self.X[0][1] + BLOCK_SIZE,
                                 fill="black", tags="head")
        self.bg.delete('tail')
        self.bg.create_rectangle(self.X[-1][0], self.X[-1][1], self.X[-1][0] + BLOCK_SIZE, self.X[-1][1] + BLOCK_SIZE,
                                 fill="red", tags="tail")
        if self.direct == "up":
            self.bg.create_line(self.X[0][0], self.X[0][1] + BLOCK_SIZE, self.X[0][0] + BLOCK_SIZE,
                                self.X[0][1] + BLOCK_SIZE,
                                fill=SNAKE_COLOR, tags='snake' + str(self.head_tag))
        elif self.direct == "down":
            self.bg.create_line(self.X[0][0], self.X[0][1], self.X[0][0] + BLOCK_SIZE, self.X[0][1],
                                fill=SNAKE_COLOR, tags='snake' + str(self.head_tag))
        elif self.direct == "right":
            self.bg.create_line(self.X[0][0], self.X[0][1], self.X[0][0], self.X[0][1] + BLOCK_SIZE,
                                fill=SNAKE_COLOR, tags='snake' + str(self.head_tag))
        else:
            self.bg.create_line(self.X[0][0] + BLOCK_SIZE, self.X[0][1], self.X[0][0] + BLOCK_SIZE,
                                self.X[0][1] + BLOCK_SIZE,
                                fill=SNAKE_COLOR, tags='snake' + str(self.head_tag))

    def score_label(self):
        self.label.destroy()
        self.label = Label(self.frame2, text="Score: " + str(self.score))
        self.label.pack()

    def draw_gameover(self):
        self.bg.delete("snake")
        self.bg.delete("food")
        self.over = self.bg.create_text((FIELD_WIDTH / 2 - BLOCK_SIZE * 2, FIELD_WIDTH / 3 + 2 * BLOCK_SIZE),
                                        text="           Game Over!\n         Your score is "
                                             + str(self.score) + "\n\n", font='Helvetica -30 bold')

    '''Module 模块'''

    def is_eatten(self):
        self.eatten = False
        if self.X[0] == [self.food_x, self.food_y]:
            self.eatten = True

    def is_dead(self):
        self.dead = False
        if (self.X[0][0] not in range(BLOCK_SIZE, FIELD_WIDTH + 1)) or (
                    self.X[0][1] not in range(BLOCK_SIZE, FIELD_HEIGHT + 1)):
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
    # 手动游戏函数
    def normal_play(self):
        while self.dead == False:
            self.change_X()
            self.draw_snake()
            self.is_eatten()
            if self.eatten == True:
                self.get_random_food()
                self.draw_food()
                self.score += 1
                self.score_label()
            self.is_dead()
            # self.bg.after(self.speed)
            self.bg.update()
        else:
            self.draw_gameover()

    # 自动游戏函数

    def init_G(self, target_x, target_y, snake, G):
        '''
        初始化G，food->0;snake->-1;empty->UNDEFINED
        :return:
        '''
        for i in xrange(WD + 1):
            for j in xrange(HT + 1):
                G[j][i] = UNDEFINED
        # 食物位置置0
        G[target_y][target_x] = 0;
        # 蛇身位置置-1
        for i in snake:
            if (i[1] / 10 >= 1 and i[1] / 10 <= HT and i[0] / 10 >= 1 and i[0] / 10 <= WD):
                G[i[1] / 10][i[0] / 10] = -1
            else:
                pass

    def virtual_play_path(self):
        '''
        模拟到达食物，产生l1，之后搜索蛇头到蛇尾是否有路径，有则返回l1，否则返回空
        :return:
        '''
        # 下面两个变量保存虚拟游戏的两个信息
        v_G = copy.deepcopy(self.G)
        v_X = self.X[:]

        l1 = []
        # 还没有吃到食物
        while v_X[0][0] != self.food_x or v_X[0][1] != self.food_y:
            # 走出一步，加入到l1，更新G
            step = self.make_one_move(v_G, v_X[0][0] / BLOCK_SIZE, v_X[0][1] / BLOCK_SIZE, 0)
            l1.append(step)
            if step == -1:  # 修改虚拟蛇身数组
                v_X.insert(0, [v_X[0][0] - BLOCK_SIZE, v_X[0][1]])
            elif step == 1:
                v_X.insert(0, [v_X[0][0] + BLOCK_SIZE, v_X[0][1]])
            elif step == -2:
                v_X.insert(0, [v_X[0][0], v_X[0][1] - BLOCK_SIZE])
            elif step == 2:
                v_X.insert(0, [v_X[0][0], v_X[0][1] + BLOCK_SIZE])
            else:
                print "direction wrong in make_one_move"
            if v_X[0][0] != self.food_x or v_X[0][1] != self.food_y:
                v_X.pop();
            self.init_G(self.food_x / BLOCK_SIZE, self.food_y / BLOCK_SIZE, v_X, v_G)
            path.DFS(self.food_x / BLOCK_SIZE, self.food_y / BLOCK_SIZE, v_G)

        # 此时已经到达食物位置
        # 获取蛇尾坐标
        tail_x, tail_y = v_X[-1][0] / BLOCK_SIZE, v_X[-1][1] / BLOCK_SIZE
        self.init_G(self.food_x / 10, self.food_y / 10, v_X, v_G)
        v_G[self.food_y / 10][self.food_x / 10] = -1;  # 暂时将食物变成蛇身
        v_G[tail_y][tail_x] = 0;
        path.DFS(tail_x, tail_y, v_G)
        if self.have_path(v_X[0][0] / BLOCK_SIZE, v_X[0][1] / BLOCK_SIZE, v_G):
            return l1
        else:
            return []

    def AI_play(self):
        '''
        自动游戏主函数
        :return:
        '''
        # head_x, head_y = self.X[0][0] / 10, self.X[0][1] / 10
        self.G = [[UNDEFINED for col in range(WD + 1)] for row in range(HT + 1)]

        while (not self.is_dead()):
            target = 0
            self.init_G(self.food_x / 10, self.food_y / 10, self.X, self.G)
            path.DFS(self.food_x / 10, self.food_y / 10, self.G)
            if self.have_path(self.X[0][0] / BLOCK_SIZE, self.X[0][1] / BLOCK_SIZE, self.G):
                l2 = self.virtual_play_path()
                if l2:
                    self.make_path_move(l2)
                else:
                    target = 1
            else:
                target = 1

            if target == 1:
                tail_x, tail_y = self.X[-1][0] / 10, self.X[-1][1] / 10  # 获取蛇尾坐标
                self.init_G(self.food_x / 10, self.food_y / 10, self.X, self.G)
                # self.G[self.food_y/10][self.food_x/10] = -1 #暂时将食物变成蛇身，在走向蛇尾时不能经过食物。
                self.G[tail_y][tail_x] = 0  # 将蛇尾变成食物
                path.DFS(tail_x, tail_y, self.G)

                if self.have_path(self.X[0][0] / 10, self.X[0][1] / 10, self.G):
                    step = self.make_one_move(self.G, self.X[0][0] / BLOCK_SIZE, self.X[0][1] / BLOCK_SIZE, 1)
                else:

                    step = self.make_possible_move(self.X[0][0] / BLOCK_SIZE, self.X[0][1] / BLOCK_SIZE)
                self.move_UI(step)

    def make_path_move(self, l):
        '''
        根据给定路径l，l中为-1, 1 , -2, 2;其中-1代表左；1代表右；-2代表下；2代表上
        更新G，更新蛇身数组
        :param l:
        :return:
        '''
        for step in l:
            if not self.is_dead():
                self.move_UI(step)

    def make_one_move(self, G, x, y, choice):
        '''
        走出路径l的第一步，choice=0为最短路径第一步，choice=1为最长路径第一步。返回这一步，其中-1代表左；1代表右；-2代表下；2代表上
        :param l:
        :return:
        '''
        direct = 0
        if choice == 0:
            min = UNDEFINED
            if path.is_free(x - 1, y, G) and G[y][x - 1] < min:
                direct = -1
                min = G[y][x - 1]
            if path.is_free(x + 1, y, G) and G[y][x + 1] < min:
                direct = 1
                min = G[y][x + 1]
            if path.is_free(x, y - 1, G) and G[y - 1][x] < min:
                direct = -2
                min = G[y - 1][x]
            if path.is_free(x, y + 1, G) and G[y + 1][x] < min:
                direct = 2
                min = G[y + 1][x]
        else:
            max = -1
            if path.is_free(x - 1, y, G) and G[y][x - 1] > max and G[y][x - 1] < UNDEFINED:
                direct = -1
                max = G[y][x - 1]
            if path.is_free(x + 1, y, G) and G[y][x + 1] > max and G[y][x + 1] < UNDEFINED:
                direct = 1
                max = G[y][x + 1]
            if path.is_free(x, y - 1, G) and G[y - 1][x] > max and G[y - 1][x] < UNDEFINED:
                direct = -2
                max = G[y - 1][x]
            if path.is_free(x, y + 1, G) and G[y + 1][x] > max and G[y + 1][x] < UNDEFINED:
                direct = 2
                max = G[y + 1][x]
        return direct

    def move_UI(self, step):
        '''
        根据step更新蛇身数组，在UI中画出新的蛇，判断是否吃到食物，迟到则更新分数，产生新的食物并画出。
        :param step:
        :return:
        '''
        # UNDEFINED-3即为吃满了所有空格

        if step == -1:
            self.direct = "left"
        elif step == 1:
            self.direct = "right"
        elif step == -2:
            self.direct = "up"
        elif step == 2:
            self.direct = "down"
        else:
            print "Direction error!"
            exit(1)
        self.change_X()
        self.draw_snake()
        self.is_eatten()
        if self.eatten == True:
            self.score += 1
            if self.score == UNDEFINED - 3:
                self.draw_gameover()
                self.bg.after(10000000000)
            self.get_random_food()
            self.draw_food()
            self.score_label()

        self.is_dead()
        # self.bg.after(self.speed)
        self.bg.update()

    def make_possible_move(self, x, y):
        '''
        在没有可选路径的时候，尝试走出一步，返回这一步
        :return:
        '''
        snake = self.X[:]
        G = copy.deepcopy(self.G)
        min = UNDEFINED
        direct = 0
        if path.is_free(x - 1, y, G):
            direct = -1
            min = G[y][x - 1]
        elif path.is_free(x + 1, y, G):
            direct = 1
            min = G[y][x + 1]
        elif path.is_free(x, y - 1, G):
            direct = -2
            min = G[y - 1][x]
        elif path.is_free(x, y + 1, G):
            direct = 2
            min = G[y + 1][x]
        return direct

    def have_path(self, target_x, target_y, G):
        '''
        判断到目标位置是否有路
        :return:true ：有路 ；false：无路
        '''
        if (path.is_free(target_x - 1, target_y, G) and G[target_y][target_x - 1] < UNDEFINED) or (
                    path.is_free(target_x + 1, target_y, G) and G[target_y][target_x + 1] < UNDEFINED) or (
                    path.is_free(target_x, target_y - 1, G) and G[target_y - 1][target_x] < UNDEFINED) or (
                    path.is_free(target_x, target_y + 1, G) and G[target_y + 1][target_x] < UNDEFINED):
            return True
        else:
            return False

    def main(self, mod):
        if mod == 1:
            self.normal_play()
        elif mod == 2:
            self.AI_play()

        self.window.mainloop()


if __name__ == '__main__':
    snake_game = snake_game()
    # 这里接受的参数为游戏模式（1为手动模式，2为AI模式）:
    snake_game.main(2)
