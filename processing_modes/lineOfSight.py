import csv
from collections import namedtuple

Node = namedtuple('Node', ['longitude', 'latitude', 'name'])
Edge = namedtuple('Edge', ['nodeA', 'nodeB'])

def read(nodes_file, edges_file):
    nodes = []
    edges = []
    for row in csv.DictReader(nodes_file):
        nodes.append(Node(float(row['longitude']), float(row['latitude']), row['name']))
    for row in csv.DictReader(edges_file):
        edges.append(Edge(row['nodeA'], row['nodeB']))

    return (nodes, edges)

def process(graph, anonymizer, decimals):
    nodes, edges = graph
    resultNodes = []
    for node in nodes:
        resultNodes.append(Node(*anonymizer(node.longitude, node.latitude, decimals), node.name))
    return (resultNodes, edges)

def write(graph, nodesOut, edgesOut):
    nodes, edges = graph
    nodesDict = {}
    nodesWriter = csv.DictWriter(nodesOut, fieldnames = ['name', 'longitude', 'latitude'])
    nodesWriter.writeheader()
    for node in nodes:
        nodesWriter.writerow(node._asdict())
        nodesDict[node.name] = node
        
    edgesWriter = csv.DictWriter(edgesOut, fieldnames = ['nodeA', 'nodeB', 'startLon', 'startLat', 'endLon', 'endLat'])
    edgesWriter.writeheader()
    for edge in edges:
        nodeLine = edge._asdict()
        nodeLine['startLat'] = nodesDict[edge.nodeA].latitude
        nodeLine['startLon'] = nodesDict[edge.nodeA].longitude
        nodeLine['endLat'] = nodesDict[edge.nodeB].latitude
        nodeLine['endLon'] = nodesDict[edge.nodeB].longitude
        edgesWriter.writerow(nodeLine)