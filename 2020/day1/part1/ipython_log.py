input = []
with open('input.txt', 'r') as fp:
    input.extend([int(line.rstrip()) for line in fp])

found = False
for index1 in range(0, len(input)):
    for index2 in range(index1 + 1, len(input)):
        if input[index1] + input[index2] == 2020:
            found = True
            break
    if found:
        break

if not found:
    print("Nothing found")
    quit(1)

print(f'Matching nubmers were: {input[index1]}, {input[index2]}')
print(f'Their sum is {input[index1] * input[index2]}')
