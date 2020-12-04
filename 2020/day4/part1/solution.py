#!/bin/env python3
from typing import Dict, List
from pprint import pprint

PASSPORTS = []


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

    pprint(passport_dict)
    passport_keys = set(passport_dict.keys())
    if not passport_keys.issubset(all_fields):
        print('Not a subset of all_fields')
        return False

    if required_fields - passport_keys:
        print(f'Does not have all required fields, missing {required_fields - passport_keys}')
        return False

    print('Valid')
    return True


PASSPORTS = read_passport_data('input.txt')
# pprint(PASSPORTS)

VALID_COUNT = 0
for PASSPORT in PASSPORTS:
    if validate_passport(PASSPORT):
        VALID_COUNT += 1

print(f'Found {VALID_COUNT} valid passports')
