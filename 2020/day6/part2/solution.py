from collections import defaultdict

total_yes = 0
with open('input.txt') as fp:
    for group in fp.read().split('\n\n'):
        print(group)
        group_answers = defaultdict(int)
        for person_number, person in enumerate(group.split()):
            for answer in person:
                group_answers[answer] += 1
        all_yes = len([group_answers[x] for x in group_answers
                       if group_answers[x] == person_number + 1])
        print(all_yes)
        print()
        total_yes += all_yes

print(total_yes)
