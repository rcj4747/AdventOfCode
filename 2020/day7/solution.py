import networkx as nx

G = nx.DiGraph()

with open('input.txt') as fp:
    for line in fp.readlines():
        # Input is in the format:
        # $outer_color bags contain $inner_number1 $inner_color1 bag(s)[, $inner_number# $inner_color# bag(s)]+\.  # noqa:
        line = line.strip()
        # print(f'{line=}')
        outer_split = line.index('contain')
        outer_color = line[:outer_split].strip().rsplit(' ', maxsplit=1)[0]
        # print(f'{outer_color=}')
        G.add_node(outer_color, visited=False)
        inner_line = line[outer_split:].rstrip('.').split(' ', maxsplit=1)[1]
        if inner_line.startswith('no other'):
            # print(f'{outer_color} is a terminal node')
            continue
        for inner in inner_line.split(','):
            inner = inner.strip()
            inner = inner.rsplit(' ', maxsplit=1)[0]  # Strip off 'bag(s)'
            inner_number, inner_color = inner.split(' ', maxsplit=1)
            # print(f'{inner_number=} {inner_color=}')
            G.add_node(inner_color, visited=False)
            G.add_edge(outer_color, inner_color,
                       weight=int(inner_number),
                       relationship='contains')

print(f'Our graph has {len(G.nodes())} nodes (bag colors)')
target = 'shiny gold'


def visit_predecessors(inner):
    for outer in G.predecessors(inner):
        if G.nodes[outer]['visited']:
            continue
        visit_predecessors(outer)
        G.nodes[outer]['visited'] = True


visit_predecessors(target)
print(f'{len([n for n, d in G.nodes.items() if d["visited"]])} bags could '
      f'contain a {target} bag')


def count_bags(outer):
    bags = 1
    for inner in G.successors(outer):
        multiple = G[outer][inner]['weight']
        bags += count_bags(inner) * multiple
    return bags


# Count all the bags
total_bags = count_bags(target)
# Remove the outermost bag from the count
total_bags -= 1
print(f'{total_bags} are required to fit inside your {target} bag')
