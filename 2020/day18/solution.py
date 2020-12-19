

operations = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
}


def push_number(stack, a):
    # In Part 2 the +, - have higher precedence than * so we will
    # process them as soon as we have 2 numbers to operate on.
    if PART2 and stack and stack[-1] in ['+', '-']:
        op = stack.pop()
        b = stack.pop()
        stack.append(process_stack([b, op, a]))
    else:
        stack.append(a)
    return stack


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
            stack = push_number(stack, ans)

        elif cur.startswith('('):
            # Strip off a leading '('
            cur = cur[1:]

            # Put the digit portion on the stack
            stripped = cur.lstrip('(')
            if stripped.isdigit():
                stack = push_number(stack, stripped)

            # Put any remaining characters back on the input
            cur = cur[:-len(stripped)]
            if cur:
                input_list.append(cur)

            return input_list, process_stack(stack)

        else:
            stack = push_number(stack, cur)

    return input_list, process_stack(stack)


for PART2 in False, True:
    with open('input.txt') as file:
        answer = 0
        for line in file.readlines():
            line = line.strip()
            _, line_answer = process_input(line.split(' '))
            answer += line_answer
        print(f'{"Part 1:" if not PART2 else "Part 2:"} {answer}')
