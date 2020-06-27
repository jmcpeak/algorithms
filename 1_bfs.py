graph = {
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
                    parent[v] = u
                    next.append(v)
        frontier = next
        i += 1

    return {
        'level': level,
        'parent': parent
    }


def computeShortestPath(vertex, bfsResult):
    paths = []
    level = bfsResult.get('level')
    parent = bfsResult.get('parent')

    for v in parent:
        path = v
        prev = parent.get(v)
        while prev:
            path = f"{path}->{prev}"
            prev = parent.get(prev)
        step = level.get(v)
        paths.append(f"{step}:: {path}")

    return paths


bfsResult = bfs(graph, 's')
shortesPath = computeShortestPath('s', bfsResult)
print(shortesPath)
