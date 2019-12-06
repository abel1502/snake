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
        self.length = 22
        self.food = Food("food", -1)
        self.food.instantiate(self.gameObject.getRoot())
        self.eat()
        
    def eat(self):
        self.length += 1
        scene = self.gameObject.getRoot()
        foodSize = self.food.getComponent(BoxTexture).size
        _x = foodSize[0] / 2 + random.random() * (scene.screen.get_rect().width - foodSize[0])
        _y = foodSize[0] / 2 + random.random() * (scene.screen.get_rect().height - foodSize[1])
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
        self.tail.addTrail(tr.pos, self.moveDir)
        # TODO: Collider Component
        headCollider = self.head.getComponent(BoxCollider)
        foodCollider = self.food.getComponent(BoxCollider)
        if Collider.collide(headCollider, foodCollider):
            self.eat()
        tailCollider = self.tail.getComponent(TailCollider)
        if Collider.collide(headCollider, tailCollider):
            print("Dead!")
            self.gameObject.getRoot().stop()


class Head(GameObject):
    def __init__(self, name=None, zIndex=0):
        super().__init__(name)
        self.addComponent(BoxTexture, (32, 32), (255, 255, 255), zIndex=zIndex, offset=(-16, -16))
        self.addComponent(BoxCollider, (32, 32), offset=(-16, -16))


class Food(GameObject):
    def __init__(self, name=None, zIndex=0):
        super().__init__(name)
        self.addComponent(BoxTexture, (16, 16), (255, 0, 0), zIndex=zIndex, offset=(-8, -8))
        self.addComponent(BoxCollider, (16, 16), offset=(-8, -8))


class TailCollider(Collider):
    def __init__(self, gameObject, width):
        super().__init__(gameObject)
        self.width = width
    
    def _collide(self, other):
        if isinstance(other, BoxCollider):
            otherRect = other.getRect()
            trail = self.gameObject.getTrail(self.width)
            #print(trail)
            if not self.gameObject.trail[0][1]:
                trail = trail[1:]
            if len(self.gameObject.trail) >= 2 and not self.gameObject.trail[1][1]:
                trail = trail[1:]
            for rect in trail:
                if otherRect.colliderect(rect):
                    return True
            return False
        return NotImplemented


class TailTexture(Texture):
    def __init__(self, gameObject, width, color, zIndex=0):
        super().__init__(gameObject, zIndex=zIndex)
        self.color = color
        self.width = width
    
    def on_draw(self, drawBuf):
        for rect in self.gameObject.getTrail(self.width):
            self.draw(drawBuf, self.color, rect)


class Tail(GameObject):
    def __init__(self, name=None, zIndex=0):
        super().__init__(name)
        self.trail = deque()
        self.addComponent(TailTexture, 32, (0, 255, 0), zIndex=zIndex)
        self.addComponent(TailCollider, 32)
    
    def addTrail(self, pos, moveDir):
        gap = False
        if len(self.trail) >= 2:
            lastDir = self.trail[-1][0] - self.trail[-2][0]
            curDir = pos - self.trail[-1][0]
            if curDir * moveDir < 0:
                gap = True
            elif curDir * lastDir > 0:
                self.trail.pop()
        self.trail.append((pos, gap))
        # !Clear
        if len(self.trail) >= 10 ** 4:
            self.trail.popleft()
    
    def getTrail(self, width):
        trail = list(self.trail)[::-1]
        res = []
        rem = self.getParent().getComponent(SnakeController).length * 32
        for i in range(1, len(trail)):
            prevPoint = trail[i - 1][0]
            curPoint = trail[i][0]
            if trail[i - 1][1]:
                continue
            segLen = abs(curPoint - prevPoint)
            rem -= segLen
            dir = (curPoint - prevPoint).normalize()
            radius = dir.rotate90() * (width / 2)
            if rem <= 0:
                r0 = prevPoint - radius - dir * 16
                r1 = curPoint + dir * rem + radius + dir * 16
                rect = Vector2.rect(r0, r1)
                res.append(rect)
                break
            r0 = prevPoint - radius - dir * 16
            r1 = curPoint + radius + dir * 16
            rect = Vector2.rect(r0, r1)
            res.append(rect)
        return res


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