#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@File    : plane_main.py
@Time    : 2020/2/27 13:41
@Author  : Yandong
@Function : 
"""
import pygame
from plane_sprite import *

class PlaneGame:

    def __init__(self):
        print("游戏初始化！")
        # 1. screen
        self.screen = pygame.display.set_mode(SCREEN_SIZE.size)
        # 2. clock
        self.clock = pygame.time.Clock()
        # 3. sprite
        self.__create_sprites()
        # 4. enemy 定时器事件
        pygame.time.set_timer(ENEMY_EVENT, 500)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

        back_ground1 = BackGround()


    def __create_sprites(self):
        # 1. 背景精灵
        back_ground2 = BackGround(is_alt=True)
        self.bg_group = pygame.sprite.Group(back_ground1, back_ground2)
        self.enemy_group = pygame.sprite.Group()
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    bg = pygame.image.load("./images/background.png")

    def start_game(self):
        print("游戏开始！")
        while True:
            # 1. clock
            self.clock.tick(FRAME)
            # 2. listen event
            self.__event_handler()
            # 3. update sprite group
            self.__update_sprites()
            # 4.碰撞检测
            self.__check_collision()
            # 5. show
            pygame.display.update()

    def __event_handler(self):

        for event in pygame.event.get():
            # quit even
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == ENEMY_EVENT:
                # print("敌机出场！！！ ")
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()



            keys_press = pygame.key.get_pressed()
            if keys_press[pygame.K_RIGHT]:
                # print('向右移动...')
                self.hero.speed += 2
            elif keys_press[pygame.K_LEFT]:
                # print("向左移动...")
                self.hero.speed -= 2
            else:
                # print("不动")
                self.hero.speed = 0


    def __check_collision(self):
        # 1.子弹 -> 敌机
        pygame.sprite.groupcollide(self.hero.bullet_group, self.enemy_group, True, True)
        # 2. 敌机 <-> 英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            # kill hero
            self.hero.kill()
            # game over
            PlaneGame.__game_over()

    def __update_sprites(self):
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        # enemy group
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        # hero
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        # bullet
        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束!")
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()