# Learning algorithms!

## Breadth First Search

Suppose we want to traverse the graph ![bfsGraph](./images/bfsGraph.jpeg)

### Concept:

1. Suppose we start at the vertex `s`; `(level = 0; parent = none)`
2. Next question to ask is what are the `vertices` that I can reach from S? The answer is `a & x`. Assign them `level = 1 & parent = s`
3. For each of these vertices ask, what are the `vertices` I can reach from each of them? The answer for a is `s & z`; Answer for x is `s, d & c`. From a if you go to s, you are back to step 1 and will be stuck in this cycle forever. So, out of all these vertices that we just found, we only one to pick the ones that we have not seen before, aka only new vertices. So, in this step the list of new vertices we come up with are: `z, d, c`; `level = 2`; `parent for z = a; parent for d & c = x`.
4. Finally from d & c the new vertices are `f & v`. `Level = 3; parent for f = d; parent for v = c`
5. f & v will not result in new nodes and therefore we are done!

### Shortest path: What's the shortest path from f to s?

Well in above steps, we kept track of parent. If you follow the parent pointer from above step, you will reach the node s.

Essentially, you should traverse the graph using BFS approach starting with the node S. Then follow the parent pointers. This will lead you to shortest path. The level value for f tells exactly how many steps is needed to go from f to s!

### Representing graphs in code:

You can use the adjacency dict that we have used below for the graph representation. (Instead of dict, you can use list too!). For every vertex, you will store the items that it is connected to.

```py
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
```

### Show me the code:

[1_bfs.py](./1_bfs.py)

### Tell me more:

https://www.youtube.com/watch?v=s-CYnVz-uh4
