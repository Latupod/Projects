import Data
CorridorContent = Data.CorridorContent
CorridorDists = Data.CorridorDists
NodeConnections = Data.NodeConnections
NodeCoords = Data.NodeCoords
CorridorFloorMapper = Data.CorridorFloorMapper
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
    #print(f"Distances: {distances}") #REMOVE
    if not queue: #is the queue is empty so done 
        return distances, reconstruct_path(predecessors, start, end)  # Return distances and path
    
    current_distance, current_node = extract_min(queue) #take node from queue with the current lowest distance to the node were currently at at set this to be the new current node were currently looking at
    #print(f"Current Distance: {current_distance} Current node: {current_node}") #REMOVE
    
    if current_node in visited: #if current node is already visited continue recrusivly to the next node
        return dijkstra_recursive(graph, start, end, visited, distances, queue, predecessors)
    
    visited.add(current_node) #mark current node as visited
    
    for neighbor, weight in graph[current_node].items(): #convert dictionary into a list of key value pairs using .items and loop through the neighbour nodes to the current node and its weighting
        if neighbor not in visited: #if nodes isnt visited
            #print(neighbor) #REMOVE
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

from functools import reduce
def total_path_dist(distances,path):
    return reduce(lambda x,y: x+y,[distances[x] for x in path])

def stripper(currentcorridor,currentroom,mapper):
    char =  mapper[currentcorridor][1][currentroom]
    char_ = ""
    for x in char:
        if x != ",":
            char_ += x
        elif x == ",":
            break
    return char_

def linkcorridortonode(corridor): #passing node connections
    nodes = []
    for node in NodeConnections:
        for neighbournode in NodeConnections[node]:
            if NodeConnections[node][neighbournode] == corridor:
                nodes.append(node)
    return nodes

def findroomtocorridor(roomwhere,mapper):
    currentcorridor = 0
    currentroom = 0
    while True:
        try:
            roomsearch=stripper(currentcorridor,currentroom,mapper)[1:]
            #print(f"{mapper[currentcorridor][1][currentroom]}:{roomsearch}")
            if roomwhere == roomsearch:
                return [roomwhere,mapper[currentcorridor][0],linkcorridortonode(mapper[currentcorridor][0]),mapper[currentcorridor][1][currentroom],findfloor(mapper[currentcorridor][0])]
            elif (currentcorridor == len(mapper)-1)and(currentroom==len(mapper[currentcorridor][1])-1):
                print("room not in map")
                return None   
            elif (len(mapper[currentcorridor][1])==0)or(currentroom == len(mapper[currentcorridor][1])-1):
                currentcorridor += 1
                currentroom = 0
            else:
                currentroom += 1
        except IndexError:
            if (currentcorridor == len(mapper)-1)and(currentroom==len(mapper[currentcorridor][1])-1):
                print("room not in map")
                return None
            elif (currentroom == len(mapper[currentcorridor][1])-1)or(len(mapper[currentcorridor][1])==0):
                currentcorridor += 1
                currentroom = 0    

def min_dist(info,graph): #passing GroundFloorCorridorDists
    lowest_dist = 100000000
    distsandpath = {}
    for node_1 in info[0][2]:
        for node_2 in info[1][2]:
            distance,path = dijkstra_recursive(graph,node_1,node_2)
            distsandpath[f"{node_1}:{node_2}"] = [(total_path_dist(distance,path)+CorridorDists[info[0][1]]+CorridorDists[info[1][1]]),path]
    for corridor in distsandpath:
        if distsandpath[corridor][0] < lowest_dist:
            lowest_dist = distsandpath[corridor][0]

    return [(key,distsandpath[key]) for key in distsandpath if distsandpath[key][0]==lowest_dist]

def decodepathofnodestocorridors(path,start,end): #passing NodeConnections
    Cpath = [start]
    for node in range(len(path)-1):
        Cpath.append(NodeConnections[path[node]][path[node+1]])
    Cpath.append(end)
    return Cpath

def findfloor(corridor):
    for floor in CorridorFloorMapper:
        for corridors in CorridorFloorMapper[floor]:
            if corridor == corridors:
                return floor

def maincode(room1,room2):
    mapper =list(CorridorContent.items())
    info = [] #room, corridor, node, room with spacing id , floor
    floor = []
    info.append(findroomtocorridor(room1,mapper))
    info.append(findroomtocorridor(room2,mapper))
    for item in info:
        floor.append(item[4]) 
        print(item)
    if info[0][1] == info[1][1]:
        print("in same corridor")
    else:
        graph = {node:{neighbour_node:CorridorDists[NodeConnections[node][neighbour_node]] for neighbour_node in NodeConnections[node]} for node in NodeConnections}
        mindist = min_dist(info,graph)
        print(f"MinDist: {mindist[0][1][1]} of dist {mindist[0][1][0]}")
        print(f"Path: {decodepathofnodestocorridors(mindist[0][1][1],info[0][1],info[1][1])}")      
        return (mindist[0][1][1],decodepathofnodestocorridors(mindist[0][1][1],info[0][1],info[1][1]),info[0][2],info[1][2],info[0][3],info[1][3],floor)

#print(maincode())
#maincode("","")