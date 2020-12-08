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

PTR = 0
ACC = 0
while True:
    print(f'{PTR=} {ACC=} {OPS[PTR]}')
    if OPS[PTR].visitited:
        raise Exception(f'Loop detected, line {PTR}. {ACC=}')
    if OPS[PTR].opcode == 'nop':
        OPS[PTR].visitited = True
        PTR += 1
        continue
    elif OPS[PTR].opcode == 'acc':
        OPS[PTR].visitited = True
        ACC += OPS[PTR].arg
    elif OPS[PTR].opcode == 'jmp':
        OPS[PTR].visitited = True
        PTR += OPS[PTR].arg
        continue
    PTR += 1
