import sys

NODES = {}


class Node():
    rules = None

    def __init__(self, number, rules=None):
        self.number = number
        if rules:
            self.add_rules(rules)

    def add_rules(self, rules):
        if rules.startswith('"'):
            self.rules = rules.strip('"')
        else:
            self.rules = []
            for rule in rules.split('|'):
                sub = []
                for node_name in rule.split():
                    node_number = int(node_name)
                    if node_number not in NODES:
                        NODES[node_number] = Node(node_number)
                    sub.append(NODES[node_number])
                self.rules.append(sub)
            if not self.rules:
                raise Exception("Empty rule set for node")

    def __repr__(self):
        return f'<Node:{self.number} : {self.rules}'


def main():
    filename = 'input.txt' if len(sys.argv) < 2 else sys.argv[1]
    with open(filename) as file:
        for line in file:
            if not line.strip():
                break
            try:
                node_name, rules = line.split(':')
            except ValueError:
                print(line)
                quit(1)
            node_number = int(node_name)
            rules = rules.strip()
            if node_number not in NODES:
                NODES[node_number] = Node(node_number)
            NODES[node_number].add_rules(rules)
        print(NODES[0])

        for line in file:
            message = line.strip()
            # print(message)


if __name__ == '__main__':
    main()
