total = 0

with open('input.txt') as fp:
    total = sum([len(set(x.translate({ord('\n'): None})))
                 for x in fp.read().split('\n\n')])
print(total)
