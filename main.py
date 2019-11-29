import pygame
from engine import *
import random
from collections import deque


class SnakeController(Behaviour):
    def on_start(self):
        self.speed = 0.15
        self.moveDir = Vector2(1, 0)
        self.head = Head("snakeHead", 1)
        self.head.instantiate(self.gameObject, pos=Vector2(0, 0))
        self.tail = Tail("snakeTail", 0.5)
        self.tail.instantiate(self.gameObject, pos=Vector2(0, 0))
        self.length = 0
        self.food = Food("food", -1)
        self.food.instantiate(self.gameObject.getRoot())
        self.eat()
        
    def eat(self):
        self.length += 1
        scene = self.gameObject.getRoot()
        foodSize = self.food.getComponent(BoxTexture).size
        _x = random.random() * (scene.screen.get_rect().width - foodSize[0])
        _y = random.random() * (scene.screen.get_rect().height - foodSize[1])
        self.food.transform.pos = Vector2(_x, _y)
    
    def on_keydown(self, key, mod, unicode, scancode):
        newMoveDir = self.moveDir
        if key in [pygame.K_w, pygame.K_UP]:
            newMoveDir = Vector2(0, -1)
        elif key in [pygame.K_s, pygame.K_DOWN]:
            newMoveDir = Vector2(0, 1)
        elif key in [pygame.K_a, pygame.K_LEFT]:
            newMoveDir = Vector2(-1, 0)
        elif key in [pygame.K_d, pygame.K_RIGHT]:
            newMoveDir = Vector2(1, 0)
        if newMoveDir @ self.moveDir == 0:
            return
        self.moveDir = newMoveDir
    
    def on_tick(self, scene):
        tr = self.head.transform
        tr.pos += self.moveDir * self.speed * scene.clock.get_time()
        tr.pos = tr.parent.fromAbsolute(tr.getAbsolutePosition().clamp(scene.screen.get_rect()))
        self.tail.addTrail(tr.pos)
        # TODO: Collider Component
        headCollider = self.head.getComponent(BoxTexture).getRect()
        foodCollider = self.food.getComponent(BoxTexture).getRect()
        if headCollider.colliderect(foodCollider):
            self.eat()


class Head(GameObject):
    def __init__(self, name=None, zIndex=0):
        super().__init__(name)
        self.addComponent(BoxTexture, (32, 32), (255, 255, 255), zIndex=zIndex, offset=(-16, -16))


class Food(GameObject):
    def __init__(self, name=None, zIndex=0):
        super().__init__(name)
        self.addComponent(BoxTexture, (16, 16), (255, 0, 0), zIndex=zIndex, offset=(-8, -8))


class TailCollider(Collider):
    pass


class TailTexture(Texture):
    def __init__(self, gameObject, width, color, zIndex=0):
        super().__init__(gameObject, zIndex=zIndex)
        self.color = color
        self.width = width
    
    def on_draw(self, drawBuf):
        trail = list(self.gameObject.trail)[::-1]
        rem = self.gameObject.getParent().getComponent(SnakeController).length * 32
        for i in range(1, len(trail)):
            prevPoint = trail[i - 1][0]
            curPoint = trail[i][0]
            segLen = abs(curPoint - prevPoint)
            rem -= segLen
            dir = (curPoint - prevPoint).normalize()
            radius = dir.rotate90() * (self.width / 2)
            if rem <= 0:
                r0 = prevPoint - radius - dir
                r1 = curPoint + dir * rem + radius + dir
                rect = Vector2.rect(r0, r1)
                self.draw(drawBuf, self.color, rect)
                break
            r0 = prevPoint - radius - dir
            r1 = curPoint + radius + dir
            rect = Vector2.rect(r0, r1)
            self.draw(drawBuf, self.color, rect)


class Tail(GameObject):
    def __init__(self, name=None, zIndex=0):
        super().__init__(name)
        self.trail = deque()
        self.addComponent(TailTexture, 32, (0, 255, 0), zIndex=zIndex)
    
    def addTrail(self, pos, food=False):
        if len(self.trail) >= 2:
            lastDir = self.trail[-1][0] - self.trail[-2][0]
            curDir = pos - self.trail[-1][0]
            if curDir @ lastDir == 0:
                if not self.trail[-1][1]:
                    self.trail.pop()
        self.trail.append((pos, food))
        # !Clear
        if len(self.trail) >= 10 ** 5:
            self.trail.popleft()


def main():
    pygame.init()
    size = 800, 600
    
    scene = Scene(size=size, bgColor=(0, 0, 0))
    snake = GameObject()
    snake.addComponent(SnakeController)
    snake.instantiate(scene)
    scene.run()

try:
    main()
finally:
    pygame.quit()