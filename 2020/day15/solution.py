import sys
from collections import defaultdict
from typing import Dict


def main():
    try:
        max_count = int(sys.argv[1])
    except IndexError:
        print(f'Usage: {sys.argv[0]} #Iterations')
        quit(1)

    with open('input.txt') as fp:
        numbers: Dict[int, int] = defaultdict(
            int,
            {int(x): int(n)
             for n, x in enumerate(fp.read().split(','), start=1)})

    # print(f'{numbers.items()}')
    counter: int = len(numbers)
    last_num: int = [key for key, value in numbers.items()
                     if value == (counter)][0]

    print(f'Finding number from iterations {max_count}: ', end='')
    while counter < max_count:
        number = numbers[last_num]
        numbers[last_num] = counter
        last_num = 0 if not number else counter - number
        counter += 1
    print(f'{last_num}')


if __name__ == '__main__':
    main()
