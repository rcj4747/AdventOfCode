import sys


def read_file(filename):
    with open(filename) as fp:
        cur_time = int(fp.readline().strip())
        bus_ids = []
        for x in fp.readline().strip().split(','):
            if x == 'x':
                bus_ids.append(None)
            else:
                bus_ids.append(int(x))
        return cur_time, bus_ids


def main():
    global CUR_START
    (_, bus_ids) = read_file(
        # sys.argv[1]if len(sys.argv) == 2 else '2020/day13/part2/test.3417')
        sys.argv[1]if len(sys.argv) == 2 else 'input.txt')
    print(f'{len(bus_ids) = }')
    print(f'{bus_ids = }')
    largest_interval = max([x for x in bus_ids if isinstance(x, int)])
    print(f'{largest_interval = }')
    CUR_START = largest_interval - bus_ids.index(largest_interval)
    cur_time = CUR_START - 1

    while True:
        found = True
        for x in bus_ids:
            cur_time += 1
            if not x:
                continue
            if cur_time % x:
                found = False
                continue
        if found:
            print(f'Found @ {CUR_START}')
            break
        CUR_START += largest_interval
        cur_time = CUR_START - 1
        # print(f'{cur_start = }\t{cur_time = }')


CUR_START = 0

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'{CUR_START=}')
