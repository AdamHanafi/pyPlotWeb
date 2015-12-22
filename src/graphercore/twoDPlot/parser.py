import math
from grapherUtils.utils import properLoop


#Reference to all of the operators
operators = "+-*/^"
#Reference to the ind symbols for 2D plotting
independentVar = "x"
#Reference to the functional operators
functionOperators = {"sin", "cos", "tan", "arctan", "arcsin", "arccos"}

#range - the range for the graph
#stack - the RPN stack
#resolution - the number of points to plot on the range
def getPlots(graphRange, RPNStack, resolution):
    n = len(RPNStack)
    #Holds the current stack with which we solve for each x value. 
    #This is a progressive stack, in that all final values are held here along
    #with the intermediate results of the current value of x
    stack = []
    

    for k in range(0, n):
        stack.append([])
        a = graphRange["xMin"] #starting value
        b = graphRange["xMax"] #ending value
        step = math.fabs(a - b) / resolution #increment value for the loop
        for d in properLoop(a, b, step):
            l = len(RPNStack[k])
            for j in range(0, l):
                if (RPNStack[k][j].isdigit()):
                    stack[k].append(RPNStack[k][j])
                #Catch the independent
                elif (independentVar.find(RPNStack[k][j]) >= 0):
                    stack[k].append(a)
                #if the current token is an operator
                elif (operators.find(RPNStack[k][j]) >= 0):
                    one = float(stack[k].pop())
                    two = float(stack[k].pop())
                    if (RPNStack[k][j] == "+"):
                        stack[k].append(two + one)
                    elif (RPNStack[k][j] == "-"):
                        stack[k].append(two - one)
                    elif (RPNStack[k][j] == "*"):
                        stack[k].append(two * one)
                    elif (RPNStack[k][j] == "/"):
                        stack[k].append(two / one)
                    elif (RPNStack[k][j] == "^"):
                        stack[k].append(math.pow(two, one))
                
                elif (RPNStack[k][j] in functionOperators):
                    one = float(stack[k].pop())
                    if (RPNStack[k][j] == "sin"):
                        stack[k].append(math.sin(one))
                    elif (RPNStack[k][j] == "cos"):
                        stack[k].append(math.cos(one))
                    elif (RPNStack[k][j] == "tan"):
                        stack[k].append(math.tan(one))
                    elif (RPNStack[k][j] == "arctan"):
                        stack[k].append(math.atan(one))
                    elif (RPNStack[k][j] == "arcsin"):
                        stack[k].append(math.asin(one))
                    if (RPNStack[k][j] == "arccos"):
                        stack[k].append(math.acos(one))
            #Increment our value at the current points
            a += step
    #print("parser", stack)
    return stack