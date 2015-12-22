import math
from grapherUtils.utils import properLoop


#Reference to all of the operators
operators = "+-*/^"
#Reference to the ind symbols for 3D plotting
independentVar = "xy"
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
        ax = graphRange["xMin"] #starting X value
        bx = graphRange["xMax"] #ending X value
        ay = graphRange["xMin"] #starting Y value
        by = graphRange["xMax"] #ending Y value
        stepx = math.fabs(ax - bx) / resolution #increment value in the X direction
        stepy = math.fabs(ay - by) / resolution #increment value in the Y direction
        i = 0
        for d in properLoop(ay, by, stepy):
            stack[k].append([])
            ax = graphRange["xMin"] #Reset these values for the next iteration
            bx = graphRange["xMax"] 
            for e in properLoop(ax, bx, stepx):
                l = len(RPNStack[k])
                for j in range(0, l):
                    if (RPNStack[k][j].isdigit()):
                        stack[k][i].append(RPNStack[k][j])
                    #Catch the independent
                    elif (independentVar.find(RPNStack[k][j]) >= 0):
                        if (RPNStack[k][j] == "x"):
                            stack[k][i].append(ax)
                        if (RPNStack[k][j] == "y"):
                            stack[k][i].append(ay)
                    #if the current token is an operator
                    elif (operators.find(RPNStack[k][j]) >= 0):
                        one = float(stack[k][i].pop())
                        two = float(stack[k][i].pop())
                        if (RPNStack[k][j] == "+"):
                            stack[k][i].append(two + one)
                        elif (RPNStack[k][j] == "-"):
                            stack[k][i].append(two - one)
                        elif (RPNStack[k][j] == "*"):
                            stack[k][i].append(two * one)
                        elif (RPNStack[k][j] == "/"):
                            stack[k][i].append(two / one)
                        elif (RPNStack[k][j] == "^"):
                            stack[k][i].append(math.pow(two, one))
                    
                    elif (RPNStack[k][j] in functionOperators):
                        one = float(stack[k][i].pop())
                        if (RPNStack[k][j] == "sin"):
                            stack[k][i].append(math.sin(one))
                        elif (RPNStack[k][j] == "cos"):
                            stack[k][i].append(math.cos(one))
                        elif (RPNStack[k][j] == "tan"):
                            stack[k][i].append(math.tan(one))
                        elif (RPNStack[k][j] == "arctan"):
                            stack[k][i].append(math.atan(one))
                        elif (RPNStack[k][j] == "arcsin"):
                            stack[k][i].append(math.asin(one))
                        if (RPNStack[k][j] == "arccos"):
                            stack[k][i].append(math.acos(one))
                #Increment our value at the current points
                ax += stepx
            ay += stepy
        i = i + 1
    #print("parser", stack)
    return stack