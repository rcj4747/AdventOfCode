import sys
from copy import copy
from functools import lru_cache
from pprint import pformat  # noqa: F401


def read_field_specs(file):
    fields = {}
    while (line := file.readline().strip()):
        # print(line)
        name, range_str = line.split(':')
        ranges = []
        range_str = range_str.strip()
        range_str_start = 0
        while range_str_start <= len(range_str):
            range_str_end = range_str[range_str_start:].find(' or ')
            if range_str_end == -1:
                range_str_end = len(range_str)
            a, b = range_str[range_str_start:range_str_end].split('-')
            ranges.append(tuple([int(a), int(b)]))
            range_str_start = range_str_end + 4
        fields[name] = ranges
    return fields


def read_my_ticket(file):
    header = file.readline().strip()
    if header != "your ticket:":
        raise Exception('Input format error, expected "your ticket:"')

    fields = [int(x) for x in file.readline().strip().split(',')]
    file.readline()  # trailing blank line
    # print(fields)
    return fields


def read_nearby_tickets(file):
    header = file.readline().strip()
    if header != "nearby tickets:":
        raise Exception('Input format error, expected "nearby tickets:"')
    fields = []
    for line in file.readlines():
        fields.append([int(x) for x in line.strip().split(',')])
    return fields


def merge_valid_ranges(field_specs):
    # Create a list of all valid ranges irrespective of field names
    all_ranges = []
    for ranges in field_specs.values():
        all_ranges.extend(ranges)
    all_ranges = sorted(all_ranges, key=lambda x: x[0])

    merged = [list(all_ranges[0])]
    for values in all_ranges[1:]:
        # New range start overlaps with prior range
        if values[0] <= merged[-1][1]:
            # New range extends past end of prior range
            if values[1] > merged[-1][1]:
                # Extend prior range to equal end of new range
                merged[-1][1] = values[1]
        # New range is separate from the prior range
        else:
            merged.append(values)

    return merged


def validate_nearby_tickets(tickets, valid_ranges):
    # Error rate is defined as the sum of invalid fields
    error_rate = 0
    valid_tickets = []
    for ticket in tickets:
        valid = True
        for field in ticket:
            for start, end in valid_ranges:
                if field >= start and field <= end:
                    # Valid, try next range
                    continue
                # Field invalid, add to error rate and move to next field
                error_rate += field
                valid = False
                break
        if valid:
            valid_tickets.append(ticket)
    return error_rate, valid_tickets


def solve_fields(tickets, field_specs):
    # Rotate the tickets to have a list of columns for qualification
    ticket_cols = tuple(zip(*reversed(tickets)))
    field_count = len(field_specs)

    if field_count != len(ticket_cols):
        raise Exception(f'Field count {field_count} does not match '
                        f'column count {len(ticket_cols)}')

    answer = [None] * len(field_specs)

    @lru_cache(maxsize=None)
    def validate_column(column, ranges):
        for data in column:
            valid_data = False
            for valid_range in ranges:
                # print(f'{valid_range}\t{data}')
                if valid_range[0] <= data and data <= valid_range[1]:
                    valid_data = True
                    break
            if not valid_data:
                return False
        return True

    def solve_column(index, field_specs):
        # print(f'solve_column({index}, {field_specs.keys()})')
        for spec in field_specs.items():
            answer[index] = spec[0]
            # print(f'{spec}')
            if validate_column(ticket_cols[index], tuple(spec[1])):
                if index >= field_count - 1:
                    return answer
                less_fields = copy(field_specs)
                del(less_fields[spec[0]])
                # print(f'{field_specs.keys() = }\n{spec = }\n'
                #       f'{less_fields.keys() = }')
                if solve_column(index + 1, less_fields):
                    return answer
        return None

    answer = solve_column(0, field_specs)
    return answer


def read_file(filename):
    with open(filename) as file:
        field_specs = read_field_specs(file)
        my_ticket = read_my_ticket(file)
        tickets = read_nearby_tickets(file)
    return{'field_specs': field_specs,
           'my_ticket': my_ticket,
           'tickets': tickets,
           }


def main():
    data_dict = read_file('input.txt' if len(sys.argv) != 2 else sys.argv[1])

    validity_ranges = merge_valid_ranges(data_dict['field_specs'])
    error_rate, valid_tickets = validate_nearby_tickets(
        data_dict['tickets'], validity_ranges)
    print(f'{error_rate = }\t{len(data_dict["tickets"]) = }\t'
          f'{len(valid_tickets) = }')

    # Determine the order of the fields in the tickets
    valid_tickets.append(data_dict['my_ticket'])
    field_order = solve_fields(valid_tickets, data_dict['field_specs'])
    # print(f'The column order is {pformat(field_order)}')

    # Find the "departure *" fields in my_ticket and return the product
    my_ticket_answer = {}
    for index, field in enumerate(field_order):
        my_ticket_answer[field] = data_dict['my_ticket'][index]
    print(f'My ticket data:\n{pformat(my_ticket_answer)}')

    product = 1
    for field in my_ticket_answer:
        if field.startswith('departure '):
            product = product * my_ticket_answer[field]
    print(f'The product of the departure fields is {product}')


if __name__ == '__main__':
    main()
