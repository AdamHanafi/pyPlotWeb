import math
from grapherUtils.utils import properLoop

#Reference to all of the operators
operators = "+-*/^"
#Reference to the ind symbols for 2D plotting
independentVar = "x"
#Reference to the functional operators
functionOperators = {"sin", "cos", "tan", "arctan", "arcsin", "arccos"}

def getValues(rpnStack, optionsObj):
    n = len(rpnStack)
    #Holds the current stack with which we solve for each x value. 
    #This is a progressive stack, in that all final values are held here along
    #with the intermediate results of the current value of x
    result = {
              "stack": [],
              "labels": []
              }

    

    for k in range(0, n):
        result["stack"].append([])
        a = optionsObj["start"] #starting value
        b = optionsObj["delta"] * 19 #ending value
        step = optionsObj["delta"] #increment value for the loop
        for d in properLoop(a, b, step):
            l = len(rpnStack[k])
            if (k == 0):
                result["labels"].append(a)
            for j in range(0, l):
                if (rpnStack[k][j].isdigit()):
                    result["stack"][k].append(rpnStack[k][j])
                #Catch the independent
                elif (independentVar.find(rpnStack[k][j]) >= 0):
                    result["stack"][k].append(a)
                #if the current token is an operator
                elif (operators.find(rpnStack[k][j]) >= 0):
                    one = float(result["stack"][k].pop())
                    two = float(result["stack"][k].pop())
                    if (rpnStack[k][j] == "+"):
                        result["stack"][k].append(two + one)
                    elif (rpnStack[k][j] == "-"):
                        result["stack"][k].append(two - one)
                    elif (rpnStack[k][j] == "*"):
                        result["stack"][k].append(two * one)
                    elif (rpnStack[k][j] == "/"):
                        result["stack"][k].append(two / one)
                    elif (rpnStack[k][j] == "^"):
                        result["stack"][k].append(math.pow(two, one))
                
                elif (rpnStack[k][j] in functionOperators):
                    one = float(result["stack"][k].pop())
                    if (rpnStack[k][j] == "sin"):
                        result["stack"][k].append(math.sin(one))
                    elif (rpnStack[k][j] == "cos"):
                        result["stack"][k].append(math.cos(one))
                    elif (rpnStack[k][j] == "tan"):
                        result["stack"][k].append(math.tan(one))
                    elif (rpnStack[k][j] == "arctan"):
                        result["stack"][k].append(math.atan(one))
                    elif (rpnStack[k][j] == "arcsin"):
                        result["stack"][k].append(math.asin(one))
                    if (rpnStack[k][j] == "arccos"):
                        result["stack"][k].append(math.acos(one))
            #Increment our value at the current points
            a += step
    #print("parser", stack)
    return result