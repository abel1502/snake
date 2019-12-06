import pygame
import math
from collections import deque
from enum import Enum
import sys


class Vector2:
    def __init__(self, *args):
        if len(args) == 0:
            self = Vector2(0, 0)
        elif len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                assert len(args[0]) == 2
                assert isinstance(args[0][0], (int, float)) and isinstance(args[0][1], (int, float))
                self.x = args[0][0]
                self.y = args[0][1]
            elif isinstance(args[0], Vector2):
                self.x = args[0].x
                self.y = args[0].y
            else:
                assert False
        elif len(args) == 2:
            assert isinstance(args[0], (int, float)) and isinstance(args[1], (int, float))
            self.x = args[0]
            self.y = args[1]
        else:
            assert False
    
    def tuple(self):
        return (self.x, self.y)
    
    def __round__(self, ndigits=0):
        return Vector2(round(self.x, ndigits=ndigits), round(self.y, ndigits=ndigits))
    
    def __str__(self):
        return "({}, {})".format(self.x, self.y)
    
    def __repr__(self):
        return "Vector2({}, {})".format(self.x, self.y)
    
    def __complex__(self):
        return complex(self.x, self.y)
    
    def __abs__(self):
        return math.hypot(self.x, self.y)
    
    def angle(self, other=None):
        if other is None:
            return math.atan2(self.y, self.x)
        assert isinstance(other, Vector2)
        return math.atan2(self @ other, self * other)
    
    @staticmethod
    def fromPolar(r, phi):
        return Vector2(r * math.cos(phi), r * math.sin(phi))
    
    def toPolar(self):
        return (abs(self), self.angle())
    
    def copy(self):
        return Vector2(self)
    
    def normalize(self):
        return self / abs(self)
    
    def lerp(self, other, time=0.5):
        return self * (1 - time) + other * time
    
    def _rotate(self, sin, cos, rel=None):
        if rel is None:
            return Vector2(self.x * cos - self.y * sin, self.x * sin + self.y * cos)
        return (self - rel)._rotate(sin, cos) + rel
    
    def rotate(self, phi, rel=None):
        return self._rotate(math.sin(phi), math.cos(phi), rel=rel)
    
    def rotate90(self, rel=None):
        return self._rotate(1, 0, rel=rel)
    
    def clamp(self, rect, loop=True):
        if loop:
            return Vector2((self.x - rect.x) % rect.width + rect.x, (self.y - rect.y) % rect.height + rect.y)
        return Vector2(max(rect.left, min(self.x, rect.right)), max(rect.top, min(self.y, rect.bottom)))
    
    @staticmethod
    def rect(v1, v2):
        x1, y1 = round(v1).tuple()
        x2, y2 = round(v2).tuple()
        size = tuple(map(abs, round(v2 - v1).tuple()))
        return pygame.Rect((min(x1, x2), min(y1, y2)), size)
    
    # ===[ Operators ]===
    
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return self + -other
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        return NotImplemented
    
    def __matmul__(self, other):
        if isinstance(other, Vector2):
            return self.x * other.y + self.y * other.x
        return NotImplemented
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self * (1 / other)
        return NotImplemented
    
    def __rmul__(self, other):
        if isinstance(other, Vector2):
            return self * other
        if isinstance(other, (int, float)):
            return self * other
        return NotImplemented
    
    def __iadd__(self, other):
        self = self + other
        return self
    
    def __isub__(self, other):
        self = self - other
        return self
    
    def __imul__(self, other):
        assert isinstance(other, (int, float))
        self = self * other
        return self
    
    def __itruediv__(self, other):
        self = self / other
        return self
    
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def __pos__(self):
        return Vector2(self.x, self.y)
    
    # ===[ Comparisons ]===
    
    def __eq__(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self == other
    
    def __lt__(self, other):
        return self.toPolar() < other.toPolar()
    
    def __le__(self, other):
        return self < other or self == other
    
    def __gt__(self, other):
        return other >= self
    
    def __ge__(self, other):
        return other > self


#class IndexedContainer:
#    def __init__(self):
#        self.elements = {}
#        self.lastId = -1
#    
#    def add(self, elem):
#        self.lastId += 1
#        self.set(self.lastId, elem)
#        return self.lastId
#    
#    def pop(self, id):
#        return self.elements.pop(id)
#    
#    def clear(self):
#        self.elements = {}
#    
#    def set(self, id, elem):
#        self.elements[id] = elem
#    
#    def get(self, id):
#        return self.elements[id]
#    
#    def getAll(self, withIds=False):
#        if withIds:
#            return self.elements.items()
#        return self.elements.values()


class Component:
    def __init__(self, gameObject):
        self.gameObject = gameObject


class GameObject:
    def __init__(self, name=None):
        self.name = name
        self.components = set()
        self.tags = set()
    
    def instantiate(self, parent, *args, **kwargs):
        self.addComponent(Transform, parent=parent.transform, *args, **kwargs)
    
    @property
    def transform(self):
        return self.getComponent(Transform)
    
    def destroy(self):
        pass  # TODO!
    
    def assignParent(self, parent):
        assert isinstance(parent, GameObject)
        self.transform.assignParent(parent.transforn)
    
    def addChild(self, child):
        assert isinstance(child, GameObject)
        self.transform.addChild(child.transform)
    
    def removeChild(self, child):
        assert isinstance(child, GameObject)
        self.transform.removeChild(child.transform)
    
    def clearChildren(self):
        self.transform.clearChildren()
    
    def getChildren(self):
        return set(map(lambda x: x.gameObject, self.transform.getChildren()))
    
    def getParent(self):
        return self.transform.getParent().gameObject
    
    def getRoot(self):
        return self.transform.getRoot().gameObject
    
    def findChildByName(self, name):
        return self.transform.findChildByName(name).gameObject
    
    def findChildByTag(self, tag):
        return self.transform.findChildByTag(tag).gameObject
    
    def findChildrenByTag(self, tag):
        return list(map(lambda x: x.gameObject, self.transform.findChildrenByTag(tag)))
    
    def broadcastMessage(self, msg, *args, targetComponent=Component, **kwargs):
        self.transform.broadcastMessage(msg, *args, targetComponent=targetComponent, **kwargs)
    
    def addComponent(self, comp, *args, **kwargs):
        comp = comp(self, *args, **kwargs)
        assert isinstance(comp, Component)
        self.components.add(comp)
    
    def removeComponent(self, comp):
        assert isinstance(comp, Component)
        self.components.discard(comp)
    
    def clearComponents(self):
        self.components.clear()
    
    def getComponents(self, type=Component):
        res = []
        for comp in self.components:
            if isinstance(comp, type):
                res.append(comp)
        return res
    
    def getComponent(self, type=Component):
        for comp in self.components:
            if isinstance(comp, type):
                return comp
        assert False
    
    def handleMessage(self, msg, *args, targetComponent=Component, **kwargs):
        handler = "on_{}".format(msg)
        #print(self.name, handler)
        for comp in self.getComponents(targetComponent):
            if hasattr(comp, handler):
                getattr(comp, handler)(*args, **kwargs)


class Transform(Component):
    def __init__(self, gameObject, parent=None, pos=(0, 0), priority=0):
        super().__init__(gameObject)
        self.priority = priority
        self.pos = Vector2(pos)
        self.parent = None
        self.assignParent(parent)
        self.children = set()
    
    def assignParent(self, parent):
        if self.parent is not None:
            self.parent.removeChild(self)
        if parent is None:
            self.parent = None
            return
        assert isinstance(parent, Transform)
        parent.addChild(self)
        self.parent = parent
    
    def addChild(self, child):
        assert isinstance(child, Transform)
        self.children.add(child)
    
    def removeChild(self, child):
        assert isinstance(child, Transform)
        self.children.discard(child)
    
    def clearChildren(self):
        self.children.clear()
    
    def getChildren(self):
        return sorted(self.children, key=lambda x: x.priority)
    
    def getParent(self):
        return self.parent
    
    def getRoot(self):
        if self.parent is not None:
            return self.parent.getRoot()
        return self
    
    def findChildByName(self, name):
        for child in self.getChildren():
            if child.gameObject.name == name:
                return child
        assert False
    
    def findChildByTag(self, tag):
        for child in self.getChildren():
            if tag in child.gameObject.tags:
                return child
        assert False
    
    def findChildrenByTag(self, tag):
        ans = []
        for child in self.getChildren():
            if tag in child.gameObject.tags:
                ans.append(child)
        return ans
    
    def broadcastMessage(self, msg, *args, targetComponent=Component, **kwargs):
        self.gameObject.handleMessage(msg, *args, targetComponent=targetComponent, **kwargs)
        for child in self.getChildren():
            child.broadcastMessage(msg, *args, targetComponent=targetComponent, **kwargs)
    
    def getPosition(self):
        return self.pos  # ?.copy()
    
    def getAbsolutePosition(self):
        if self.parent is None:
            return self.getPosition()
        return self.getPosition() + self.parent.getAbsolutePosition()
    
    def getRelativePosition(self, other):
        return self.getAbsolutePosition() - other.getAbsolutePosition()
    
    def toAbsolute(self, coords):
        return coords + self.getAbsolutePosition()
    
    def fromAbsolute(self, coords):
        return coords - self.getAbsolutePosition()
    
    def toRelative(self, other, coords):
        return coords + self.getRelativePosition(other)
    
    def fromRelative(self, other, coords):
        return coords - self.getRelativePosition(other)


class Behaviour(Component):
    pass


class Texture(Component):
    def __init__(self, gameObject, zIndex=0):
        super().__init__(gameObject)
        self.zIndex = zIndex
    
    def draw(self, drawBuf, color, rect):
        drawBuf.append((color, rect, self.zIndex))


class BoxTexture(Texture):
    def __init__(self, gameObject, size, color, zIndex=0, offset=(0, 0)):
        super().__init__(gameObject, zIndex=zIndex)
        self.offset = Vector2(offset)
        self.color = color
        self.size = size
    
    def getRect(self):
        pos = round(self.gameObject.transform.getAbsolutePosition() + self.offset)
        return pygame.Rect(pos.tuple(), self.size)
    
    def on_draw(self, drawBuf):
        self.draw(drawBuf, self.color, self.getRect())


class Collider(Component):
    @staticmethod
    def collide(first, second):
        assert isinstance(first, Collider)
        assert isinstance(second, Collider)
        res = first._collide(second)
        if res is not NotImplemented:
            return res
        res = second._collide(first)
        if res is not NotImplemented:
            return res
        raise NotImplementedError()


class BoxCollider(Collider):
    def __init__(self, gameObject, size, offset=(0, 0)):
        super().__init__(gameObject)
        self.offset = Vector2(offset)
        self.size = size
    
    def getRect(self):
        pos = round(self.gameObject.transform.getAbsolutePosition() + self.offset)
        return pygame.Rect(pos.tuple(), self.size)
    
    def _collide(self, other):
        if not isinstance(other, BoxCollider):
            return NotImplemented
        return self.getRect().colliderect(other.getRect())


class Scene(GameObject):
    def __init__(self, size=(800, 600), fpsLimit=1000, bgColor=(255, 255, 255)):
        super().__init__("Scene")
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.fpsLimit = fpsLimit
        self.bgColor = bgColor
        self.drawBuf = []
        self.addComponent(Transform)
    
    def handleEvent(self, event):
        tr = self.transform
        if event.type == pygame.QUIT:
            self.stop()
        if event.type == pygame.KEYDOWN:
            tr.broadcastMessage("keydown", event.key, event.mod, event.unicode, event.scancode)
        if event.type == pygame.KEYUP:
            tr.broadcastMessage("keyup", event.key, event.mod)
        pass  # TODO: Implement the rest!!
    
    def run(self):
        tr = self.transform
        tr.broadcastMessage("start")
        while True:
            self.clock.tick(self.fpsLimit)
            #print(self.clock.get_fps())
            self.drawBuf = []
            for event in pygame.event.get():
                self.handleEvent(event)
            tr.broadcastMessage("tick", self)
            self.screen.fill(self.bgColor)
            tr.broadcastMessage("draw", self.drawBuf, targetComponent=Component)
            self.drawAll()
    
    def drawAll(self):
        for color, rect, _ in sorted(self.drawBuf, key=lambda x: x[2]):
            surface = pygame.Surface(rect.size)
            surface.fill(color)
            self.screen.blit(surface, rect)
        pygame.display.update()
    
    def stop(self):
        pygame.quit()
        sys.exit()


isclose = math.isclose