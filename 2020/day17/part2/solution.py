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

# 2D input to 3D cube with input centered
cube = np.array(input_array, dtype='B')
cube = cube[np.newaxis, :]
cube = np.pad(cube,
              ((1, 1), (1, 1), (1, 1)),
              constant_values=0)
hypercube = cube[np.newaxis, :]
hypercube = np.pad(hypercube,
                   ((1, 1), (0, 0), (0, 0), (0, 0)),
                   constant_values=0)
del(cube)


def process_hypercube(hypercube):
    print(f'Processing hypercube with shape {hypercube.shape}')
    new_hypercube = hypercube.copy()
    for w in range(hypercube.shape[0]):
        minw = max(0, w - 1)
        maxw = min(hypercube.shape[0], w + 2)
        for z in range(hypercube.shape[1]):
            minz = max(0, z - 1)
            maxz = min(hypercube.shape[1], z + 2)
            for y in range(hypercube.shape[2]):
                miny = max(0, y - 1)
                maxy = min(hypercube.shape[2], y + 2)
                for x in range(hypercube.shape[3]):
                    minx = max(0, x - 1)
                    maxx = min(hypercube.shape[3], x + 2)
                    adj_hypercube = hypercube[minw:maxw, minz:maxz,
                                              miny:maxy, minx:maxx]
                    active_count = adj_hypercube.sum()

                    # Remove self from the sum
                    center = hypercube[w, z, y, x]

                    active_count -= center
                    new_hypercube[w, z, y, x] = center
                    if center:
                        if not (active_count == 2 or active_count == 3):
                            new_hypercube[w, z, y, x] = 0
                    elif active_count == 3:
                        new_hypercube[w, z, y, x] = 1
    return new_hypercube


count = 0
iterations = 6
while True:
    hypercube = process_hypercube(hypercube)
    if count == (iterations - 1):
        break
    # In each iteration the array will grow
    hypercube = np.pad(hypercube,
                       ((1, 1), (1, 1), (1, 1), (1, 1)),
                       constant_values=0)
    count += 1

# print(hypercube)
print(int(hypercube.sum()))
