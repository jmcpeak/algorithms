
# see read me for the graph denoted by this
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


def walkAllEdges(graph):
    for edge in graph:
        print(
            f"Computation starting from edge {edge}; All path will lead to edge {edge}")
        bfsResult = bfs(graph, edge)
        shortesPath = computeShortestPath(edge, bfsResult)
        print(shortesPath)


walkAllEdges(graph)
# output::

# Computation starting from edge a; All path will lead to edge a
# ['0:: a', '1:: s->a', '1:: z->a', '2:: x->s->a', '3:: d->x->s->a', '3:: c->x->s->a', '4:: f->d->x->s->a', '4:: v->c->x->s->a']
# Computation starting from edge s; All path will lead to edge s
# ['0:: s', '1:: a->s', '1:: x->s', '2:: z->a->s', '2:: d->x->s', '2:: c->x->s', '3:: f->d->x->s', '3:: v->c->x->s']
# Computation starting from edge d; All path will lead to edge d
# ['0:: d', '1:: f->d', '1:: x->d', '1:: c->d', '2:: v->f->d', '2:: s->x->d', '3:: a->s->x->d', '4:: z->a->s->x->d']
# Computation starting from edge f; All path will lead to edge f
# ['0:: f', '1:: d->f', '1:: c->f', '1:: v->f', '2:: x->d->f', '3:: s->x->d->f', '4:: a->s->x->d->f', '5:: z->a->s->x->d->f']
# Computation starting from edge z; All path will lead to edge z
# ['0:: z', '1:: a->z', '2:: s->a->z', '3:: x->s->a->z', '4:: d->x->s->a->z', '4:: c->x->s->a->z', '5:: f->d->x->s->a->z', '5:: v->c->x->s->a->z']
# Computation starting from edge x; All path will lead to edge x
# ['0:: x', '1:: s->x', '1:: d->x', '1:: c->x', '2:: a->s->x', '2:: f->d->x', '2:: v->c->x', '3:: z->a->s->x']
# Computation starting from edge c; All path will lead to edge c
# ['0:: c', '1:: d->c', '1:: f->c', '1:: x->c', '1:: v->c', '2:: s->x->c', '3:: a->s->x->c', '4:: z->a->s->x->c']
# Computation starting from edge v; All path will lead to edge v
# ['0:: v', '1:: f->v', '1:: c->v', '2:: d->f->v', '2:: x->c->v', '3:: s->x->c->v', '4:: a->s->x->c->v', '5:: z->a->s->x->c->v']
