#!/bin/env python3

ANSWER = 0


def tree_or_snow(terrain: str):
    if len(terrain) != 1:
        raise Exception('Did not receive a single char in tree_or_snow')
    if terrain not in ['.', '#']:
        raise Exception('Character was neither a tree or snow')

    if terrain == '#':
        return 1
    return 0


SLOPE = []
with open('input.txt', 'r') as fp:
    SLOPE.extend([line.strip() for line in fp])
SLOPE_WIDTH = len(SLOPE[0])


def traverse_slope(across, down=1):
    cur_down = down - 1
    position = 0
    trees = 0
    for line in SLOPE:
        cur_down += 1
        # print(f'Line: {line}\nPosition: {position}\n'
        #       f'Char: {line[position]}\nCur_down: {cur_down}\n')
        if cur_down == down:
            cur_down = 0
        else:
            continue

        trees += tree_or_snow(line[position])
        position += across
        position = position % SLOPE_WIDTH
    return trees


# Determine the number of trees you would encounter if, for each of the
# following slopes, you start at the top-left corner and traverse the map
# all the way to the bottom:

# Right 1, down 1.
# Right 3, down 1. (This is the slope you already checked.)
# Right 5, down 1.
# Right 7, down 1.
# Right 1, down 2.

# In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s)
# respectively; multiplied together, these produce the answer 336.
ATTEMPTS = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
ANSWER = 1
for ACROSS, DOWN in ATTEMPTS:
    T = traverse_slope(across=ACROSS, down=DOWN)
    print(f'Encounter {T} trees while travelling {ACROSS} across, {DOWN} down')
    ANSWER = ANSWER * T

print(f'The answer is {ANSWER}')
