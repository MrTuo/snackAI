# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:55:43 2015

@author: 妥明翔
"""
from Tkinter import*
import random

#窗口大小
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 600

#得分label高度
LABEL_HEIGHT = 40

# 游戏区域大小
FIELD_HEIGHT = WINDOW_HEIGHT - LABEL_HEIGHT
FIELD_WIDTH = WINDOW_WIDTH

#像素大小
BLOCK_SIZE = 10

# 蛇
# 蛇的每一小块的大小
SNAKE_COLOR = "blue"
# 墙
# 墙的厚度
WALL_COLOR = "red"

# 食物
# 食物大小
FOOD_COLOR = "orange"


class snack_game:

    def __init__(self):
        # 属性：
        self.direct = "left"
        self.dead = False
        self.eatten = False
        self.speed = 200
        # 随机生成食物的坐标(生成在窗口的上半部分)
        self.food_x = random.randrange(
            BLOCK_SIZE, FIELD_WIDTH - BLOCK_SIZE * 2, BLOCK_SIZE)
        self.food_y = random.randrange(BLOCK_SIZE, FIELD_HEIGHT/2 - BLOCK_SIZE, BLOCK_SIZE)
        # 随机生成蛇头坐标（生成在窗口的下半部分,靠右5步，不然一出来就死了OTZ）
        self.snack_x = random.randrange(BLOCK_SIZE*5, FIELD_WIDTH - BLOCK_SIZE*5, BLOCK_SIZE)
        self.snack_y = random.randrange(FIELD_HEIGHT/2, FIELD_HEIGHT-BLOCK_SIZE, BLOCK_SIZE)
        self.score = 0
        # 记录蛇身的所有坐标，初始化为3个
        self.X = [0, 0, 0]
        print self.food_x,self.food_y,
        print self.snack_x,self.snack_y,
        for i in range(3):
            self.X[i] = [self.snack_x + BLOCK_SIZE * i, self.snack_y]

    '''View 模块'''

    def draw_wall(self):
        #左方墙
        self.bg.create_rectangle(0, 0, BLOCK_SIZE, FIELD_HEIGHT, fill=WALL_COLOR)
        #右方墙
        self.bg.create_rectangle(FIELD_WIDTH - BLOCK_SIZE, 0, FIELD_WIDTH, FIELD_HEIGHT, fill=WALL_COLOR)
        #上方墙
        self.bg.create_rectangle(0, 0, FIELD_WIDTH, BLOCK_SIZE, fill=WALL_COLOR)
        #下方墙
        self.bg.create_rectangle(0, FIELD_HEIGHT - BLOCK_SIZE, FIELD_WIDTH, FIELD_HEIGHT, fill=WALL_COLOR)

    def get_random_food(self):
        '''
        随机生成食物的坐标，要求不能与蛇体重合。
        '''
        valid=1
        while valid==1:
            self.food_x = random.randrange(BLOCK_SIZE, FIELD_WIDTH-2*BLOCK_SIZE, BLOCK_SIZE)
            self.food_y = random.randrange(BLOCK_SIZE, FIELD_HEIGHT-2*BLOCK_SIZE, BLOCK_SIZE)
            for i in self.X:
                if self.food_x==i[0] and self.food_y==i[1]:
                    valid=1
                    break
            valid=0


    def draw_food(self):
        self.bg.delete("food")
        self.food = self.bg.create_rectangle(
            self.food_x, self.food_y, self.food_x + BLOCK_SIZE, self.food_y + BLOCK_SIZE, fill=FOOD_COLOR, tags="food")

    def draw_snack(self):
        self.bg.delete("snack")
        for i in self.X:
            self.snack = self.bg.create_rectangle(
                i[0], i[1], i[0] + BLOCK_SIZE, i[1] + BLOCK_SIZE, fill=SNAKE_COLOR, tags="snack")

    def score_label(self):
        self.label.destroy()
        if self.eatten == True:
            self.score += 10
            print self.score
        self.label = Label(self.frame2, text="Score: " + str(self.score))
        self.label.pack()

    def draw_gameover(self):
        self.bg.delete("snack")
        self.bg.delete("food")
        self.over = self.bg.create_text((FIELD_WIDTH/2-BLOCK_SIZE*2, FIELD_WIDTH/3+2*BLOCK_SIZE), text="           Game Over!\n         Your score is "
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
        if (self.X[0][0] not in range(BLOCK_SIZE, FIELD_WIDTH-2*BLOCK_SIZE+1)) or (self.X[0][1] not in range(BLOCK_SIZE, FIELD_HEIGHT-2*BLOCK_SIZE+1)):
            self.dead = True
        else:
            for i in range(1, len(self.X)):
                if self.X[i] == self.X[0]:
                    self.dead = True
                    break

    def change_X(self):
        #修改蛇身数组
        if self.direct == 'left':
            self.X.insert(0, [self.X[0][0] - BLOCK_SIZE, self.X[0][1]])
        elif self.direct == 'up':
            self.X.insert(0, [self.X[0][0], self.X[0][1] - BLOCK_SIZE])
        elif self.direct == 'right':
            self.X.insert(0, [self.X[0][0] + BLOCK_SIZE, self.X[0][1]])
        elif self.direct == 'down':
            self.X.insert(0, [self.X[0][0], self.X[0][1] + BLOCK_SIZE])
        if self.eatten == False:
            self.X.pop()

    '''Control 模块'''

    def control(self, event):

        if event.keycode == 37:
            self.direct = 'left'
        elif event.keycode == 38:
            self.direct = 'up'
        elif event.keycode == 39:
            self.direct = 'right'
        elif event.keycode == 40:
            self.direct = 'down'
        #调整蛇的速度
        elif event.keycode == 87:
            self.speed -= 25
        elif event.keycode == 83:
            self.speed += 25

    def main(self):

        self.window = Tk()
        self.window.geometry()
        self.window.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.window.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.window.title("Snake game")

        self.frame1 = Frame(self.window, relief=GROOVE)
        self.frame2 = Frame(self.window, relief=RAISED, height=LABEL_HEIGHT, width=WINDOW_WIDTH)
        self.bg = Canvas(self.frame1, width=WINDOW_WIDTH, height=WINDOW_HEIGHT-LABEL_HEIGHT, bg="white")
       
        self.label = Label(self.frame2, text="Score: " + str(self.score))

        self.frame1.pack()
        self.frame2.pack(fill=BOTH)
        self.label.pack(side=LEFT)
        self.bg.pack(fill=BOTH)
        self.bg.bind('<Key>', self.control)
        self.bg.focus_set()
        self.draw_wall()
        self.draw_food()
        while self.dead == False:
            if self.eatten == True:
                self.get_random_food()
                self.draw_food()
            self.draw_snack()
            self.is_eatten()
            self.score_label()
            self.is_dead()
            self.change_X()

            self.bg.after(self.speed)
            self.bg.update()
        else:
            self.draw_gameover()

        self.window.mainloop()

snack_game = snack_game()
snack_game.main()
