# read the readme first!
# note that we are using Directed graph here but could have done undirected one too. The algoritm works for

graph = {
    'undershirt': ['pants', 'shoes'],
    'pants': ['shoes', 'belt'],
    'belt': ['jacket'],
    'shirt': ['tie', 'belt'],
    'tie': ['jacket'],
    'jacket': [],
    'socks': ['shoes'],
    'shoes': [],
    'watch': [],
}

# graph = {
#     'shirt': ['tie', 'belt'],
#     'watch': [],
#     'undershirt': ['pants', 'shoes'],
#     'socks': ['shoes'],
#     'pants': ['shoes', 'belt'],
#     'belt': ['jacket'],
#     'tie': ['jacket'],
#     'jacket': [],
#     'shoes': [],
# }


def dfs(adjList):
    parent = {}

    def topoSort():
        sortedItems = []

        return {
            'add': lambda item: sortedItems.insert(0, item),
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
            'edgeBelongsToForest': lambda: edgeBelongsToForest,
            'getTotalForest': lambda: forestNumber,
            'isCyclic': lambda: isCyclic
        }

    watchMen = gateKeeper()
    classifier = classifyEdge()
    topoSorter = topoSort()

    def dfsVisit(edge):
        watch = watchMen['gateTracker'](edge)
        watch['enter']()
        classifier['markEdgeAsExploring'](edge)

        for adj in adjList.get(edge, []):
            if adj not in parent:
                parent[adj] = edge
                classifier['classify'](edge, adj)
                dfsVisit(adj)  # follow this edge
            else:
                classifier['classify'](edge, adj)

        watch['exit']()
        topoSorter['add'](edge)
        classifier['updateEdgeAsExplored'](edge)

    for edge in adjList:
        if edge not in parent:
            classifier['incrementForest']()  # only time forest is discovered
            parent[edge] = None
            dfsVisit(edge)

    return {
        'parent': parent,
        'getEntryExitTime': watchMen['getGateLog'],
        'getEdgeClassification': classifier['getEdgeClassification'],
        'getTotalForest': classifier['getTotalForest'],
        'edgeBelongsToForest': classifier['edgeBelongsToForest'],
        'getSortedItems': topoSorter['getSortedItems']
    }


def getGateLog(log):
    val = ""
    for edge in log:
        timer = log.get(edge)
        enter = timer['enter']
        exit = timer['exit']
        val = f"{val}{edge}: {enter}/{exit}\n"

    return val


result = dfs(graph)
print(f"{getGateLog(result['getEntryExitTime']())}")
print(f"Parent: {result['parent']}")
print(f"Edges: {result['getEdgeClassification']()}")
print(f"Forest #: {result['getTotalForest']()}")
print(f"Edges and forest relation: #{result['edgeBelongsToForest']()}")
print(f"Topologically sorted Items: {result['getSortedItems']()}")

# undershirt: 1/10
# pants: 2/9
# shoes: 3/4
# belt: 5/8
# jacket: 6/7
# shirt: 11/14
# tie: 12/13
# socks: 15/16
# watch: 17/18

# Parent: {'undershirt': None, 'pants': 'undershirt', 'shoes': 'pants', 'belt': 'pants',
#          'jacket': 'belt', 'shirt': None, 'tie': 'shirt', 'socks': None, 'watch': None}
# Edges: {'tree': ['undershirt->pants', 'pants->shoes', 'pants->belt', 'belt->jacket', 'shirt->tie'],
#         'back': [], 'forward': ['undershirt->shoes'], 'cross': ['tie->jacket', 'shirt->belt', 'socks->shoes']}
# Forest  # : 4
# # {'undershirt': 1, 'pants': 1, 'shoes': 1, 'belt': 1, 'jacket': 1, 'shirt': 2, 'tie': 2, 'socks': 3, 'watch': 4}
# Edges and forest relation:
# Topologically sorted Items: ['watch', 'socks', 'shirt', 'tie', 'undershirt', 'pants', 'belt', 'jacket', 'shoes']
