# priority.py

"""
Nice data wrappers and enums.
"""

from enum import IntEnum

class DefaultPriority(IntEnum):
    win = 0
    block = 1
    center = 2
    corner = 3
    side = 4

class Status(IntEnum):
    win = 0
    tie = 1
    ongoing = 2


from collections import namedtuple
Coords = namedtuple("Coords", "row col num")


class Cell:

    def __init__(self):
        self.display = "_"
        self.type = 0
        self.coords = 0

    def __str__(self):
        return self.display

    def __repr__(self):
        return self.__str__()


class Priority:

    def __init__(self, num, cell):
        self.num = num
        self.cell = cell

    def __str__(self):
        return str(self.num) + " " + self.cell.__str__() + " " + str(self.cell.coords) + "\n"

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        return self.num > other.num
