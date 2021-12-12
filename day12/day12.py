from collections import defaultdict

with open('input') as f:
    connections = f.read().split('\n')

connection_map = defaultdict(list)
for c in connections:
    if not c:
        continue
    start, end = c.split('-')
    connection_map[start].append(end)
    if start != 'start' and end != 'end':
        connection_map[end].append(start)

routes = set()
def explore(start, route, can_visit_a_small_cave_twice):
    if start.lower() == start:
        small_caves_visited = [cave for cave in route if cave.lower() == cave]
        if start in route and (
            start == 'start'
            or not can_visit_a_small_cave_twice
            or len(small_caves_visited) != len(set(small_caves_visited))
        ):
            return
    route = tuple([*route, start])
    if start == 'end':
        routes.add(route)
    else:
        for connection in connection_map[start]:
            explore(connection, route, can_visit_a_small_cave_twice) 


explore('start', tuple(), False)
print(len(routes)) 

routes = set()
explore('start', tuple(), True)
print(len(routes))

