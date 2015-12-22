#This module converts function tokens into a postfix notation stack

#hold the precedence values for each operator
precedence = {
              "+": 2,
              "-": 2,
              "*": 3,
              "/": 3,
              "^": 4
}

association = {
            "+": "left",
            "-": "left",
            "/": "left",
            "*": "left",
            "^": "right"
}

independents = "xy"

functionOperators = {"sin", "cos", "tan", "arctan", "arcsin", "arccos"}

def toRPN(tokens):
    stack = []
    for a in range(0 ,len(tokens)):
        stack.append([])
        operatorStack = []
        op1 = None
        op2 = None
        for k in range(0, len(tokens[a])):
            #Check if the token is a number or an independent variable
            if ( (tokens[a][k].isdigit()) | (independents.find(tokens[a][k]) >= 0) ):
                stack[a].append(tokens[a][k])
            
            #We're just checking to see if the current token is an operator. We will compare against precedence for consistency
            elif (tokens[a][k] in precedence):
                #Use a flag to avoid having to catch a bunch of exceptions caused by non-existent object indexes
                skipWhile = False
                stackIndex = 1
                op1 = tokens[a][k]
                try:
                    op2 = operatorStack[len(operatorStack) - 1]
                    if (not(op2 in precedence)):
                        skipWhile = True
                except IndexError: 
                    op2 = ""
                    skipWhile = True
                    
                if (skipWhile == False):
                    while ( (precedence[op2]) & (association[op1] == "left") & (precedence[op1] <= precedence[op2]) | (association[op1] == "right") & (precedence[op1] < precedence[op2]) ):
                        stack[a].append(op2)
                        operatorStack.pop()
                        stackIndex += 1
                        try:
                            op2 = operatorStack[len(operatorStack) - 1]
                        except IndexError:
                            break
                operatorStack.append(op1)
            
            elif (tokens[a][k] == "("):
                operatorStack.append(tokens[a][k])
            elif (tokens[a][k] ==")"):
                stackIndex = 1
                while (operatorStack[len(operatorStack) - 1] != "("):
                    stack[a].append(operatorStack.pop())
                    
                #The "(" token at the end is simply discarded
                operatorStack.pop()
                
                #Check to see if the preceding token is a function operator, if so put it to the output
                if (len(operatorStack) >= 1):
                    if (operatorStack[-1] in functionOperators):
                        stack[a].append(operatorStack.pop())
                
            elif (tokens[a][k] in functionOperators):
                operatorStack.append(tokens[a][k])
            skipWhile = False
    
        while (len(operatorStack) > 0):
            stack[a].append(operatorStack.pop())
    
    print("RPNStack", stack)
    return stack
    