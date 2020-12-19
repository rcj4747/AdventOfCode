

operations = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
}


def process_stack(stack):
    a = int(stack.pop())
    while stack:
        op = stack.pop()
        b = int(stack.pop())
        a = operations[op](a, b)
    return a


def process_input(input_list):
    stack = []
    while True:
        try:
            cur = input_list.pop()
        except IndexError:
            break
        if cur.endswith(')'):
            # Strip off just the trailing ')'
            cur = cur[:-1]

            # Push any remaining characters back on the input
            if cur:
                input_list.append(cur)

            input_list, ans = process_input(input_list)
            stack.append(ans)

        elif cur.startswith('('):
            # Strip off a leading '('
            cur = cur[1:]

            # Put the digit portion on the stack
            stripped = cur.lstrip('(')
            if stripped.isdigit():
                stack.append(stripped)

            # Put any remaining characters back on the input
            cur = cur[:-len(stripped)]
            if cur:
                input_list.append(cur)

            return input_list, process_stack(stack)

        else:
            stack.append(cur)

    return input_list, process_stack(stack)


with open('input.txt') as file:
    part1 = 0
    for line in file.readlines():
        line = line.strip()
        _, answer = process_input(line.split(' '))
        part1 += answer
    print(f'{part1 = }')
