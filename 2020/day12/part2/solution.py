import math
import sys
from dataclasses import dataclass
from typing import List


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


@dataclass
class Ship():
    position: Coordinate
    waypoint: Coordinate  # relative to ship

    def move_waypoint(self, direction: Coordinate, distance: int):
        self.waypoint = self.waypoint + direction * distance

    def rotate_waypoint(self, angle: int):
        # print(f'{angle = }')
        rad = math.radians(angle)
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.waypoint.x * cosa - self.waypoint.y * sina
        y = self.waypoint.x * sina + self.waypoint.y * cosa

        # Round negative values to up in absolute terms
        intx = int(math.copysign(round(abs(x)), x))
        inty = int(math.copysign(round(abs(y)), y))

        # print(f'{self.waypoint = }')
        self.waypoint = Coordinate(intx, inty)
        # print(f'{self.waypoint = }')

    def move(self, units: int):
        self.position += self.waypoint * units


def read_file(filename):
    with open(filename) as fp:
        return [x.strip() for x in fp.readlines()]


def main():
    commands: List[str] = read_file(
        sys.argv[1]if len(sys.argv) == 2 else 'input.txt')
    print(f'{len(commands) = }')

    # Initial state
    ferry = Ship(position=Coordinate(x=0, y=0),
                 waypoint=Coordinate(x=10, y=1),
                 )
    print(ferry)

    for command in commands:
        move = command[0]
        units = int(command[1:])
        if move in ['R', 'L']:
            if move == 'R':
                units *= -1
            ferry.rotate_waypoint(units)
        elif move == 'F':
            ferry.move(units)
        elif move in DIRECTIONS:
            ferry.move_waypoint(DIRECTIONS[move], units)
        else:
            raise Exception(f'Unknown command {move}')
        print(f'{command = }\t{ferry}')
    print(f'{ferry.position.manhattan_distance(Coordinate(0,0)) = }')


if __name__ == '__main__':
    main()
