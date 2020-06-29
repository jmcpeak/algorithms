# read the readme first!
# note that we are using Directed graph here but could have done undirected one too. The algoritm works for
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

    def classifyEdge():
        forestNumber = 0
        edgesBeingExplored = {}
        edgeBelongsToForest = {}
        isCyclic = False  # only for Directed graphs
        classification = {
            'tree': [],
            'back': [],
            'forward': [],
            'cross': []
        }

        def nodesArePartOfSameForest(u, v):
            uForest = edgeBelongsToForest.get(u)
            vForest = edgeBelongsToForest.get(v)
            return uForest == vForest

        def classifyAs(edge, parent, adj):
            classification[edge].append(f"{parent}->{adj}")

        def classifyAsTree(parent, adj):
            classifyAs('tree', parent, adj)

        def classifyAsBack(parent, adj):
            nonlocal isCyclic
            isCyclic = True  # back edge <=> cyclic graph for directed graphs
            classifyAs('back', parent, adj)

        def classifyAsForward(parent, adj):
            classifyAs('forward', parent, adj)

        def classifyAsCrossEdge(parent, adj):
            classifyAs('cross', parent, adj)

        def classify(parent, adj):
            if adj not in edgesBeingExplored:
                # new adj edge found from parent through adj
                classifyAsTree(parent, adj)
            elif (edgesBeingExplored[parent] & edgesBeingExplored[adj]):
                # both edges are being explored; One edge being explored led to edge that is still being explored. This is back edge
                classifyAsBack(parent, adj)
            elif(edgesBeingExplored[parent] & edgesBeingExplored[adj] == False):
                # parent is being explored but its child is done
                # either forward or cross edge depending on which forest they belong to
                if(nodesArePartOfSameForest(parent, adj)):
                    classifyAsForward(parent, adj)
                else:
                    classifyAsCrossEdge(parent, adj)
            else:
                raise Exception(
                    f"Failed classification for the edge {parent} - {adj} ")

        def markEdgeAsExploring(edge):
            edgesBeingExplored[edge] = True
            edgeBelongsToForest[edge] = forestNumber

        def updateEdgeAsExplored(edge):
            edgesBeingExplored[edge] = False

        def incrementForest():
            nonlocal forestNumber
            forestNumber = forestNumber + 1

        return {
            'classify': classify,
            'markEdgeAsExploring': markEdgeAsExploring,
            'updateEdgeAsExplored': updateEdgeAsExplored,
            'incrementForest': incrementForest,
            'getEdgeClassification': lambda: classification,
            'getTotalForest': lambda: forestNumber,
            'isCyclic': lambda: isCyclic
        }

    watchMen = gateKeeper()
    classifier = classifyEdge()

    def dfsVisit(edge):
        watch = watchMen['gateTracker'](edge)
        watch['enter']()
        #
        classifier['markEdgeAsExploring'](edge)

        for adj in adjList.get(edge):
            if adj not in parent:
                parent[adj] = edge
                classifier['classify'](edge, adj)
                dfsVisit(adj)  # follow this edge
            else:
                classifier['classify'](edge, adj)

        watch['exit']()
        classifier['updateEdgeAsExplored'](edge)

    for edge in vertices:
        if edge not in parent:
            classifier['incrementForest']()  # only time forest is discovered
            parent[edge] = None
            dfsVisit(edge)

    return {
        'parent': parent,
        'getEntryExitTime': watchMen['getGateLog'],
        'getEdgeClassification': classifier['getEdgeClassification'],
        'getTotalForest': classifier['getTotalForest']
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
print(f"{getGateLog(result['getEntryExitTime']())}")
print(f"Parent: {result['parent']}")
print(f"Edges: {result['getEdgeClassification']()}")
print(f"Forest #: {result['getTotalForest']()}")

# a: 1/8
# b: 2/7
# e: 3/6
# d: 4/5
# c: 9/12
# f: 10/11

# Parent: {'a': None, 'b': 'a', 'e': 'b', 'd': 'e', 'c': None, 'f': 'c'}
# Edges: {'tree': ['a->b', 'b->e', 'e->d', 'c->f'],
#         'back': ['d->b', 'f->f'], 'forward': ['a->d'], 'cross': ['c->e']}
# Forest  # : 2
