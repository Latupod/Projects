#NECA
INPUT_LIST = {
    
    "NECA_INPUTS": ["InV","FinV","Mass","Time","Accelleration","Displ","Angle"] #using d as displacement for simplicity of entry

}
g = 9.81 #freefall

def NECA_input(TYPE_INPUTS):
    valid = False
    addto = "" 
    Cache = []
    Calling = INPUT_LIST[TYPE_INPUTS]
    
    for INPUT in Calling:
        addto += INPUT
        
    print ("These are following possible inputs for the selected calculation: " , addto)
    print("Please enter values for each variable, type question mark if variable is unknown")

    for INPUT in Calling:
        Cache.append([(input(INPUT + ": ")),(INPUT)])
    for item in range(len(Cache)):
        NECA_confirm(Cache,item)

    NECA_Calc(Cache)

def NECA_confirm(Cache,item):
    term_val = Cache[item][0]
    term = Cache[item][1]
    confirm = input("You have entered " + term + " as " + term_val + ". Is this correct, type y or n: ")
    if confirm == "n":
        Cache[item][0] = input("Changing " + term + " to: ")
    elif confirm != "y":
        print("please enter valid answer")
        NECA_confirm(Cache,item)
    else:
        return None
            
def NECA_Calc(Cache):
    #formula_options = [["InV","FinV","Displacement","Accelleration"],["InV","Time","Displacement","Accelleration"],["FinV","Time","Displacement","Accelleration"],["InV","FinV","Time","Accelleration"],["InV","FinV","Time","Displacement"]]
    formula_valid = []
    
    #toFind = [term[1] for term in Cache if term[0] == 0]
    toFind = list(filter(lambda x: x[0]=="?",Cache))
    print("Variables to found: " + toFind)
    
    if len(toFind) > 2:
        print("Given variables cannot be found with given information")
        return None
    
    #for formula in formula_options:
    #    for var in formula:
    #        if var in toFind:
    #            formula.remove(var)
    #    if len(formula) >= 3:
    #        formula_valid.append(formula_options.index(formula))

    #xtx

#
TYPE = input("What calculation are you doing: NECA , Force Diagram")
NECA_input((TYPE + "_INPUTS"))