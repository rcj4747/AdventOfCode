#!/bin/env python3

TREES = 0


def count_trees(tree_or_snow: str):
    global TREES

    if len(tree_or_snow) != 1:
        raise Exception('Did not receive a single char in count_trees')
    if tree_or_snow not in ['.', '#']:
        raise Exception('Character was neither a tree or snow')

    if tree_or_snow == '#':
        TREES += 1


slope = []
with open('input.txt', 'r') as fp:
    slope.extend([line.strip() for line in fp])

slope_width = len(slope[0])
offset = 3  # for each line we go over 3
position = 0

for line in slope:
    print(f'Line: {line}\nPosition: {position}\nChar: {line[position]}\n')
    count_trees(line[position])
    position += offset
    position = position % slope_width

print(f'You encountered {TREES} trees.')
