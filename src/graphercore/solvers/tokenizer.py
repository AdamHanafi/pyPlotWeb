#This module is responsible for breaking a query up into tokens

decimalDelim = "."
symbols = "+-*/^()"
functionalOperators = {"sin", "cos", "tan", "arctan", "arcsin", "arccos"}

#We will parse this statement character by character
def parseToken(query):
    
    independents = {
                "x": False,
                "y": False
                }
    
    tempContainer = ""
    tokens = []
    #Keep track of how many independents we have
    dimension = 1
    currentType = "" #Holds the current token type when going character by character
    for a in range(0, len(query)):
        #Make everything lower case
        query[a] = query[a].lower()
        query[a] = query[a].replace(" ", "") #Remove all spaces
        
        tokens.append([])
        n = len(query[a])
        for k in range(0, n):
            if (not currentType == "char"):
                tempContainer = ""
            if (query[a][k].isdigit()):
                currentType = "number"
                tempContainer += query[a][k]
                #First, check of we reached the end of the list
                if (k + 1 != n):
                    #Check for the next character
                    if (query[a][k + 1].isdigit() == False):
    
                        if (query[a][k + 1] == decimalDelim):
                            print("contains decimals")
                        tokens[a].append(tempContainer)
                        tempContainer = ""
                
                #If we did reach the end, append all that may be left in 
                else:
                    tokens[a].append(tempContainer)
            #check for symbols
            elif (symbols.find(query[a][k]) >= 0):
                tokens[a].append(query[a][k])
            
            #check for the independent variables
            elif (query[a][k] in independents):
                independents[query[a][k]] = True #mark the ind as used
                tokens[a].append(query[a][k])
                
            else:
                currentType = "char"
                tempContainer += query[a][k]
                if (tempContainer in functionalOperators):
                    tokens[a].append(tempContainer)
                    tempContainer = ""
        
    
    if (independents["x"]):
        dimension += 1 
        
    if (independents["y"]):
        dimension += 1
        
    #If no independent has been specified, assume it is 2
    if (dimension == 1):
        dimension += 1
    print("tokens", tokens)
    return {
             "tokens": tokens,
             "dimension": dimension
             }