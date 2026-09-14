GroundFloorCorridorDists = {"Reception":1,
                            "Corridor 1":10,
                            "Corridor 2a":8,"Corridor 2b":1,"Corridor 2x":1,
                            "Corridor 3":2,
                            "Corridor 4a":10,"Corridor 4b":2,"Corridor 4x":1,
                            "Atrium a":11,"Atrium b":2,
                            "Corridor 5":4,"Corridor 5x":1,
                            "Corridor 6a":2.5,"Corridor 6b":2.5,"Corridor 6c":3,"Corridor 6d":3,"Corridor 6e":3,
                            "Corridor 7":2,"Corridor 7x":2,
                            "Corridor 8a":6,"Corridor 8b":2,
                            "Corridor 9a":4,"Corridor 9b":2,"Corridor 9x":1,
                            "Corridor 10a":2,"Corridor 10b":4,
                            "Corridor 11a":5,"Corridor 11b":5,
                            "Corridor 12a":5, "Corridor 12b":5,
                            "Corridor 13a":3, "Corridor 13b":2,
                            "Corridor 14a":5, "Corridor 14x":1,"Corridor 14b":5,
                            "Corridor 15a":3, "Corridor 15b":4,
                            "Corridor 16":4,
                            "Corridor 17a":4,"Corridor 17b":3,"Corridor 17c":3,"Corridor 17x":1,
                            "Corridor 18a":5,"Corridor 18b":5,
                            "Corridor 19a":5,"Corridor 19b":5,
                            "Corridor 20":6,
                            "Corridor 21":5,
                            "Corridor 22":4,
                            "Corridor 23":4,
                            "Corridor 24":7,
                            "Corridor 25":3,
                            }

#need to do exits/entrances for some places
GroundFloorNodesAndCorridors = {
    "Reception":["0Reception Stairs,Ground","0Headmaster's Study","0G1","0G2","0Main Entrance"],
    "Corridor 1":["2G3","3G4","3G5","4G6","5G7","6G8","7G9","8G10"],
    "Corridor 2a":["0G11","2G12","2G13","4G14","5G15","5Barry Martin Centre","7G16","8G17"],"Corridor 2b":["0Cloisters","0StairsToLanguage,Ground"],"Corridor 2x":[], #check stair label
    "Corridor 3":[],
    "Corridor 4a":["0G25","3G24","6G23","8G18","7Barry Martin Centre"],"Corridor 4b":[],"Corridor 4x":[],
    "Atrium a":["0StairsToLibrary,Ground","0G42","0G43","0G44","0G45","1G46","3G57","5Atrium Toilets,Ground","5G48","7G49"],"Atrium b":[],
    "Corridor 5":["3StairsToHistory,Ground","3G51","5G52","7G53","8History Toilets,Ground","9G54"],"Corridor 5x":["0G50"],
    "Corridor 6a":["9G64","1StairsToBioligy,Ground"],"Corridor 6b":["9G62","0G63"],"Corridor 6c":["0G61"],"Corridor 6d":["8G58","0StairsToChemistry,Ground"],"Corridor 6e":["GG56","3G55","0G57"],
    "Corridor 7":[],"Corridor 7x":[],
    "Corridor 8a":[],"Corridor 8b":[],
    "Corridor 9a":["2G72","0GStairsToArt,Ground","2G70","4G71","4G69","9G68"],"Corridor 9b":["0G67"],"Corridor 9x":[],
    "Corridor 10a":[],"Corridor 10b":["9G66","9G65"],
    "Corridor 11a":["8G32","6G33","3G41","1G34"],"Corridor 11b":["0G30","0G31"],#check g34 corridor approach
    "Corridor 12a":["2Disabled Toilets,Ground,Cloisters","5Toilets,Ground,Cloisters"], "Corridor 12b":["3StairsToLatin,Ground","4G29","5G28","8G26","9G27"],
    "Corridor 13a":[], "Corridor 13b":[],
    "Corridor 14a":["1Medical Room","3G91A","5G91B"], "Corridor 14x":["0Main School Queue"],"Corridor 14b":["2G38","2G39","4G36","4G37","4G40","7G35"],
    "Corridor 15a":["0G79"], "Corridor 15b":[],
    "Corridor 16":["0StairsToEnglish,Ground","1G76","1G77","3Toilets,Ground,DesEng","4G75","7G74a","7G74","9G73","5G78"],
    "Corridor 17a":["0Lift,Ground,Hammond","5Hammond Theatre","9Disabled Toilets,Ground,Hammond Theatre"],"Corridor 17b":["0Staff Toilets,Ground,Hammond Theatre","3G81","9Changing Room,Ground,North Gym"],"Corridor 17c":[],"Corridor 17x":[],
    "Corridor 18a":[],"Corridor 18b":[],
    "Corridor 19a":[],"Corridor 19b":[],
    "Corridor 20":["0G86","0Toilets,Ground,Hammond Theatre","G85"],
    "Corridor 21":["0G89","3G88","4G87","5StairsToDanceStudio,Ground","5Lift,Ground,Dance Studio"],
    "Corridor 22":[],
    "Corridor 23":["9StairsToStaffDining,Ground"],
    "Corridor 24":["5Practise Rooms","0P11","7P10","9Staff Toilets,Ground,Garrik","8P9"],
    "Corridor 25":["7P1","4P2","4P8","2P7","2P3","0P4","0P5","0P6"],
    }


#need to add none/null connections or dead end node connections not finished
NodeConnections = {
    "Node 1":{"Node 24":"Corridor 11a", "Node 2":"Corridor 1", "Node 26":"Corridor 14b", "Node1x":"Reception"},
    "Node 1x":{"Node 1":"Reception"},
    "Node 2":{"Node 1":"Corridor 1", "Node 3":"Corridor 2a", "Node 4":"Atrium a"},
    "Node 2x":{"Node 2":"Corridor 2x"},
    "Node 3":{"Node 18":"Corridor 4a", "Node 4":"Corridor 4b", "Node 6":"Corridor 2b"},
    "Node 4":{"Node 2":"Atrium a", "Node 3":"Corridor 4b", "Node 5":"Atrium b"},
    "Node 4x":{"Node 4":"Corridor 4x"},
    "Node 5":{"Node 4":"Atrium b", "Node 6":"Corridor 3"},
    "Node 5x":{"Node 5":"Corridor 5x"},
    "Node 6":{"Node 3":"Corridor 2b", "Node 5":"Corridor 3", "Node 7":"Corridor 8b"},
    "Node 7":{"Node 6":"Corridor 8b", "Node 10":"Corridor 7", "Node 16":"Corridor 8a"},
    "Node 8":{"Node 5":"Corridor 5", "Node 9":"Corridor 6e"},
    "Node 9":{"Node 8":"Corridor 6e", "Node 10":"Corridor 6d"},
    "Node 10":{"Node 9":"Corridor 6d", "Node 11":"Corridor 6c", "Node 7":"Corridor 7"},
    "Node 10x":{"Node 10":"Corridor 7x"},
    "Node 11":{"Node 10":"Corridor 6b", "Node 12":"Corridor 6b",},
    "Node 12":{"Node 11":"Corridor 6b", "Node 16":"Corridor 10b", "Node 13":"Corridor 6a"},
    "Node 13":{"Node 12":"Corridor 6a", "Node 14":"Corridor 9b"},
    "Node 13x":{"Node 13":"Corridor 9x"},
    "Node 14":{"Node 13":"Corridor 9b", "Node 17":"Corridor 13b", "Node 15":"Corridor 9a"},
    "Node 15":{"Node 14":"Corridor 9a", "Node 20":"Corridor 15a"},
    "Node 16":{"Node 12":"Corridor 10b", "Node 7":"Corridor 8a", "Node 18":"Corridor 10a"},
    "Node 17":{"Node 14":"Corridor 13b", "Node 19":"Corridor 13a", "Node 20":"Corridor 15b"},
    "Node 18":{"Node 16":"Corridor 10a", "Node 3":"Corridor 4a", "Node 24":"Corridor 11b", "Node 19":"Corridor 12b"},
    "Node 19":{"Node 18":"Corridor 12b", "Node 17":"Corridor 13a", "Node 21":"Corridor 12a", "Node 23":"Corridor 19b"},
    "Node 20":{"Node 15":"Corridor 15a", "Node 17":"Corridor 15b", "Node 21":"Corridor 17c"},
    "Node 20x":{"Node 20":"Corridor 17x"},
    "Node 21":{"Node 20":"Corridor 17c", "Node 19":"Corridor 12a", "Node 22":"Corridor 17b"},
    "Node 22":{"Node 21":"Corridor 17b", "Node 23":"Corridor 18a", "Node 25":"Corridor 17a", "Node 27":"Corridor 20"},
    "Node 23":{"Node 22":"Corridor 18a", "Node 24":"Corridor 18b", "Node 26":"Corridor 19a", "Node 19":"Corridor 19b"},
    "Node 24":{"Node 23":"Corridor 18b", "Node 18":"Corridor 11b", "Node 1":"Corridor 11a"},
    "Node 25":{"Node 22":"Corridor 17a", "Node 26":"Corridor 14a"},
    "Node 25xa":{"Node 25":"Corridor 22"},
    "Node 25xb":{"Node 25":"Corridor 23"},
    "Node 26":{"Node 25":"Corridor 14a", "Node 23":"Corridor 19a", "Node 1":"Corridor 14b"},
    "Node  26x":{"Node 26":"Corridor 14x"},
    "Node 27":{"Node 22":"Corridor 20"},
    "Node 28":{"Node 28x":"Corridor 24","None":"Corridor 25"},
    "Node 28x":{"Node 28":"Corridor 24"},
    }
#This Works#
'''
graph = {}
toprint = {}
for node in NodeConnections:
        for key in NodeConnections[node]:
                toprint[key] = GroundFloorCorridorDists[NodeConnections[node][key]]
        graph[node] = toprint
        toprint = {}
'''
#But this is cooler
graph = {node:{neighbour_node:GroundFloorCorridorDists[NodeConnections[node][neighbour_node]] for neighbour_node in NodeConnections[node]} for node in NodeConnections}
#||#

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

def total_path_dist(distances,endnode):
    return distances(endnode)

#start_node = 'Node 1'
#end_node = 'Node 20'
'''
run = input("Start?")
while run.lower() != "n":
        start_node,end_node = input("Give me a start and end node seperated by a comma").split(",")
        distances, path = dijkstra_recursive(graph, start_node, end_node)
        if path == ["Node 1"]:
                print("Node not reachable as of now")
        else:
                print(f"Shortest distances from {start_node}: {distances}")
                print(f"Shortest path from {start_node} to {end_node}: {path}")
        run = input("Start?")'
'''

def stripper(currentcorridor,currentroom):
    char =  mapper[currentcorridor][1][currentroom]
    char_ = ""
    for x in char:
        if x != ",":
            char_ += x
        elif x == ",":
            break
    return char_

def linkcorridortonode(corridor):
    nodes = []
    for node in NodeConnections:
        for neighbournode in NodeConnections[node]:
            #print(NodeConnections[node][neighbournode])
            if NodeConnections[node][neighbournode] == corridor:
                print("https://integralmaths.org/")
                nodes.append(node)
                break
    return nodes

mapper =list(GroundFloorNodesAndCorridors.items())
run = input("Start?")

def findroomtocorridor(roomwhere):
    found = False
    currentcorridor = 0
    currentroom = 0
    while found is False:
        try:
            roomsearch=stripper(currentcorridor,currentroom)[1:]
            if roomwhere == roomsearch:
                print(f"{roomwhere}:{mapper[currentcorridor][0]}")
                print(linkcorridortonode(mapper[currentcorridor][0]))
                #found = True
                return [roomwhere,mapper[currentcorridor][0],linkcorridortonode(mapper[currentcorridor][0])]
            elif (currentcorridor == len(mapper)-1)and(currentroom==len(mapper[currentcorridor][1])-1):
                print("room not in map")
                return None
                #found = True     
            elif (len(mapper[currentcorridor][1])==0)or(currentroom == len(mapper[currentcorridor][1])-1):
                currentcorridor += 1
                currentroom = 0

            else:
                currentroom += 1
        except IndexError:
            if (currentcorridor == len(mapper)-1)and(currentroom==len(mapper[currentcorridor][1])-1):
                print("room not in map")
                return None
                #found = True
            elif (currentroom == len(mapper[currentcorridor][1])-1)or(len(mapper[currentcorridor][1])==0):
                currentcorridor += 1
                currentroom = 0    

room1,room2 = input("Give me two rooms").split(",")
info = [] #room, corridor, node
info.append(findroomtocorridor(room1))
info.append(findroomtocorridor(room2))
print(info)
dijkstra_recursive(graph,info[0][2],info[1][2])
dists = {}
def mindist():
    global dists
    