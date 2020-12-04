import re
from dataclasses import dataclass


@dataclass
class password(object):
    min_len: int
    max_len: int
    val: str
    password: str

    def __init__(self, in_str):
        scheme = r'(?P<min_len>\d+)-(?P<max_len>\d+) (?P<val>[a-z]): ' + \
                 r'(?P<password>[a-z]+)'
        match = re.match(scheme, in_str)
        if not match:
            raise Exception(f'Input "{in_str} did not match format')

        in_str = match.groupdict()
        self.min_len = int(in_str['min_len'])
        self.max_len = int(in_str['max_len'])
        self.val = in_str['val']
        self.password = in_str['password']

    def is_valid(self):
        matches = len(re.findall(f'{self.val}', self.password))

        if matches >= self.min_len and matches <= self.max_len:
            return True
        return False


passwords = []
with open('input.txt', 'r') as fp:
    passwords.extend([password(line) for line in fp])

count = 0
for p in passwords:
    if p.is_valid():
        print(p)
        count += 1

print(f'There were {count} valid passwords')