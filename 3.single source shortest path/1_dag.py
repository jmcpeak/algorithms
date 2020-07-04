# read readme

from math import inf, isinf
from json import dumps

graph = {
    'r': {'s': 5, 't': 3},
    's': {'t': 2, 'x': 6},
    't': {'x': 7, 'y': 4, 'z': 2},
    'x': {'y': -1, 'z': 1},
    'y': {'z': -2},
    'z': {}
}


def dfs(adjList):
    parent = {}

    def topoSort():
        sortedItems = []

        def add(item):
            sortedItems.insert(0, item)

        return {
            'add': add,
            'getSortedItems': lambda: sortedItems
        }

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
    topoSorter = topoSort()

    def dfsVisit(edge):
        watch = watchMen['gateTracker'](edge)
        watch['enter']()

        for adj in adjList.get(edge, {}):
            if adj not in parent:
                parent[adj] = edge
                dfsVisit(adj)

        watch['exit']()
        topoSorter['add'](edge)

    for edge in adjList:
        if edge not in parent:
            parent[edge] = None
            dfsVisit(edge)

    return topoSorter['getSortedItems']()


def sp(adjList, source, topoItems):

    def init(src, items):
        state = {}

        def addToState(vertex, d, pi):
            state[vertex] = {
                'd': d,
                'pi': pi
            }

        def initState():
            nonlocal state
            for item in items:
                if(item == src):
                    addToState(item, 0, None)
                else:
                    addToState(item, inf, None)

        def relax(parent, child, weight):
            # the inital value of infinity would be set by initalizer step
            # but you can think of virtual initalization where if a value does not exist yet,
            # assume distance is positive inifinity. Saves init step cycle by doing this!
            childState = state.get(child, {'d': inf, 'pi': None})
            parentDValue = state.get(parent)['d']
            possibleNewValue = parentDValue + weight

            if(possibleNewValue < childState['d']):
                # this is what relaxing means
                addToState(child, possibleNewValue, parent)
                return possibleNewValue

            return parentDValue

        # run init
        initState()

        return {
            'relax': relax,
            'getPaths': lambda: state
        }

    relax = init(source, topoItems)

    for parent in topoItems:
        for adj, weight in adjList.get(parent).items():
            newValue = relax['relax'](parent, adj, weight)
            if(isinf(newValue)):
                # this means parent edge is before source and there is no point in iterating this
                break

    return relax['getPaths']()


def spDAG(adjList, source):
    topoItems = dfs(adjList)
    return sp(adjList, source, topoItems)


def getSPlog(source, path):
    val = {}

    def computeExactPath(source, currentVertex, pathMap):
        fullPath = f"{currentVertex}"
        pi = currentVertex
        while pi:
            vertexVal = pathMap.get(pi)
            pi = vertexVal['pi']
            fullPath = f"{pi} -> {fullPath}" if pi != None else fullPath

        return fullPath

    for vertex in path:
        d = path.get(vertex)['d']
        key = f"{source} -> {vertex} {d}"
        val[key] = computeExactPath(source, vertex, path)
    return val


path = spDAG(graph, 's')
print(f"Shortest Path: {dumps(getSPlog('s', path), indent = 2)}")

# Topologically sorted Items: ['r', 's', 't', 'x', 'y', 'z']
# Shortest Path: {
#   "s -> r inf": "r",
#   "s -> s 0": "s",
#   "s -> t 2": "s -> t",
#   "s -> x 6": "s -> x",
#   "s -> y 5": "s -> x -> y",
#   "s -> z 3": "s -> x -> y -> z"
# }
