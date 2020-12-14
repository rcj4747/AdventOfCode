import sys
from collections import defaultdict
from itertools import product
from typing import DefaultDict, List


def read_file(filename: str) -> List[str]:
    with open(filename) as fp:
        lines = [x.strip() for x in fp.readlines()]
        return lines


def compute_masks(mask_in: str, address: str) -> List[int]:
    """Create a list of addresses from an input mask and input address

    Each bit in the mask affects the address mask in the following way:
      0 - Address bit unchanged
      1 - Address bit set to 1
      X - Address bit either 0 or 1 (resulting in multiple addresses)
    The list of addresses returned represents all possible combinations.
    """
    x_count = mask_in.count('X')
    addresses_out: List[int] = []
    for prod in product(['0', '1'], repeat=x_count):
        new_address = []
        prod_idx = 0
        for index in range(len(mask_in)):
            mask_chr = mask_in[index]
            if mask_chr == 'X':
                addr_chr = prod[prod_idx]
                prod_idx += 1
            elif mask_chr == '1':
                addr_chr = '1'
            elif mask_chr == '0':
                addr_chr = address[index]

            new_address.append(addr_chr)
        new_addr_str = ''.join(new_address)
        addresses_out.append(int(new_addr_str, base=2))
    return addresses_out


def memory_set(address: int, value: int,
               mask: str,
               memory: DefaultDict[int, int]
               ) -> DefaultDict:
    address_binstr = f'{address:036b}'

    for addr in compute_masks(mask, address_binstr):
        memory[addr] = value
    return memory


def main() -> None:
    lines = read_file(
        sys.argv[1]if len(sys.argv) == 2 else 'input.txt')
    memory: DefaultDict[int, int] = defaultdict(int)
    mask: str = '0' * 36
    for line in lines:
        # Handle "mask = #########"
        if line.startswith('mask'):
            mask = line.split('=')[1].strip()
            continue

        # Handle line "mem[#####] = #######"
        addr_int = int(line.split('=')[0][4:-2])
        value_int = int(line.split('=')[1].strip())
        memory = memory_set(addr_int, value_int, mask, memory)

    mem_sum = sum([x for x in memory.values()])
    print(f'Contents of memory sums to {mem_sum}')


if __name__ == '__main__':
    main()
