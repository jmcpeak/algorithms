graphs = {
    'a': ['s', 'z'],
    's': ['a', 'x'],
    'd': ['f', 'x', 'c'],
    'f': ['d', 'c', 'v'],
    'z': ['a'],
    'x': ['s', 'd', 'c'],
    'c': ['d', 'f', 'x', 'v'],
    'v': ['f', 'c']
}


def bfs(adj, s):
    level = {s: 0}
    parent = {s: None}

    i = 1
    frontier = [s]

    while frontier:
        next = []
        for u in frontier:
            for v in adj.get(u):
                if level.get(v) == None:
                    level[v] = i
                    parent[v] = s
                    next.append(v)
        frontier = next
        i += 1

    print(level)


bfs(graphs, 's')
