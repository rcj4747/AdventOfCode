import sys
from dataclasses import dataclass
from enum import IntEnum
from typing import List


class Heading(IntEnum):
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


@dataclass
class Coordinate():
    x: int
    y: int

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, units: int):
        return Coordinate(self.x * units, self.y * units)

    def manhattan_distance(self, other):
        coord = self - other
        return abs(coord.x) + abs(coord.y)


DIRECTIONS = {
    'N': Coordinate(x=0, y=1),
    'E': Coordinate(x=1, y=0),
    'S': Coordinate(x=0, y=-1),
    'W': Coordinate(x=-1, y=0),
}


Heading_to_Direction = {
    Heading.NORTH: DIRECTIONS['N'],
    Heading.EAST: DIRECTIONS['E'],
    Heading.SOUTH: DIRECTIONS['S'],
    Heading.WEST: DIRECTIONS['W'],
}


@dataclass
class Ship():
    position: Coordinate
    heading: Heading

    def move(self, direction: Coordinate, distance: int):
        self.position = self.position + direction * distance

    def rotate(self, units: int):
        while units < 0:
            units += 360
        self.heading = Heading((self.heading + units) % 360)

    def forward(self, units: int):
        self.move(Heading_to_Direction[self.heading], units)


def read_file(filename):
    with open(filename) as fp:
        return [x.strip() for x in fp.readlines()]


def main():
    commands: List[str] = read_file(
        sys.argv[1]if len(sys.argv) == 2 else 'input.txt')
    print(f'{len(commands) = }')

    # Initial state
    ferry = Ship(position=Coordinate(x=0, y=0), heading=Heading.EAST)
    print(ferry)

    for command in commands:
        move = command[0]
        units = int(command[1:])
        if move in ['R', 'L']:
            if move == 'L':
                units *= -1
            ferry.rotate(units)
        elif move == 'F':
            ferry.forward(units)
        elif move in DIRECTIONS:
            ferry.move(DIRECTIONS[move], units)
        else:
            raise Exception(f'Unknown command {move}')
        print(f'{command = }\t{ferry}')
    print(f'{ferry.position.manhattan_distance(Coordinate(0,0)) = }')


if __name__ == '__main__':
    main()
