import copy
from dataclasses import dataclass


@dataclass
class Op():
    opcode: str
    arg: int
    visitited: bool


OPS = []
with open('input.txt') as fp:
    for line in fp.readlines():
        op, arg = line.strip().split()
        OPS.append(Op(op, int(arg), False))


def find_jmpnop_ops(ops):
    locations = []
    for loc, op in enumerate(ops):
        if op.opcode == 'jmp' or op.opcode == 'nop':
            locations.append(loc)
    return locations


def alter_ops(ops, loc):
    new_ops = copy.deepcopy(ops)
    op = new_ops[loc]
    if op.opcode == 'jmp':
        op.opcode = 'nop'
    elif op.opcode == 'nop':
        op.opcode = 'jmp'
    else:
        raise RuntimeError(f'Unexpected opcode {op.opcode}')
    return new_ops


def run_program(ops):
    ptr = 0
    acc = 0
    ops_end = len(ops)
    while True:
        if ptr == ops_end:
            print('Successful execution')
            break
        if ptr > ops_end:
            raise IndexError('Jump past end of code {PTR=} {len(OPS)=}')
        # print(f'{ptr=} {acc=} {ops[ptr]}')
        if ops[ptr].visitited:
            raise RuntimeError(f'Loop detected, line {ptr}. {acc=}')
        if ops[ptr].opcode == 'nop':
            ops[ptr].visitited = True
            ptr += 1
            continue
        elif ops[ptr].opcode == 'acc':
            ops[ptr].visitited = True
            acc += ops[ptr].arg
        elif ops[ptr].opcode == 'jmp':
            ops[ptr].visitited = True
            ptr += ops[ptr].arg
            continue
        ptr += 1
    return acc


acc = None
LOCS = find_jmpnop_ops(OPS)
print(f'{len(LOCS)} permutations to test')
for ATTEMPT_NUM, LOC in enumerate(LOCS):
    print(f'Attempting permutation {ATTEMPT_NUM}')
    NEW_OPS = alter_ops(OPS, LOC)
    try:
        acc = run_program(NEW_OPS)
    except IndexError as exc:
        print(f'{exc}\n')
        continue
    except RuntimeError as exc:
        print(f'{exc}\n')
        continue
    print(f'{LOC=} {acc=}')
    break
