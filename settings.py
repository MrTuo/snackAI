# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 09:55:43 2015

@author: 妥明翔
"""
'''
定义一些游戏中的常量
'''

# 得分label高度
LABEL_HEIGHT = 40
BLOCK_SIZE = 10# 像素大小
# 游戏区域大小(必须为20的整数倍)
FIELD_HEIGHT = 200
FIELD_WIDTH = 200

#窗口大小
WINDOW_HEIGHT = FIELD_HEIGHT + LABEL_HEIGHT + 2 * BLOCK_SIZE
WINDOW_WIDTH = FIELD_WIDTH + 2 * BLOCK_SIZE

#颜色定义
# 蛇
SNAKE_COLOR = "blue"
# 墙
WALL_COLOR = "red"
# 食物
FOOD_COLOR = "orange"

# 区域矩阵的行列数
WD = FIELD_WIDTH / 10
HT = FIELD_HEIGHT / 10
UNDEFINED = WD * HT