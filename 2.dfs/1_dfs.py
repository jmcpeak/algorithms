# read the readme first!
# note that we are using Directed graph here but could have done undirected one too. The algoritm works for
# directed and undirected both

graph = {
    'a': ['b', 'd'],
    'b': ['e'],
    'c': ['e', 'f'],
    'd': ['b'],
    'e': ['d'],
    'f': ['f']
}


def dfs(vertices, adjList):
    parent = {}

    def gateKeeper():
        counter = 0
        gate = {}

        def incrementCounter():
            nonlocal counter
            counter = counter + 1
            return counter

        def gateTracker(node):
            gate[node] = {
                'enter': None,
                'exit': None
            }

            def enter():
                gate[node]['enter'] = incrementCounter()

            def exit():
                gate[node]['exit'] = incrementCounter()

            return {
                'enter': enter,
                'exit': exit
            }

        def getGateLog():
            return gate

        return {
            'gateTracker': gateTracker,
            'getGateLog': getGateLog
        }

    watchMen = gateKeeper()

    def dfsVisit(edge):
        watch = watchMen['gateTracker'](edge)
        watch['enter']()

        for adj in adjList.get(edge, []):
            if adj not in parent:
                parent[adj] = edge
                dfsVisit(adj)  # follow this

        watch['exit']()

    for edge in vertices:
        if edge not in parent:
            parent[edge] = None
            dfsVisit(edge)

    return {
        'parent': parent,
        'getEntryExitTime': watchMen['getGateLog']()
    }


def getGateLog(log):
    val = ""
    for edge in log:
        timer = log.get(edge)
        enter = timer['enter']
        exit = timer['exit']
        val = f"{val}{edge}: {enter}/{exit}\n"

    return val


result = dfs(['a', 'b', 'c', 'd', 'e'], graph)
print(f"{getGateLog(result['getEntryExitTime'])}")
print(f"parent: {result['parent']}")

# a: 1/8
# b: 2/7
# e: 3/6
# d: 4/5
# c: 9/12
# f: 10/11

# parent: {'a': None, 'b': 'a', 'e': 'b', 'd': 'e', 'c': None, 'f': 'c'}
