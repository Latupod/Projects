from math import inf
'''
Map = {"G1":[(),()],
       "G2":[(),()],
       "G3":[(),()],
       "G4":[(),()],
       "G5":[(),()],
       "G6":[(),()],
       "G7":[(),()],
       "G8":[(),()],
       "G9":[(),()],
       "G10":[(),()],
       "G11":[(),()],
       "G12":[(),()],
       "G13":[(),()],
       "G14":[(),()],
       "G15":[(),()],
       "G16":[(),()],
       "G17":[(),()],
       "G18":[(),()],
       "G19":[(),()],
       "G20":[(),()],
       "G21":[(),()],
       "G22":[(),()],
       "G23":[(),()],
       "G24":[(),()],
       "G25":[(),()],
       "G26":[(),()],
       "G27":[(),()],
       "G28":[(),()],
       "G29":[(),()],
       "G30":[(),()],
       "G31":[(),()],
       "G32":[(),()],
       "G33":[(),()],
       "G34":[(),()],
       "G35":[(),()],
       "G36":[(),()],
       "G37":[(),()],
       "G38":[(),()],
       "G39":[(),()],
       "G40":[(),()],
       "G41":[(),()],
       "G42":[(),()],
       "G43":[(),()],
       "G44":[(),()],
       "G45":[(),()],
       "G46":[(),()],
       "G47":[(),()],
       "G48":[(),()],
       "G49":[(),()],
       "G50":[(),()],
       "G51":[(),()],
       "G52":[(),()],
       "G53":[(),()],
       "G54":[(),()],
       "G55":[(),()],
       "G56":[(),()],
       "G57":[(),()],
       "G58":[(),()],
       "G59":[(),()],
       "G60":[(),()],
       "G61":[(),()],
       "G62":[(),()],
       "G63":[(),()],
       "G64":[(),()],
       "G65":[(),()],
       "G66":[(),()],
       "G67":[(),()],
       "G68":[(),()],
       "G69":[(),()],
       "G70":[(),()],
       "G71":[(),()],
       "G72":[(),()],
       "G73":[(),()],
       "G74":[(),()],
       "G74a":[(),()],
       "G75":[(),()],
       "G76":[(),()],
       "G77":[(),()],
       "G78":[(),()],
       "G79":[(),()],
       "G80":[(),()],
       "G81":[(),()],
       "G82":[(),()],
       "G83":[(),()],
       "G84":[(),()],
       "G85":[(),()],
       "G86":[(),()],
       "G87":[(),()],
       "G88":[(),()],
       "G89":[(),()],
       "G90":[(),()],
       "G91a":[(),()],
       "G91b":[(),()],
       "Headmaster's Study":[(),()],
       "Med Room":[(),()],
       "Main Hall":[(),()],
       "Hammond Theatre":[(),()],
       "Dining Hall":[(),()],
       "Sports Hall":[(),()],
       "Sports Pavillions":[(),()],
       "North Gym":[(),()],
       "Cloisters":[(),()],
       "M1":[(),()],
       "M2":[(),()],
       "M3":[(),()],
       "P1":[(),()],
       "P1":[(),()],
       "P1":[(),()],
       "P1":[(),()],
       "P2":[(),()],
       "P3":[(),()],
       "P4":[(),()],
       "P5":[(),()],
       "P6":[(),()],
       "P7":[(),()],
       "P8":[(),()],
       "P9":[(),()],
       "P10":[(),()],
       "P11":[(),()],
       "Practise Rooms":[(),()],
       "Main School Queue":[(),()],
}
'''

'''
Example Graph
graphs = 
        (
        {"A": {"B":30, "C":20},
        "B": {"A":30, "C":20, "E":60},
        "C": {"A":20, "B":20, "D":30},
        "D": {"C":30, "E":30},
        "E": {"B":60,"D":30} 
        },
        #"A",
        #"E"
        )
'''


PointsOfInterest = {"Stairs":["0Reception Stairs","3Stairs(To Language)","0Stairs(To Library)","0Barry Martin Stairs","2Stairs(To History)","7Stairs(To Latin)"],
            "Entrances": ["0Main Entrance","4Cloisters Entrance","0Atrium Entrance","9Lecture Theatre Entrance"],
            "Subject Offices": [["Maths Office","0G45"],["Physics Office","0G25"]],
            "Head Of Years": [["Third Year","0G44"],["First Year","7G53"]],
            "Toilets": ["9Toilets(History)","5Toilets(Atrium)","1Disabled Toilets(Cloisters)","2Toilets(Cloisters)",],
            }

CorridorsRoomsContainer = {"Reception":["0Reception Stairs","0Headmaster's Study","0G1","0G2","0Main Entrance"],
                            "Corridor 1":["2G3","3G4","3G5","4G6","4G7","6G8","7G9","8G10"],
                            "Corridor 2":["9G35","8G36","8G37","7G38","7G39","8G40","4Cloisters","2G91B","1G91A","0Medical Room","4Cloisters Entrance"], #change
                            "Corridor 2a":[], #new
                            "Corridor 2b":[], #new
                            "Corridor 3":["0G34","1G41","3G33","4G32","5Cloisters","5Main Hall"],#change
                            "Corridor 3a":[],
                            "Corridor 3b":[],
                            "Corridor 4a":["0G11","2G12","3G13","4G14","6G15","8G16","9G17","6Barry Martin Centre"],
                            "Corridor 4b":["2Chess Courtyard","3Stairs(To Language)","0Atrium Entrance"],
                            "Corridor 5":["0G25","3G24","7G23","8G18","7Barry Martin Centre"],
                            "Corridor 6":["1Disabled Toilets(Cloisters)","2Toilets(Cloisters)","7Stairs(To Latin)","8G26"],#change
                            "Corridor 6a":[],
                            "Corridor 6b":[],
                            "Corridor 6x":[],
                            "Corridor 7":["0Lecture Theatre","2Stairs(To History)","3G51","5G52","7G53","9G51","9Toilets(History)","9Changing Rooms"],
                            "Corridor 8":[],
                            "Corridor 9":[],
                            "Corridor 10":[],
                            "Corridor 11":[],
                            "Corridor 12":[],
                            "Corridor 12x":[],#empty
                            "Corridor 13":[],
                            "Corridor 14":[],
                            "Corridor 15":[],
                            "Corridor 15a":[],#empty
                            "Corridor 15b":[],#empty
                            "Corridor 15c":[],#empty
                            "Corridor 15d":[],#empty
                            "Corridor 16":[],
                            "Corridor 16x":[],#empty
                            "Corridor 17":[],
                            "Corridor 18":[],
                            "Corridor 19":[],
                            "Corridor 20":[],
                            "Corridor 21":[],
                            "Atrium":["0Stairs(To Library)","0G45","0G44","0G45","9Lecture Theatre Entrance","5Toilets(Atrium)",],
                            "Barry Martin Centre":["0Barry Martin Stairs","0G21"]
                                }

GroundFloorCorridorDists = {"Reception":2,
                            "Corridor 1":10,
                            "Corridor 2a":5,
                            "Corridor 2b":5,
                            "Corridor 3a":5,
                            "Corridor 3b":5, 
                            "Corridor 4a":10,
                            "Corridor 4b":1,
                            "Corridor 5":10,
                            "Corridor 6a":5,
                            "Corridor 6b":5,
                            "Corridor 6x":3,
                            "Corridor 7":4,
                            "Corridor 8":6,
                            "Corridor 9":5,
                            "Corridor 10":3,
                            "Corridor 11":5,
                            "Corridor 12":2,
                            "Corridor 12x":3,
                            "Corridor 13":5,
                            "Corridor 14":6,
                            "Corridor 15":6,
                            "Corridor 15a":5,
                            "Corridor 15b":4,
                            "Corridor 15c":5,
                            "Corridor 15d":4,
                            "Corridor 16":5,
                            "Corridor 17":5,
                            "Corridor 18":6,
                            "Corridor 19":5,
                            "Corridor 20":3,
                            "Corridor 21":7,
                            "Atrium":10,
                            "Barry Martin Centre":inf
                                }

GroundFloorNodesAndCorridors = {"Node 1": ["Reception","Corridor 1","Corridor 2b","Corridor 3a",],
                                "Node 1x":["Corridor 15a","Corridor 3a","Corridor 3b"],
                                "Node 2": ["Corridor 1","Corridor 4a","Atrium",],
                                "Node 3": ["Corridor 4a","Corridor 5","Corridor 4b",],
                                "Node 4": ["Corridor 4b","Atrium","Corridor 7",],
                                "Node 5": ["Corridor 7","Corridor 8",],
                                "Node 6": ["Corridor 8","Corridor 9",],
                                "Node 7": ["Corridor 9","Corridor 10",],
                                "Node 8": ["Corridor 9","Corridor 11",],
                                "Node 9": ["Corridor 11","Corridor 6x",],
                                "Node 9x":["Corridor 6x","Corridor 6a","Corridor 6b","Corridor 15b",],
                                "Node 10": ["Corridor 10","Corridor 5","Corridor 6b","Corridor 3b",],
                                "Node 11": ["Corridor 11","Corridor 12",],
                                "Node 12": ["Corridor 12","Corridor 13","Corridor 12x",],
                                "Node 12x": ["Corridor 12x","Corridor 15","Corridor 6a"],
                                "Node 13": ["Corridor 15","Corridor 16","Corridor 14","Corridor 15c",],
                                "Node 14": ["Corridor 14","Corridor 2a","Corridor 18","Corridor 19",],
                                "Node 14x":["Corridor 2a","Corridor 2b","Corridor 15d"],
                                "Node 15": ["Corridor 16x","Corridor 2","Corridor 6","Corridor 3",],
                                "Node 16": ["Corridor 16","Corridor 17"],
                                "Node 17":["Corridor 20","Corridor 21",]
                                #"Node Barry": ["Corridor 5","Corridor 4a"]
                                }
NodeConnections = {
    "Node 1": {"Node 2":"Corridor 1", "Node 1x":"Corridor 3a", "Node 14x":"Corridor 2b"},
    "Node 1x":{"Node 1":"Corridor 3a", "Node 15":"Corridor 15a", "Node 10":"Corridor 3b"},
    "Node 2": {"Node 1":"Corridor 1", "Node 3":"Corridor 4a", "Node 4": "Atrium"},
    "Node 3": {"Node 2":"Corridor 4a", "Node 4":"Corridor 4b", "Node 10":"Corridor 5"},
    "Node 4": {"Node 3":"Corridor 4b", "Node 2":"Atrium","Node 5":"Corridor 7"},
    "Node 5": {"Node 4":"Corridor 7", "Node 6":"Corridor 8"},
    "Node 6": {"Node 5":"Corridor 8", "Node 7":"Corridor 9"},
    "Node 7": {"Node 6":"Corridor 9", "Node 8":"Corridor 9", "Node 10":"Corridor 10"},
    "Node 8": {"Node 7":"Corridor 9", "Node 11":"Corridor 11", "Node 9":"Corridor 11"},
    "Node 9": {"Node 11":"Corridor 11", "Node 8":"Corridor 11", "Node 9x":"Corridor 6x"},
    "Node 9x":{"Node 10":"Corridor 6b", "Node 15":"Corridor 15b", "Node 9":"Corridor 6x", "Node 12x":"Corridor 6a"},
    "Node 10": {"Node 1x":"Corridor 3b", "Node 7":"Corridor 10", "Node 3":"Corridor 5", "Node 9x":"Corridor 6b"},
    "Node 11": {"Node 8":"Corridor 11", "Node 9":"Corridor 11", "Node 12":"Corridor 12"},
    "Node 12": {"Node 13x":"Corridor 13", "Node 12x":"Corridor 15x", "Node 11":"Corridor 12"},
    "Node 12x": {"Node 12":"Corridor 12x", "Node 13":"Corridor 15", "Node 9x":"Corridor 6a"},
    "Node 13": {"Node 12x":"Corridor 15", "Node 14":"Corridor 14", "Node 16":"Corridor 16", "Node 15":"Corridor 15c"},
    "Node 14": {"Node 14x":"Corridor 2a", "Node 13":"Corridor 14"},
    "Node 14x":{"Node 1":"Corridor 2b", "Node 15":"Corridor 15d", "Node 14":"Corridor 2a"},
    "Node 15": {"Node 1x":"Corridor 15a", "Node 14x":"Corridor 15d", "Node 9x":"Corridor 15b", "Node 13":"Corridor 15c"},
    "Node 16":{"Node 13":"Corridor 16"},
    "Node 17":{},
    #"Node Barry": {},
    }

GroundFloorGroups = {"Main Building": [()],
                     "M Block": [()],
                     "Sports Hall": [()],
                     "Sports Pavillion": [()],
                     "Garrick Centre": [()],
                     }

#Testing Graphs With Dijkstra:
#NodeConnections is the main map connecting node to node with corridors as distances
#GroundFloorCorridorDists is the mapping distances for each key 


def dijkstra(NodeConnections,GroundFloorCorridorDists,start,end):
    unvisited = []
    distances = NodeConnections.copy()
    for node in NodeConnections:
        unvisited.append(node)
        distances[node] = [inf,None] #distances and previous node
    distances[start] = [0,None]
    
    current_node = start
    closest_node = ""
    print(f"Searching for: {end}, Starting at: {start}")
    while unvisited :
        print(f"Unvisited nodes: {unvisited}")
        if (current_node in unvisited):
            unvisited.remove(current_node) #current node visited so remove
        print(f"Current node: {current_node}")
        print(f"Current node looking at: {NodeConnections[current_node]}")
        for node in NodeConnections[current_node]: #checking each connected node to current node
            print(f"SubNodes checking: {node}")
            distance_to_current_node = GroundFloorCorridorDists[NodeConnections[current_node][node]] #distance from current node to node bieng checked
            if (distances[current_node][0] + distance_to_current_node) < (distances[node][0]):
                distances[node] = [(distances[current_node][0] + distance_to_current_node) , current_node] #distance from "start" to current node
            if (node in unvisited) and (((closest_node == "")) or ((distance_to_current_node < GroundFloorCorridorDists[NodeConnections[current_node][closest_node]]))):
                closest_node = node #closest node is the current closest node from the current node
        print(f"NB: {closest_node}")
        current_node = closest_node
        closest_node = ""
        
    path = []
    current_node = end
    while (start not in path) or (end not in path):
        path.append(current_node)
        current_node = distances[current_node][1]
    path = path[::-1]
    return path

'''
userinput = input()
while userinput != "q":
    userstart,userend = input("Start and End pls split with a comma").split(",")
    print(dijkstra(NodeConnections,GroundFloorCorridorDists,userstart,userend))
    userinput = input()'
'''
#Test Input:
print(print(dijkstra(NodeConnections,GroundFloorCorridorDists,"Node 1","Node 2")))