import re
from dataclasses import dataclass


@dataclass
class password(object):
    pos1: int
    pos2: int
    val: str
    password: str

    def __init__(self, in_str):
        scheme = r'(?P<pos1>\d+)-(?P<pos2>\d+) (?P<val>[a-z]): ' + \
                 r'(?P<password>[a-z]+)'
        match = re.match(scheme, in_str)
        if not match:
            raise Exception(f'Input "{in_str} did not match format')

        in_str = match.groupdict()
        self.pos1 = int(in_str['pos1'])
        self.pos2 = int(in_str['pos2'])
        self.val = in_str['val']
        self.password = in_str['password']

    def is_valid(self):
        matches = re.finditer(f'{self.val}', self.password)

        found = False

        for match in matches:
            if match.end() == self.pos1 or match.end() == self.pos2:
                if found:
                    # pos1 XOR pos2, not pos1 OR pos2
                    return False
                found = True

        return found


# passwords = [password('6-7 m: mlmrrmm')]

passwords = []
with open('input.txt', 'r') as fp:
    passwords.extend([password(line) for line in fp])

count = 0
for p in passwords:
    if p.is_valid():
        print(p)
        count += 1

print(f'There were {count} valid passwords')