# -*- coding: utf-8 -*-

import pygame
from pygame import *
from mymaps import*
import operator
import math
import random

class Vec2d(object):
    __slots__ = ['x', 'y']

    def __init__(self, x_or_pair, y = None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")

    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)

    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True

    def __nonzero__(self):
        return bool(self.x or self.y)

    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vec2d"
        if isinstance(other, Vec2d):
            return Vec2d(f(self.x, other.x),
                         f(self.y, other.y))
        elif (hasattr(other, "__getitem__")):
            return Vec2d(f(self.x, other[0]),
                         f(self.y, other[1]))
        else:
            return Vec2d(f(self.x, other),
                         f(self.y, other))

    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vec2d"
        if (hasattr(other, "__getitem__")):
            return Vec2d(f(other[0], self.x),
                         f(other[1], self.y))
        else:
            return Vec2d(f(other, self.x),
                         f(other, self.y))

    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self

    # Addition
    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)
    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vec2d):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self

    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            return Vec2d(self.x - other, self.y - other)
    def __rsub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(other.x - self.x, other.y - self.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2d(other - self.x, other - self.y)
    def __isub__(self, other):
        if isinstance(other, Vec2d):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self

    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x*other.x, self.y*other.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(self.x*other[0], self.y*other[1])
        else:
            return Vec2d(self.x*other, self.y*other)
    __rmul__ = __mul__

    def __imul__(self, other):
        if isinstance(other, Vec2d):
            self.x *= other.x
            self.y *= other.y
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self

    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        return self._io(other, operator.div)

    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)

    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)

    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)

    def __divmod__(self, other):
        return self._o2(other, operator.divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)

    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)

    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)

    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)

    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__

    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__

    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__

    # Unary operations
    def __neg__(self):
        return Vec2d(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self):
        return Vec2d(operator.pos(self.x), operator.pos(self.y))

    def __abs__(self):
        return Vec2d(abs(self.x), abs(self.y))

    def __invert__(self):
        return Vec2d(-self.x, -self.y)

    # vectory functions
    def get_length_sqrd(self):
        return self.x**2 + self.y**2

    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)
    def __setlength(self, value):
        length = self.get_length()
        self.x *= value/length
        self.y *= value/length
    length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")

    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y

    def rotated(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vec2d(x, y)

    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))
    def __setangle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, None, "gets or sets the angle of a vector")

    def get_angle_between(self, other):
        cross = self.x*other[1] - self.y*other[0]
        dot = self.x*other[0] + self.y*other[1]
        return math.degrees(math.atan2(cross, dot))

    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return Vec2d(self)

    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length

    def perpendicular(self):
        return Vec2d(-self.y, self.x)

    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return Vec2d(-self.y/length, self.x/length)
        return Vec2d(self)

    def dot(self, other):
        return float(self.x*other[0] + self.y*other[1])

    def get_distance(self, other):
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)

    def get_dist_sqrd(self, other):
        return (self.x - other[0])**2 + (self.y - other[1])**2

    def projection(self, other):
        other_length_sqrd = other[0]*other[0] + other[1]*other[1]
        projected_length_times_other_length = self.dot(other)
        return other*(projected_length_times_other_length/other_length_sqrd)

    def cross(self, other):
        return self.x*other[1] - self.y*other[0]

    def interpolate_to(self, other, range):
        return Vec2d(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range)

    def convert_to_basis(self, x_vector, y_vector):
        return Vec2d(self.dot(x_vector)/x_vector.get_length_sqrd(), self.dot(y_vector)/y_vector.get_length_sqrd())

    def __getstate__(self):
        return [self.x, self.y]

    def __setstate__(self, dict):
        self.x, self.y = dict

class Gene():
    def __init__(self, marker, unfold):
        self.marker = marker
        self.unfold = unfold


class Turtle():
    def __init__(self, position, heading):
        self.position = position
        self.heading = heading
        self._position_stack = []
        self._heading_stack = []

    def memorise_heading(self):
        self._heading_stack.append(Vec2d(self.heading))

    def memorise_position(self):
        self._position_stack.append(Vec2d(self.position))

    def memorise_position_and_heading(self):
        self._position_stack.append(Vec2d(self.position))
        self._heading_stack.append(Vec2d(self.heading))

    def last_position(self):
        self.position = self._position_stack[-1]
        del self._position_stack[-1]

    def last_heading(self):
        self.heading = self._heading_stack[-1]
        del self._heading_stack[-1]

    def last_position_and_heading(self):
        self.position = self._position_stack[-1]
        del self._position_stack[-1]
        self.heading = self._heading_stack[-1]
        del self._heading_stack[-1]


class LSystem():
    def __init__(self, iterations, dna):
        self.iterations = iterations
        self.dna = dna
        self.chromozomes = []
        self.unfolded = []

    def append_gene(self, gene):
        self.chromozomes.append(gene)

    def unfold(self):
        self.unfolded.append(self.dna)
        for iteration in range(0, self.iterations):
            self.unfolded.append(self.unfolded[-1])
            for c in self.chromozomes:
                self.unfolded[-1] = self.unfolded[-1].replace(c.marker, c.unfold)

    def buildmap(self, sizex, sizey):
        l_map = []
        for x in range(0, sizex):
            l_map.append(list(""))
            for y in range(0, sizey):
                l_map[x] += 'E'
        self.unfold()
        self.interpret(l_map)
        return l_map

    def interpret(self, l_map):
        turtle = Turtle(Vec2d(len(l_map)/4, len(l_map[0])/4), Vec2d(1, 0))
        for p in self.unfolded[-1]:
            l_map[min(max(int(turtle.position.x), 0), len(l_map)-1)][min(max(int(turtle.position.y), 0), len(l_map)-1)] = p
            if p == '>':
                turtle.heading.rotate(90)
            elif p == '<':
                turtle.heading.rotate(-90)
            elif p == '[':
                turtle.memorise_position()
            elif p == ']':
                turtle.last_position()
            elif p == '(':
                turtle.memorise_heading()
            elif p == ')':
                turtle.last_heading()
            elif p == '{':
                turtle.memorise_position_and_heading()
            elif p == '}':
                turtle.last_position_and_heading()
            else:
                turtle.position += turtle.heading


class LSystemMap(WorldMap):
    def __init__(self):
        l = list("BGTSBTABMM")
        random.shuffle(l)
        result = ''.join(l)
        self.Lsystem = LSystem(3, result)
        self.Lsystem .append_gene(Gene("T", "B<MTBE"))
        self.Lsystem .append_gene(Gene("E", "B[TB]T"))
        self.Lsystem .append_gene(Gene("M", "(T<MLB)"))
        self.Lsystem .append_gene(Gene("S", "BT>MB<S"))
        self.Lsystem .append_gene(Gene("L", "MMLR"))
        self.Lsystem .append_gene(Gene("MM", "BMCMB"))
        self.MAZE = self.Lsystem .buildmap(6,6)
        WorldMap.__init__(self, 'worldtest/LSystem.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(y_offset=+8, map_id=2), RectangleArea((4, 0), (5, 0)))
        x = 1
        for line in self.MAZE:
            x += 1
            y = 1
            print(line)
            for char in line:
                y += 1
                if char == 'S':
                    self.add_object(SpecialBoulder(self), Position(x, y))
                elif char == 'B':
                    self.add_object(MazeBoulder(self), Position(x, y))
                elif char == 'M':
                    self.add_object(CrazyMonster(self, hero), Position(x, y))
                elif char == 'C':
                    self.add_object(HealChest(hero), Position(x, y))
                elif char == 'R':
                    self.add_object(ExplosiveBarrel(self,hero), Position(x, y))
                elif char == 'L':
                    self.add_object(MazeLog(self), Position(x, y))

        hero.update_position(self.objects[PARTY].position)
        hero.ref(self.objects[PARTY])
        print(hero.position)

    def find(self, keycharacter):
        value = 0
        if keycharacter in self.ObjectMap:
            value = self.ObjectMap[keycharacter]
        return value



class LSystemMap2(WorldMap):
    def __init__(self):
        l = list("BGTEBMM")
        random.shuffle(l)
        result = ''.join(l)
        self.Lsystem = LSystem(3, result)
        self.Lsystem .append_gene(Gene("T", "B<MTBE"))
        self.Lsystem .append_gene(Gene("E", "B[TB]T"))
        self.Lsystem .append_gene(Gene("M", "(T<MLB)L"))
        self.Lsystem .append_gene(Gene("S", "BT>MB<S"))
        self.Lsystem .append_gene(Gene("L", "MMLR"))
        self.Lsystem .append_gene(Gene("MM", "BMCMB"))
        self.MAZE = self.Lsystem .buildmap(6,6)
        WorldMap.__init__(self, 'worldtest/LSystem2.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(x_offset=+8, map_id=2), RectangleArea((0, 2), (0, 7)))
        self.add_area(RelativeTeleportArea(x_offset=-8, map_id=3), RectangleArea((9, 2), (9, 7)))
        x = 1
        for line in self.MAZE:
            x += 1
            y = 1
            print(line)
            for char in line:
                y += 1
                if char == 'S':
                    self.add_object(SpecialBoulder(self), Position(x, y))
                elif char == 'B':
                    self.add_object(MazeBoulder(self), Position(x, y))
                elif char == 'M':
                    self.add_object(CrazyMonster(self, hero), Position(x, y))
                elif char == 'C':
                    self.add_object(HealChest(hero), Position(x, y))
                elif char == 'R':
                    self.add_object(ExplosiveBarrel(self,hero), Position(x, y))
                elif char == 'L':
                    self.add_object(MazeLog(self), Position(x, y))

        hero.update_position(self.objects[PARTY].position)
        hero.ref(self.objects[PARTY])
        print(hero.position)

    def find(self, keycharacter):
        value = 0
        if keycharacter in self.ObjectMap:
            value = self.ObjectMap[keycharacter]
        return value