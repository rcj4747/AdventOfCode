from itertools import combinations


# Read the data file as a list of integers
with open('input.txt') as fp:
    data = [int(x) for x in fp.read().split()]

# Skip the 25 integer preamble
ptr = 25
invalid = None
# Iterate though the data to find an number that does not have
# two numbers in the 25 numbers preceeding it whose sum is equal to it
for ptr in range(25, len(data)):
    valid = False
    for x, y in combinations(data[ptr - 25: ptr], r=2):
        if (x + y) == data[ptr]:
            valid = True
            break
    if not valid:
        invalid = data[ptr]
        break

if invalid:
    print(f'Invalid data {data[ptr]} found at offset {ptr}')
else:
    raise RuntimeError('Failed to find invalid data')

# Find a range of 2 or more numbers in the data whose sum is equal
# to the invalid number
found = False
for start in range(0, len(data)):
    for end in range(start + 1, len(data) + 1):
        if sum(data[start:end]) == invalid:
            found = True
            break
    if found:
        break

if found:
    print(f'Found range {start=}, {end=}')
else:
    raise RuntimeError(f'Could not find a range with a sum of {invalid}')

# Find smallest and largest in range
smallest = min(data[start:end])
largest = max(data[start:end])

# Print their sum
print(f'{smallest=} + {largest=} = {smallest+largest}')
