import numpy as np


def translate_input(instr):
    out = []
    for x in instr:
        out.append(1 if x == '#' else 0)
    return out


input_array = []
# with open('test.txt') as file:
with open('input.txt') as file:
    for line in file.readlines():
        input_array.append(translate_input(line.strip()))

# 2D input
cube = np.array(input_array, dtype='B')
cube = cube[np.newaxis, :]
cube = np.pad(cube,
              ((1, 1), (1, 1), (1, 1)),
              constant_values=0)
# print(cube)


def process_cube(cube):
    print(f'Processing cube with shape {cube.shape}')
    new_cube = cube.copy()
    for z in range(cube.shape[0]):
        minz = max(0, z - 1)
        maxz = min(cube.shape[0], z + 2)
        for y in range(cube.shape[1]):
            miny = max(0, y - 1)
            maxy = min(cube.shape[1], y + 2)
            for x in range(cube.shape[2]):
                minx = max(0, x - 1)
                maxx = min(cube.shape[2], x + 2)
                # print(f'[{minz}:{maxz}, {miny}:{maxy}, {minx}:{maxx}]')
                adj_cube = cube[minz:maxz, miny:maxy, minx:maxx]
                # print(adj_cube)
                # print()
                active_count = adj_cube.sum()

                # Remove self from the sum
                center = cube[z, y, x]

                active_count -= center
                new_cube[z, y, x] = center
                if center:
                    if not (active_count == 2 or active_count == 3):
                        new_cube[z, y, x] = 0
                elif active_count == 3:
                    new_cube[z, y, x] = 1
    return new_cube


count = 0
iterations = 6
while True:
    cube = process_cube(cube)
    if count == (iterations - 1):
        break
    # In each iteration the array will grow
    cube = np.pad(cube, ((1, 1), (1, 1), (1, 1)), constant_values=0)
    count += 1

# print(cube)
print(int(cube.sum()))
