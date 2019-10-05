from random import SystemRandom
from collections import namedtuple
import statistics
from numpy.random import normal
from math import radians, cos, sin, asin, sqrt
from typing import List

Node = namedtuple('Node', ['longitude', 'latitude', 'name'])
Edge = namedtuple('Edge', ['nodeA', 'nodeB'])

def randomize(graph, nodeProbability, edgeProbability):
    rng = SystemRandom()
    nodes, edges = graph
    goalNodes = len(nodes) + rng.randint(0, int(len(nodes) * (1 - nodeProbability)))
    goalEdges = len(edges) + rng.randint(0, int(len(edges) * (1 - edgeProbability)))

    resultNodes = [node for node in nodes if rng.random() <= nodeProbability + nodeDegreeWeight(node, nodes, edges)]
    validOriginalEdges = [edge for edge in edges if any((node for node in resultNodes if edge.nodeA == node.name)) \
                             and any((node for node in resultNodes if edge.nodeB == node.name))]

    edgeProbability = edgeProbability * len(edges) / len(validOriginalEdges)

    resultEdges = [edge for edge in validOriginalEdges if rng.random() <= edgeProbability]

    latitudeDist = getDistribution([node.latitude for node in nodes])
    longitudeDist = getDistribution([node.longitude for node in nodes])
    numOutEdgesDist = getDistribution([len([edge for edge in edges if edge.nodeA == node.name]) for node in nodes])
    pathLengthDist = getDistribution(list(
            map(lambda edge: haversine(edge[0].longitude, edge[0].latitude, edge[1].longitude, edge[1].latitude), \
                map(lambda edge: getNodeObjectsForEdge(edge, nodes), edges))))

    anyFakes, resultNodes, resultEdges = createFakeNodes(goalNodes, resultNodes, resultEdges, latitudeDist, longitudeDist, numOutEdgesDist, pathLengthDist)
    resultEdges = ensureGoalEdgesNoSingletons(goalEdges, resultNodes, resultEdges, pathLengthDist)

    if anyFakes:
        resultNodes, resultEdges = renameGraph(resultNodes, resultEdges)

    return (resultNodes, resultEdges)

def renameGraph(nodes: List[Node], edges: List[Edge]):
    nameMap = {}
    newNodes = []
    newEdges = []
    for node in nodes:
        nameMap[node.name] = "Node{}".format(len(nameMap))
        newNodes.append(Node(node.longitude, node.latitude, nameMap[node.name]))
    for edge in edges:
        newEdges.append(Edge(nameMap[edge.nodeA], nameMap[edge.nodeB]))
    return (newNodes, newEdges)

def ensureGoalEdgesNoSingletons(goalEdges, nodes: List[Node], edges: List[Edge], distanceDist):
    rng = SystemRandom()
    while len(edges) > goalEdges:
        edgeToRemove = rng.randint(0, len(edges) - 1)
        edges.pop(edgeToRemove)
    while len(edges) < goalEdges:
        srcNode = nodes[rng.randint(0, len(nodes) - 1)]
        target = getTargetNode(srcNode, [node for node in nodes if node != srcNode], distanceDist.sample())
        if Edge(srcNode.name, target.name) not in edges and Edge(target.name, srcNode.name) not in edges:
            edges.append(Edge(srcNode.name, target.name))
    for singleton in (node for node in nodes if len([edge for edge in edges if edge.nodeA == node.name or edge.nodeB == node.name]) == 0):
        target = getTargetNode(singleton, [node for node in nodes if node != singleton], distanceDist.sample())
        edges.append(Edge(singleton.name, target.name))
    return edges
    

def createFakeNodes(goalNodes, initialNodes: List[Node], initialEdges: List[Edge], latitudeDist, longitudeDist, numEdgeOutDist, pathLengthDist):
    createdNode = False
    finalNodes = initialNodes
    finalEdges = initialEdges
    rng = SystemRandom()
    for i in range(len(initialNodes), goalNodes):
        createdNode = True
        newNode = Node(longitudeDist.sample(), latitudeDist.sample(), "Generated{}".format(i))
        for _ in range(int(numEdgeOutDist.sample())):
            finalEdges.append(getNewRandomEdge(rng, newNode, finalNodes, pathLengthDist))
        finalNodes.append(newNode)

    return (createdNode, finalNodes, finalEdges)

def getNewRandomEdge(rng, newNode, nodes, pathLengthDist):
    isOut = bool(rng.randint(0, 1))
    target = getTargetNode(newNode, nodes, pathLengthDist.sample())
    if isOut:
        return Edge(newNode.name, target.name)
    else:
        return Edge(target.name, newNode.name)

def getTargetNode(source, targets, distance):
    distKey = lambda node: abs(haversine(source.longitude, source.latitude, node.longitude, node.latitude) - distance)
    return min(targets, key=distKey)

def nodeDegree(node, edges):
    return len([edge for edge in edges if edge.nodeA == node.name or edge.nodeB == node.name])

def nodeDegreeWeight(target, nodes, edges):
    degree = nodeDegree(target, edges)
    return 1 - len([node for node in nodes if node != target and nodeDegree(node, edges) >= degree]) / (len(nodes) - 1.0)

def getNodeObjectsForEdge(edge, nodes):
    return (next((node for node in nodes if node.name == edge.nodeA)), next((node for node in nodes if node.name == edge.nodeB)))

Distribution = namedtuple('Distribution', ['mean', 'stddev', 'sample'])

def getDistribution(values):
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    return Distribution(mean, stdev, lambda: round(normal(mean, stdev), 3))


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 * 1000 # Radius of earth in kilometers. Use 3956 for miles
    return c * r