import math


class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
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
        return hypot(self.x, self.y)
    
    def angle(self, other=None):
        if other is None:
            return math.atan2(self.y, self.x)
        assert isinstance(other, Vector2)
        return math.atan2(self @ other, self * other)
    
    @staticmethod
    def fromRPhi(r, phi):
        return Vector2(r * math.cos(phi), r * math.sin(phi))
    
    def toRPhi(self):
        return (abs(self), self.angle())
    
    def copy(self):
        return Vector2(self.x, self.y)
    
    def normalize(self):
        return self / abs(self)
    
    def _rotate(self, sin, cos, rel=None):
        if rel is None:
            return Vector2(self.x * cos - self.y * sin, self.x * sin + self.y * cos)
        return (self - rel)._rotate(sin, cos) + rel
    
    def rotate(self, phi, rel=None):
        return self._rotate(math.sin(phi), math.cos(phi), rel=rel)
    
    def clamp(self, rect, loop=True):
        if loop:
            return Vector2((self.x - rect.x) % rect.width + rect.x, (self.y - rect.y) % rect.height + rect.y)
        return Vector2(max(rect.left, min(self.x, rect.right)), max(rect.top, min(self.y, rect.bottom)))
    
    # ===[ Operators ]===
    
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        raise NotImplementedError()
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return self + -other
        raise NotImplementedError()
    
    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        raise NotImplementedError()
    
    def __matmul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.y, self.y * other.x)
        raise NotImplementedError()
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self * (1 / other)
        raise NotImplementedError()
    
    def __rmul__(self, other):
        if isinstance(other, Vector2):
            return self * other
        if isinstance(other, (int, float)):
            return self * other
        raise NotImplementedError()
    
    def __rmatmul__(self, other):
        if isinstance(other, Vector2):
            return other * self
        if isinstance(other, (int, float)):
            return self * other
        raise NotImplementedError()
    
    def __iadd__(self, other):
        self = self + other
        return self
    
    def __isub__(self, other):
        self = self - other
        return self
    
    def __imul__(self, other):
        self = self * other
        return self
    
    def __imatmul__(self, other):
        self = self @ other
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
            raise NotImplementedError()
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self == other
    
    def __lt__(self, other):
        return self.toRPhi() < other.toRPhi()
    
    def __le__(self, other):
        return self < other or self == other
    
    def __gt__(self, other):
        return other >= self
    
    def __ge__(self, other):
        return other > self