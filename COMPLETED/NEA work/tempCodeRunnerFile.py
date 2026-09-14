GroundFloorCorridorDists = {"Reception":1,
                            "Corridor 1":10,
                            "Corridor 2a":8,
                            "Corridor 2b":1,
                            "Corridor 2x":1,
                            "Corridor 3":2,
                            "Corridor 4a":10,
                            "Corridor 4b":2,
                            "Corridor 4x":1,
                            "Atrium a":11,
                            "Atrium b":2,
                            "Corridor 5":4,
                            "Corridor 5x":1,
                            "Corridor 6a":2.5,
                            "Corridor 6b":2.5,
                            "Corridor 6c":3,
                            "Corridor 6d":3,
                            "Corridor 6e":3,
                            "Corridor 7":2,
                            "Corridor 7x":2,
                            "Corridor 8a":6,
                            "Corridor 8b":2,
                            "Corridor 9a":4,
                            "Corridor 9b":2,
                            "Corridor 9x":1,
                            "Corridor 10a":2,
                            "Corridor 10b":5,
                            "Corridor 11a":5,
                            "Corridor 11b":5,
                            "Corridor 12a":5,
                            "Corridor 12b":5,
                            "Corridor 13a":3,
                            "Corridor 13b":2,
                            "Corridor 14a":5,
                            "Corridor 14x":1,
                            "Corridor 14b":5,
                            "Corridor 15a":3,
                            "Corridor 15b":4,
                            "Corridor 16":4,
                            "Corridor 17a":4,
                            "Corridor 17b":3,
                            "Corridor 17c":3,
                            "Corridor 17x":1,
                            "Corridor 18a":5,
                            "Corridor 18b":5,
                            "Corridor 19a":5,
                            "Corridor 19b":5,
                            "Corridor 20":6,
                            "Corridor 21":5,
                            "Corridor 22":4,
                            "Corridor 23":4,
                            "Corridor 24":7,
                            "Corridor 25":3,
                            }


GroundFloorNodesAndCorridors = {"":[]}

NodeConnections = {
    "Node 1":{"Node 24":"Corridor 11a", "Node 2":"Corridor 1", "Node 26":"Corridor 14b"},
    "Node 2":{"Node 1":"Corridor 1", "Node 3":"Corridor 2a", "Node 4":"Atrium a"},
    "Node 3":{"Node 18":"Corridor 4a", "Node 4":"Corridor 4b", "Node 6":"Corridor 2b"},
    "Node 4":{"Node 2":"Atrium a", "Node 3":"Corridor 4b", "Node 5":"Atrium b"},
    "Node 5":{"Node 4":"Atrium b", "Node 6":"Corridor 3"},
    "Node 6":{"Node 3":"Corridor 2b", "Node 5":"Corridor 3", "Node 7":"Corridor 8b"},
    "Node 7":{"Node 6":"Corridor 8b", "Node 10":"Corridor 7", "Node 16":"Corridor 8a"},
    "Node 8":{"Node 5":"Corridor 5", "Node 9":"Corridor 6e"},
    "Node 9":{"Node 8":"Corridor 6e", "Node 10":"Corridor 6d"},
    "Node 10":{"Node 9":"Corridor 6d", "Node 11":"Corridor 6c", "Node 7":"Corridor 7"},
    "Node 11":{"Node 10":"Corridor 6b", "Node 12":"Corridor 6b",},
    "Node 12":{"Node 11":"Corridor 6b", "Node 16":"Corridor 10b", "Node 13":"Corridor 6a"},
    "Node 13":{"Node 12":"Corridor 6a", "Node 14":"Corridor 9b"},
    "Node 14":{"Node 13":"Corridor 9b", "Node 17":"Corridor 13b", "Node 15":"Corridor 9a"},
    "Node 15":{"Node 14":"Corridor 9a", "Node 20":"Corridor 15a"},
    "Node 16":{"Node 12":"Corridor 10b", "Node 7":"Corridor 8a", "Node 18":"Corridor 10a"},
    "Node 17":{"Node 14":"Corridor 13b", "Node 19":"Corridor 13a", "Node 20":"Corridor 15b"},
    "Node 18":{"Node 16":"Corridor 10a", "Node 3":"Corridor 4a", "Node 24":"Corridor 11b", "Node 19":"Corridor 12b"},
    "Node 19":{"Node 18":"Corridor 12b", "Node 17":"Corridor 13a", "Node 21":"Corridor 12a", "Node 23":"Corridor 19b"},
    "Node 20":{"Node 15":"Corridor 15a", "Node 17":"Corridor 15b", "Node 21":"Corridor 17c"},
    "Node 21":{"Node 20":"Corridor 17c", "Node 19":"Corridor 12a", "Node 22":"Corridor 17b"},
    "Node 22":{"Node 21":"Corridor 17b", "Node 23":"Corridor 18a", "Node 25":"Corridor 17a", "Node 27":"Corridor 20"},
    "Node 23":{"Node 22":"Corridor 18a", "Node 24":"Corridor 18b", "Node 26":"Corridor 19a", "Node 19":"Corridor 19b"},
    "Node 24":{"Node 23":"Corridor 18b", "Node 18":"Corridor 11b", "Node 1":"Corridor 11a"},
    "Node 25":{"Node 22":"Corridor 17a", "Node 26":"Corridor 14a"},
    "Node 26":{"Node 25":"Corridor 14a", "Node 23":"Corridor 19a", "Node 1":"Corridor 14b"},
    "Node 27":{"Node 22":"Corridor 20"},
    "Node 28":{},
    }

graph = {}

#toprint = ""
toprint = {}
for node in NodeConnections:
        for key in NodeConnections[node]:
                #toprint += key + ":" + str(GroundFloorCorridorDists[NodeConnections[node][key]]) + ", " 
                toprint[key] = GroundFloorCorridorDists[NodeConnections[node][key]]
        #print(f"Node:{node} || {toprint}")
        graph[node] = toprint
        toprint = {}
        #toprint = ""


def extract_min(queue):
    min_index = 0
    for current_node in range(1, len(queue)):
        if queue[current_node][0] < queue[min_index][0]: #If the distance for term i in queue is less than the current minimum distance to term min index
            min_index = current_node #set new min_index to current_node
    return queue.pop(min_index)

def dijkstra_recursive(graph, start, end, visited=None, distances=None, queue=None, predecessors=None):
    if visited is None: #At the start when first running such this runs once
        visited = set() #created the visited set
        distances = {node: float('inf') for node in graph} #create dicitonary of nodes with each distance to the staart node as infinity
        distances[start] = 0 #set distance from start node to start node as 0 (obvisouly)
        queue = [(0, start)]  # (distance, node) #the start node is added to the queue
        predecessors = {} #predecessor list to track the path being taken
    #print(f"Distances: {distances}")
    if not queue: #is the queue is empty so done 
        return distances, reconstruct_path(predecessors, start, end)  # Return distances and path
    
    current_distance, current_node = extract_min(queue) #take node from queue with the current lowest distance to the node were currently at at set this to be the new current node were currently looking at
    #print(f"Current Distance: {current_distance} Current node: {current_node}")
    
    if current_node in visited: #if current node is already visited continue recrusivly to the next node
        return dijkstra_recursive(graph, start, end, visited, distances, queue, predecessors)
    
    visited.add(current_node) #mark current node as visited
    
    for neighbor, weight in graph[current_node].items(): #convert dictionary into a list of key value pairs using .items and loop through the neighbour nodes to the current node and its weighting
        if neighbor not in visited: #if nodes isnt visited
            new_distance = current_distance + weight #calculate a new distance to that node (from start node)
            if new_distance < distances[neighbor]: #if the new distances is lower than the current lowest distance to the neighbour (from start node)
                distances[neighbor] = new_distance #set new distance to be the lowest distance to neighbour (from start nodw)
                predecessors[neighbor] = current_node #set the current node as the closest node to the neighbour node
                queue.append((new_distance, neighbor))#add the new distance and neighbour to the queue
    
    return dijkstra_recursive(graph, start, end, visited, distances, queue, predecessors)

def reconstruct_path(predecessors, start, end):
    path = []
    current = end
    while current in predecessors:
        path.append(current)
        current = predecessors[current]
    path.append(start)
    return path[::-1]  # Reverse the path

#start_node = 'Node 1'
#end_node = 'Node 20'
run = input("Start?")
while run.lower() != "n":
        start_node,end_node = input("Give me a start and end node seperated by a comma").split(",")
        distances, path = dijkstra_recursive(graph, start_node, end_node)
        if path == ["Node 1"]:
                print("Node not reachable as of now")
        else:
                print(f"Shortest distances from {start_node}: {distances}")
                print(f"Shortest path from {start_node} to {end_node}: {path}")
        run = input("Start?")