import sys
from collections import defaultdict
from typing import Dict


def read_file(filename):
    with open(filename) as fp:
        lines = [x.strip() for x in fp.readlines()]
        return lines


def main():
    lines = read_file(
        sys.argv[1]if len(sys.argv) == 2 else 'input.txt')
    memory: Dict[int, int] = defaultdict(int)
    mask = 'X' * 36
    for line in lines:
        if line.startswith('mask'):
            mask = line.split('=')[1].strip()
            # print(f'{mask = }')
            continue
        # Handle line "mem[#####] = #######"
        addr = int(line.split('=')[0][4:-2])
        value_int = int(line.split('=')[1].strip())
        value_binstr = f'{value_int:036b}'
        # print(f'{addr = :5}\t{value_int = }\n'
        #       f'{value_binstr = }\n'
        #       f'{mask         = }')
        # print(f'{int(value_binstr, base=2)}')
        new_val = ''
        for idx in range(36):
            # print(f'{idx = :2} ', end='')
            if mask[idx] != 'X':
                new_val = ''.join([new_val, mask[idx]])
                # print(f'mask {mask[idx]} ', end='')
            else:
                new_val = ''.join([new_val, value_binstr[idx]])
                # print(f'val  {value_binstr[idx]} ', end='')
            # print(new_val)
        memory[addr] = str(new_val)
    # print(f'{memory}')

    mem_sum = sum([int(x, base=2) for x in memory.values()])
    print(f'Contents of memory sums to {mem_sum}')


if __name__ == '__main__':
    main()
