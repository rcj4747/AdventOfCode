with open('input.txt') as fp:
    adapters = sorted([int(x) for x in fp.readlines()])

print(adapters)

# There's a 3-jolt delta between the last adapter and the device
adapters.append(adapters[-1] + 3)

delta = [0, 0, 0, 0]
joltage = 0
for adapter in adapters:
    delta[adapter - joltage] += 1
    joltage = adapter

print(f'Joltage differences and their counts {list(enumerate(delta))}')
print(f'Product of 1-jolt & 3-jolt deltas = {delta[1] * delta[3]=}')
