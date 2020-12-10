from typing import List


with open('input.txt') as fp:
    adapters = sorted([int(x) for x in fp.readlines()])

# Insert the 0-jolt jack
adapters.insert(0, 0)

# There's a 3-jolt delta between the last adapter and the device
adapters.append(adapters[-1] + 3)

adapter_groups = []
curr: List[int] = []
# Break the input into groups of adapters separated by 3-jolt gaps
# A 3-jolt gap only allows for a single combination of adapters
for adapter in adapters:
    if not curr or adapter - curr[-1] == 1:
        curr.append(adapter)
    else:
        adapter_groups.append(curr)
        curr = [adapter]
adapter_groups.append(curr)
print(adapter_groups)

total_combinations = 1
# For a run of length x, the number of valid combinations is combinations[x]
# These were found with paper and pencil given that the input has only
# 1&3 jolt deltas, all numbers in an adapter group would be consecutive.
# This lookup table of combinations goes to x=6 although the input only has
# groups as large as 5
combinations = [0, 1, 1, 2, 4, 7, 13]
print('\nGrpLen\tCombinations')
for group in adapter_groups:
    # Find the product of all the combinations
    total_combinations = total_combinations * combinations[len(group)]
    print(f'{combinations[len(group)]}\t{total_combinations}')
print(f'{total_combinations = }')
