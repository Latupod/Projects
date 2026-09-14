GroundFloorCorridorDists = {"Reception":1,                          
                            "Corridor 1b":10,"Corridor 1a":3,
                            "Corridor 2a":8,"Corridor 2b":1, "Corridor 2c":1, "Corridor 2x":1,
                            "Corridor 3":2,
                            "Corridor 4a":10,"Corridor 4b":2,"Corridor 4x":1,
                            "Atrium a":11,"Atrium b":2,
                            "Corridor 5":4,"Corridor 5xa":1,"Corridor 5xb":1,
                            "Corridor 6a":2.5,"Corridor 6b":2.5,"Corridor 6c":3,"Corridor 6d":3,"Corridor 6e":3,
                            "Corridor 7":2,"Corridor 7x":2,
                            "Corridor 8a":6,"Corridor 8b":2,
                            "Corridor 9a":2,"Corridor 9b":3,"Corridor 9c":3,"Corridor 9x":1,
                            "Corridor 10a":2,"Corridor 10b":4,
                            "Corridor 11a":5,"Corridor 11b":5,
                            "Corridor 12a":5, "Corridor 12b":5,
                            "Corridor 13a":3, "Corridor 13b":2,
                            "Corridor 14a":5, "Corridor 14x":1,"Corridor 14b":5,
                            "Corridor 15a":3, "Corridor 15b":4,"Corridor 15c":3,
                            "Corridor 16":4,
                            "Corridor 17a":4,"Corridor 17b":3,"Corridor 17c":3,"Corridor 17x":1,
                            "Corridor 18a":5,"Corridor 18b":5,
                            "Corridor 19a":5,"Corridor 19b":5,
                            "Corridor 20":6,
                            "Corridor 21":5,
                            "Corridor 22":4,
                            "Corridor 23a":4,
                            "Corridor 23b":1,
                            "Corridor 24":7,
                            "Corridor 25":3,
                            "Corridor 25x":1,
                            "Corridor GSLi":1,
                            "Corridor GSR":1,
                            "Corridor GSL":1,
                            "Corridor GSH":1,
                            "Corridor GSC":1,
                            "Corridor GSB":1,
                            "Corridor GSE":1,
                            "Corridor GSSD":1,
                            "Corridor GSDS":1,
                            "Corridor GSLtn":1,
                            }

StairsGround = ["0Reception Stairs,Ground","0StairsToLibrary,Ground","0StairsToLanguage,Ground","3StairsToHistory,Ground",
          "1StairsToBioligy,Ground","0StairsToChemistry,Ground","0GStairsToArt,Ground","3StairsToLatin,Ground",
          "0StairsToEnglish,Ground","5StairsToDanceStudio,Ground","9StairsToStaffDining,Ground"]


#need to do exits/entrances for some places
GroundFloorNodesAndCorridors = {
    "Reception":["0Headmaster's Study","0G1","0G2","0Main Entrance"],
    "Corridor GSR":["0Reception Stairs,Ground"],
    "Corridor 1a":["2G3","3G4","3G5","4G6","5G7","6G8","7G9","8G10"],
    "Corridor 1b":[],
    "Corridor 2a":["0G11","2G12","2G13","4G14","5G15","5Barry Martin Centre","7G16","8G17"],"Corridor 2b":["0Cloisters",],"Corridor 2c":[],"Corridor 2x":[], #check stair label
    "Corridor GSLi":["0StairsToLibrary,Ground"],
    "Corridor GSL":["0StairsToLanguage,Ground"],
    "Corridor 3":[],
    "Corridor 4a":["0G25","3G24","6G23","8G18","7Barry Martin Centre"],"Corridor 4b":[],"Corridor 4x":[],
    "Atrium a":["0G42","0G43","0G44","0G45","1G46","3G57","5Atrium Toilets,Ground","5G48","7G49"],"Atrium b":[],
    "Corridor 5":["3G51","5G52","7G53","8History Toilets,Ground","9G54"],"Corridor 5xb":["0G50"],"Corridor 5xa":[],
    "Corridor GSH":["0StairsToHistory,Ground"],
    "Corridor 6a":["9G64",],"Corridor 6b":["9G62","0G63"],"Corridor 6c":["0G61"],"Corridor 6d":["8G58",],"Corridor 6e":["GG56","3G55","0G57"],
    "Corridor GSC":["0StairsToChemistry,Ground"],
    "Corridor GSB":["0StairsToBioligy,Ground"],
    "Corridor 7":[],"Corridor 7x":[],
    "Corridor 8a":[],"Corridor 8b":[],
    "Corridor 9a":[],"Corridor 9b":["2G72","2G70","4G71","4G69","9G68","3GStairsToArt,Ground",],"Corridor 9c":["0G67"],"Corridor 9x":[],
    "Corridor 10a":[],"Corridor 10b":["9G66","9G65"],
    "Corridor 11a":["8G32","6G33","3G41","1G34"],"Corridor 11b":["0G30","0G31"],#check g34 corridor approach
    "Corridor 12a":["2Disabled Toilets,Ground,Cloisters","5Toilets,Ground,Cloisters"], "Corridor 12b":["4G29","5G28","8G26","9G27"],
    "Corridor GSLtn":["0StairsToLatin,Ground",],
    "Corridor 13a":[], "Corridor 13b":[],
    "Corridor 14a":["1Medical Room","3G91A","5G91B"], "Corridor 14x":["0Main School Queue"],"Corridor 14b":["2G38","2G39","4G36","4G37","4G40","7G35"],
    "Corridor 15a":["0G79"], "Corridor 15b":[],"Corridor 15c":[],
    "Corridor 16":["1G76","1G77","3Toilets,Ground,DesEng","4G75","7G74a","7G74","9G73","5G78"],
    "Corridor GSE":["0StairsToEnglish,Ground",],
    "Corridor 17a":["0Lift,Ground,Hammond","5Hammond Theatre","9Disabled Toilets,Ground,Hammond Theatre"],"Corridor 17b":["0Staff Toilets,Ground,Hammond Theatre","3G81","9Changing Room,Ground,North Gym"],"Corridor 17c":[],"Corridor 17x":[],
    "Corridor 18a":[],"Corridor 18b":[],
    "Corridor 19a":[],"Corridor 19b":[],
    "Corridor 20":["0G86","0Toilets,Ground,Hammond Theatre","G85"],
    "Corridor 21":["0G89","3G88","4G87","5Lift,Ground,Dance Studio"],
    "Corridor GSDS":["0StairsToDanceStudio,Ground",],
    "Corridor 22":["9Lower School Queue"],
    "Corridor 23":["4Dining Hall"],
    "Corridor GSSD":["0StairsToStaffDining,Ground"],
    "Corridor 24":["5Practise Rooms","0P11","7P10","9Staff Toilets,Ground,Garrik","8P9"],
    "Corridor 25":["7P1","4P2","4P8","2P7","2P3","0P4","0P5","0P6"],
    "Corridor 25x":["0Garrik"],
    }


#need to add none/null connections or dead end node connections not finished
NodeConnections = {
    "Node 1":{"Node 24":"Corridor 11a", "Node 2a":"Corridor 1a", "Node 26":"Corridor 14b", "Node 1x":"Reception","Reception Stairs Ground":"Corridor GSR"},
    "Reception Stairs Ground":{"Node 1":"Corridor GSR"}, #Add the next floor node asw e.g. "Reception Stairs First":"Corridor SSR" #Note G is ground, S is stair, R is reception
    "Node 1x":{"Node 1":"Reception"},
    "Node 2a":{"Node 1":"Corridor 1a", "Node 3a":"Corridor 2a", "Node 2b":"Corridor 1b","Library Stairs Ground":"Corridor GSLi","Node 2x":"Corridor 2x"},
    "Node 2b":{"Node 2a":"Corridor 1b","Node 4":"Atrium a"},
    "Library Stairs Ground":{"Node 2a":"Corridor GSLi"},#Add the next floor node asw
    "Node 2x":{"Node 2a":"Corridor 2x"},
    "Node 3a":{"Node 18":"Corridor 4a","Node 3b":"Corridor 2c","Node 2a":"Corridor 2a"},
    "Node 3b":{"Language Stairs Ground":"Corridor GSL", "Node 4":"Corridor 4b", "Node 6":"Corridor 2b", "Node 3a":"Corridor 2c"},
    "Language Stairs Ground":{"Node 3b":"Corridor GSL"},
    "Node 4":{"Node 2b":"Atrium a", "Node 3b":"Corridor 4b", "Node 5":"Atrium b"},
    "Node 4x":{"Node 4":"Corridor 4x"},
    "Node 5":{"Node 4":"Atrium b", "Node 6":"Corridor 3","History Stairs Ground":"Corridor GSH"},
    "History Stairs Ground":{"Node 5":"Corridor GSH","Node 5xb":"Corridor 5xa"},
    "Node 5xa":{"Node 5xb":"Corridor 5xb",},    
    "Node 5xb":{"History Stairs Ground":"Corridor 5xa","Node 5xa":"Corridor 5xb","Node 8":"Corridor 5"},
    "Node 6":{"Node 3b":"Corridor 2b", "Node 5":"Corridor 3", "Node 7":"Corridor 8b"},
    "Node 7":{"Node 6":"Corridor 8b", "Node 10":"Corridor 7", "Node 16":"Corridor 8a"},
    "Node 8":{"Node 5xb":"Corridor 5", "Node 9":"Corridor 6e"},
    "Node 9":{"Node 8":"Corridor 6e", "Node 10":"Corridor 6d"},
    "Node 10":{"Node 9":"Corridor 6d", "Node 11":"Corridor 6c", "Node 7":"Corridor 7", "Chemistry Stairs Ground":"Corridor GSC"},
    "Chemistry Stairs Ground":{"Node 10":"Corridor GSC"},
    "Node 10x":{"Node 10":"Corridor 7x"},
    "Node 11":{"Node 10":"Corridor 6b", "Node 12":"Corridor 6b",},
    "Node 12":{"Node 11":"Corridor 6b", "Node 16":"Corridor 10b", "Node 13":"Corridor 6a"},
    "Node 13":{"Node 12":"Corridor 6a", "Node 14":"Corridor 9c", "Bioligy Stairs Ground":"Corridor GSB"},
    "Bioligy Stairs Ground":{"Node 13":"Corridor GSB"},
    "Node 13x":{"Node 13":"Corridor 9x"},
    "Node 14":{"Node 13":"Corridor 9c", "Node 17":"Corridor 13b", "Art Stairs Ground":"Corridor 9b"},
    "Node 15":{"Art Stairs Ground":"Corridor 9a", "Node 20":"Corridor 15a", "Art Stairs Ground":"Corridor 9a"},
    "Art Stairs Ground":{"Node 15":"Corridor 9a", "Node 14":"Corridor 9b"},
    "Node 16":{"Node 12":"Corridor 10b", "Node 7":"Corridor 8a", "Node 18":"Corridor 10a"},
    "Node 17":{"Node 14":"Corridor 13b", "Node 19":"Corridor 13a", "Node 20x":"Corridor 15b"},
    "Node 18":{"Node 16":"Corridor 10a", "Node 3a":"Corridor 4a", "Node 24":"Corridor 11b", "Node 19":"Corridor 12b"},
    "Node 19":{"Node 18":"Corridor 12b", "Node 17":"Corridor 13a", "Node 21":"Corridor 12a", "Node 23":"Corridor 19b","Latin Stairs Ground":"Corridor GSLtn"},
    "Latin Stairs Ground":{"Node 19":"Corridor GSLtn"},
    "Node 20":{"Node 15":"Corridor 15a","Node 20x":"Corridor 15c","Node 20xb":"Corridor 16"},
    "Node 20xa":{"Node 20x":"Corridor 17x"},
    "Node 20xb":{"Node 20":"Corridor 16", "English Stairs Ground":"Corridor GSE"},
    "Node 20x":{"Node 20":"Corridor 15c","Node 20xa":"Corridor 17x","Node 17":"Corridor 15b","Node 21":"Corridor 17c"},
    "English Stairs Ground":{"Node 20xb":"Corridor GSE"},
    "Node 21":{"Node 20x":"Corridor 17c", "Node 19":"Corridor 12a", "Node 22":"Corridor 17b", "Dance Studio Stairs Ground":"Corridor GSDS"},
    "Dance Studio Stairs Ground":{"Node 27":"Corridor GSDS"},
    "Node 22":{"Node 21":"Corridor 17b", "Node 23":"Corridor 18a", "Node 25":"Corridor 17a", "Node 27":"Corridor 20"},
    "Node 23":{"Node 22":"Corridor 18a", "Node 24":"Corridor 18b", "Node 26":"Corridor 19a", "Node 19":"Corridor 19b"},
    "Node 24":{"Node 23":"Corridor 18b", "Node 18":"Corridor 11b", "Node 1":"Corridor 11a"},
    "Node 25":{"Node 22":"Corridor 17a", "Node 26":"Corridor 14a", "Node 25x":"Corridor 23b"},
    "Node 25x":{"Node 25":"Corridor 23b","Node 25xa":"Corridor 22", "Node 25xb":"Corridor 23a"},
    "Staff Dining Stairs Ground":{"Node 25x":"Corridor GSSD"},
    "Node 25xa":{"Node 25x":"Corridor 22"},
    "Node 25xb":{"Node 25x":"Corridor 23a"},
    "Node 26":{"Node 25":"Corridor 14a", "Node 23":"Corridor 19a", "Node 1":"Corridor 14b"},
    "Node 26x":{"Node 26":"Corridor 14x"},
    "Node 27":{"Node 22":"Corridor 20","Node 27x":"Corridor 21"},
    "Node 27x":{"Node 27":"Corridor 21"},
    "Node 28":{"Node 28x":"Corridor 24","None":"Corridor 25"},
    "Node 28xb":{"Node 28":"Corridor 24"},
    "Node 28xa":{"Node 28":"Corridor 25x"},
    "Node 28xc":{"Node 28":"Corridor 25"}
    }

NodeCoords = {
    "Node 1":(-2068,-1426),
    "Reception Stairs Ground":(-2068,-1510), 
    "Node 1x":(-2068,-1608),
    "Node 2a":(-2705,-1426),
    "Node 2b":(-2845,-1426),
    "Library Stairs Ground":(-2775,-1426),
    "Node 2x":(-2705,-1629),
    "Node 3a":(-2705,-950),
    "Node 3b":(-2705,-901),
    "Language Stairs Ground":(-2705,-862),
    "Node 4":(-2845,-901),
    "Node 4x":(-3034,-901),
    "Node 5":(-2845,-789),
    "History Stairs Ground":(-2845,-705),
    "Node 5xa":(-3034,-705),
    "Node 5xb":(-2908,-705),
    "Node 6":(-2705,-789),
    "Node 7":(-2509,-789),
    "Node 8":(-2908,-579),
    "Node 9":(-2705,-579),
    "Node 10":(-2509,-579),
    "Chemistry Stairs Ground":(-2579,-579),
    "Node 10x":(-2509,-404),
    "Node 11":(-2313,-579),
    "Node 12":(-2068,-579),
    "Node 13":(-1893,-579),
    "Bioligy Stairs Ground":(-1956,-579),
    "Node 13x":(-1893,-404),
    "Node 14":(-1739,-579),
    "Node 15":(-1382,-579),
    "Art Stairs Ground":(-1522,-579),
    "Node 16":(-2068,-789),
    "Node 17":(-1739,-719),
    "Node 18":(-2068,-950),
    "Node 19":(-1739,-950),
    "Latin Stairs Ground":(-1886,-950),
    "Node 20":(-1382,-670),
    "Node 20xa":(-1235,-719),
    "Node 20xb":(-976,-670),
    "Node 20x":(-1382,-719), 
    "English Stairs Ground":(-927,-670),
    "Node 21":(-1382,-950),
    "Dance Studio Stairs Ground":(-906,-1244),
    "Node 22":(-1382,-1181),
    "Node 23":(-1739,-1181),
    "Node 24":(-2068,-1181),
    "Node 25":(-1382,-1426),
    "Staff Dining Stairs Ground":(-1382,-1580),
    "Node 25x":(-1382,-1503),
    "Node 25xa":(-976,-1503),
    "Node 25xb":(-1382,-1797),
    "Node 26":(-1739,-1426),
    "Node 26x":(-1739,-1580),
    "Node 27":(-906,-1181),
    "Node 27x":(-906,-1433),
    "Node 28":(-1578,-2098),
    "Node 28xb":(-878,-2098),
    "Node 28xa":(-1578,-1930),
    "Node 28xc":(-1578,-2308),
    }

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
    # total = 0
    # for node in distances:
    #     if node in path:
    #         total += distances[node]
    # return total
    #EITHER CODE ABOVE OR BELOW WORKS
    return int(reduce(lambda x,y: x+y,[distances[x] for x in path]))
    

def MainLoop(start_node=None,end_node=None):
    start_node,end_node = input("Give me a start and end node seperated by a comma").split(",")
    distances, path = dijkstra_recursive(graph, start_node, end_node)
    if path == ["Node 1"]:
            print("Node not reachable as of now")
    else:
            print(f"Shortest distances from {start_node}: {distances}")
            print(f"Shortest path from {start_node} to {end_node}: {path}")
            print(f"Total distance: {total_path_dist(distances,path)}")
            return(total_path_dist(distances,path))

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
            #print(NodeConnections[node][neighbournode]) #REMOVE
            if NodeConnections[node][neighbournode] == corridor:
                #print("https://integralmaths.org/") #REMOVE
                nodes.append(node)
                break
    return nodes

def findroomtocorridor(roomwhere):
    currentcorridor = 0
    currentroom = 0
    while True:
        try:
            roomsearch=stripper(currentcorridor,currentroom)[1:]
            if roomwhere == roomsearch:
                #print(f"{roomwhere}:{mapper[currentcorridor][0]}") #REMOVE
                #print(linkcorridortonode(mapper[currentcorridor][0])) #REMOVE
                return [roomwhere,mapper[currentcorridor][0],linkcorridortonode(mapper[currentcorridor][0])]
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

def min_dist(info):
    lowest_dist = 100000000
    distsandpath = {}
    for node_1 in info[0][2]:
        for node_2 in info[1][2]:
            distance,path = dijkstra_recursive(graph,node_1,node_2)
            distsandpath[f"{node_1}:{node_2}"] = [(total_path_dist(distance,path)+GroundFloorCorridorDists[info[0][1]]+GroundFloorCorridorDists[info[1][1]]),path]
    for corridor in distsandpath:
        if distsandpath[corridor][0] < lowest_dist:
            lowest_dist = distsandpath[corridor][0]
        print(f"{corridor}:{distsandpath[corridor]}")
    return [(key,distsandpath[key]) for key in distsandpath if distsandpath[key][0]==lowest_dist]

def decodepathofnodestocorridors(path,start,end):
    Cpath = [start]
    for node in range(len(path)-1):
        Cpath.append(NodeConnections[path[node]][path[node+1]])
    Cpath.append(end)
    return Cpath


mapper =list(GroundFloorNodesAndCorridors.items())
graph = {node:{neighbour_node:GroundFloorCorridorDists[NodeConnections[node][neighbour_node]] for neighbour_node in NodeConnections[node]} for node in NodeConnections}

def maincode():
    try:
        room1,room2 = input("Give me two rooms seperated by a comma").split(",")
    except ValueError:
        room1 = "G3"
        room2 = "G28"
    info = [] #room, corridor, node
    info.append(findroomtocorridor(room1))
    info.append(findroomtocorridor(room2))
    if info[0][1] == info[1][1]:
        print("in same corridor")
    else:
        mindist = min_dist(info)
        print(f"MinDist: {mindist[0][1][1]} of dist {mindist[0][1][0]}")
        print(f"Path: {decodepathofnodestocorridors(mindist[0][1][1],info[0][1],info[1][1])}")

while True:
    maincode()

