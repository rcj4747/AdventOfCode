#!/bin/env python3
import re
from typing import Dict, List
from pprint import pprint

from schema import Schema, And, Const, Use, Optional, SchemaError


PASSPORTS = []

## Field specification
# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.


def read_passport_data(filename: str) -> List[Dict[str, str]]:
    passports = []
    with open(filename, 'r') as fp:
        data: Dict[str, str] = {}
        for line in fp:
            line = line.strip()
            if not line and data:
                passports.append(data)
                data = {}
            else:
                for field in line.split(' '):
                    k, v = field.split(':')
                    data[k] = v
        if data:  # Append last passport if no trailing newline
            passports.append(data)
    return passports


def _validate_fields(passport_dict: Dict[str, str]) -> bool:
    """Validate the passport fields against a schema"""

    def validate_height(height_str: str) -> bool:
        match = re.match(r'(?P<qt>[0-9]+)(?P<units>cm|in)', height_str)
        if not match:
            return False
        height, units = match.groups()
        height = int(height)
        if units == 'cm':
            return 150 <= height <= 193
        elif units == 'in':
            return 59 <= height <= 76
        return False

    eye_colors = ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
    schema = Schema({
        'byr': And(Use(int), lambda x: 1920 <= x <= 2002,
                   error='Birth year (byr) not between 1920 & 2020 inclusive'),
        'iyr': And(Use(int), lambda x: 2010 <= x <= 2020,
                   error='Issue year (iyr) not between 2010 & 2020 inclusive'),
        'eyr': And(Use(int), lambda x: 2020 <= x <= 2030,
                   error='Expiration (eyr) year not between 2020 & 2030 inclusive'),
        'hgt': And(str, validate_height,
                   error='Height (hgt) not in range 150cm-192cm or 59in-76in'),
        'hcl': And(str, lambda x: re.match(r'^#[0-9a-f]{6}', x),
                   error='Hair color (hcl) not hex rgb'),
        'ecl': And(str, lambda x: x in ('amb', 'blu', 'brn', 'gry',
                                        'grn', 'hzl', 'oth'),
                   error=f'Eye color not in {eye_colors}'),
        'pid': And(Const(And(Use(str), lambda x: len(x) == 9)),
                   Use(int),
                   error='Passport ID (pid) not a 9-digit number'),
        Optional('cid'): And(str, error='Optional Country ID (cid) not a string'),
    })

    try:
        schema.validate(passport_dict)
    except SchemaError as se:
        pprint(passport_dict)
        print(f'{se}\n')
        return False

    return True


def validate_passport(passport_dict: Dict[str, str]) -> bool:
    required_fields = set([
        'byr',  # Birth year
        'iyr',  # Issue year
        'eyr',  # Expiration year
        'hgt',  # Height
        'hcl',  # Hair color
        'ecl',  # Eye color
        'pid',  # Passport ID
        ])
    optional_fields = set([
        'cid',  # Country ID
        ])
    all_fields = required_fields | optional_fields

    passport_keys = set(passport_dict.keys())
    if not passport_keys.issubset(all_fields):
        pprint(passport_dict)
        print('Not a subset of all_fields\n')
        return False

    if required_fields - passport_keys:
        pprint(passport_dict)
        print(f'Does not have all required fields, missing {required_fields - passport_keys}\n')
        return False

    return _validate_fields(passport_dict)


PASSPORTS = read_passport_data('input.txt')

VALID_COUNT = 0
for PASSPORT in PASSPORTS:
    if validate_passport(PASSPORT):
        VALID_COUNT += 1

print(f'Found {VALID_COUNT} valid passports')
