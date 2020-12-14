import sys


def read_file(filename):
    with open(filename) as fp:
        cur_time = int(fp.readline().strip())
        bus_ids = sorted([int(x) for x in fp.readline().strip().split(',')
                          if x != 'x'])
        return cur_time, bus_ids


def main():
    (cur_time, bus_ids) = read_file(
        sys.argv[1]if len(sys.argv) == 2 else 'input.txt')
    print(f'{len(bus_ids) = }')
    print(f'{bus_ids = }')

    next_arrivals = []
    for bus in bus_ids:
        next_arrivals.append(cur_time % bus)
    print(f'{next_arrivals = }')
    soonest = next_arrivals.index(max(next_arrivals))
    print(f'{cur_time // bus_ids[soonest] = }')
    next_id = bus_ids[soonest]
    next_time = ((cur_time // next_id) + 1) * next_id
    answer = next_id * (next_time - cur_time)
    print(f'{next_id = } arrives in {next_time - cur_time = }')
    print(f'Our answer is {answer}')


if __name__ == '__main__':
    main()
