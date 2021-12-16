from collections import defaultdict


with open('input') as f:
    cave = [[int(col) for col in row] for row in f.read().split('\n') if row]

def explore(cave):
    def get_risk_to_node(node):
        if node in risk_to_node:
            return risk_to_node[node]
        return float('inf') 


    def get_risk_estimate(node):
        return len(cave) - node[0] + len(cave[0]) - node[1]


    def get_neighbour(current, delta):
        x = current[0] + delta[0]
        y = current[1] + delta[1]
        if x < 0 or y < 0 or x >= len(cave) or y >= len(cave[0]):
            return
        return x, y


    def get_lowest_risk_node():
        min_risk = float('inf')
        min_node = None
        for node in nodes_to_investigate:
            risk = risk_through_node[node]
            if risk < min_risk:
                min_risk = risk
                min_node = node
        return min_node

 
    risk_to_node = {(0, 0): 0}
    risk_through_node = {(0, 0): get_risk_estimate((0, 0))}
    nodes_to_investigate = set([(0, 0)])

    while len(nodes_to_investigate):
        best_node = get_lowest_risk_node()
        if best_node == (len(cave) - 1, len(cave[0]) - 1):
            return risk_to_node[best_node]
        nodes_to_investigate.remove(best_node)
        for neighbour_delta in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            neighbour = get_neighbour(best_node, neighbour_delta)
            if not neighbour:
                continue
            risk_to_neighbour = risk_to_node[best_node] + cave[neighbour[0]][neighbour[1]]
            if risk_to_neighbour < get_risk_to_node(neighbour):
                risk_to_node[neighbour] = risk_to_neighbour
                risk_through_node[neighbour] = risk_to_neighbour + get_risk_estimate(neighbour)
                nodes_to_investigate.add(neighbour)

print(explore(cave))

big_cave = []
for i in range(5):
    for row in cave:
        big_cave.append([])
    for j in range(5):
        for r, row in enumerate(cave):
            for col in row:
                big_cave[i * len(cave) + r].append((col - 1 + i + j) % 9 + 1)

print(explore(big_cave))

