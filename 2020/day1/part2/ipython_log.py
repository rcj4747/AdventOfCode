from itertools import combinations

input = []
with open('input.txt', 'r') as fp:
    input.extend([int(line.rstrip()) for line in fp])

found = False


for x, y, z in (combinations(input, 3)):
    if x + y + z == 2020:
        found = True
        break

if not found:
    print('No solution found')
    quit(1)

print(f'Solution is {x} * {y} * {z} = {x * y * z}')
# Solution is 1030 * 268 * 722 = 199300880