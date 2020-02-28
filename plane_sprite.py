#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File    : plane_sprite.py
@Time    : 2020/2/27 12:23
@Author  : Yandong
@Function : 
"""
import pygame
import random

# screen
SCREEN_SIZE = pygame.Rect(0, 0, 480, 700)
FRAME = 60
ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):

    def __init__(self, image_name, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect() # size (0,0,length, width)
        self.speed = speed

    def update(self):
        # 垂直方向上移动
        self.rect.y += self.speed

class BackGround(GameSprite):
    """
    父类不满足子类要求，派生出子类改写。
    """
    def __init__(self, is_alt= False):
        super().__init__("./images/background.png")
        if is_alt:
            self.rect.y = -self.rect.height
        else:
            pass

    def update(self):
        # 1. 父类实现
        super().update()
        # 2. 判断是否移除屏幕，返回起始位置
        if self.rect.y >= SCREEN_SIZE.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """
    敌机
    """
    def __init__(self):
        # 1.父类，指定图片
        super().__init__("./images/enemy1.png")
        # 2.初始速度
        self.speed = random.randint(1, 3)
        # 3.初始位置
        self.rect.bottom = 0
        max_x = SCREEN_SIZE.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        # 1.父类，更新位置
        super().update()
        # 2. 飞出屏幕，清除
        if self.rect.y >= SCREEN_SIZE.height:
            # print("飞机飞出屏幕！！！")
            # kill 销毁精灵
            self.kill()

    def __del__(self):
        # print('敌机 %s 实例销毁...' % self.rect)
        pass


class Hero(GameSprite):

    # 初始化，加载图片，子弹组属性
    def __init__(self):
        super().__init__("./images/me1.png", 0)
        self.rect.centerx = SCREEN_SIZE.centerx
        self.rect.bottom = SCREEN_SIZE.bottom - 120
        self.bullet_group = pygame.sprite.Group()

    # update 位置
    def update(self):
        self.rect.x += self.speed
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= SCREEN_SIZE.width - self.rect.width:
            self.rect.x = SCREEN_SIZE.width - self.rect.width

    # fire
    def fire(self):

        for i in (0, 1, 2):
            bullet = Bullet()
            # pos
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            self.bullet_group.add(bullet)


class Bullet(GameSprite):

    def __init__(self):
        super().__init__('./images/bullet1.png', -2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()