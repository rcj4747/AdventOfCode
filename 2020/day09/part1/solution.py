from itertools import combinations


with open('input.txt') as fp:
    data = [int(x) for x in fp.read().split()]

ptr = 25
for ptr in range(25, len(data)):
    valid = False
    for x, y in combinations(data[ptr - 25: ptr], r=2):
        if (x + y) == data[ptr]:
            valid = True
            break
    if not valid:
        print(f'Invalid data {data[ptr]} found at offset {ptr}')
        break
