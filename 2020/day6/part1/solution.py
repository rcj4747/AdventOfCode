from typing import Set


total = 0

with open('input.txt') as fp:
    # total = sum([len(set(x.translate({ord('\n'): None})))
    #              for x in fp.read().split('\n\n')])

    # Solution broken out to explain my daughter
    for group in fp.read().split('\n\n'):
        print(f'New group: {group}')
        group_answers: Set[str] = set()
        for person in group.split('\n'):
            print(f'New person: {person}')
            for answer in person:
                print(f'{answer =}')
                group_answers = group_answers.union(answer)
            print()
        print(f'{group_answers =}\n')
        total += len(group_answers)

print(f'{total =}')
