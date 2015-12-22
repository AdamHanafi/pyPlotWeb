from sympy import *

global X
global Y
X = symbols("x")
Y = symbols("y")

#format a string to latex
def formatToLatex(functions):
    if (isinstance(functions, list)):
        output = []
        for k in range(0, len(functions)):
            output.append(
                          {
                           "rawText": functions[k],
                           "formatted": latex(functions[k]),
                           "label": "f" + str(k)
                           })
    else: 
        output = latex(functions)
    return output


def getDerivative(functions):
    output = []
    for k in range(0, len(functions)):
        rawResult = str(diff(functions[k], X)).replace("**", "^")
        formattedResult = formatToLatex(diff(functions[k], X))
        output.append({
                       "rawText": str(rawResult),
                       "formatted": formattedResult,
                       "label": "f" + str(k)
                       })
    return output
    
def getIntegral(functions):
    output = []
    for k in range(0, len(functions)):
        rawResult = str(integrate(functions[k], X)).replace("**", "^")
        formattedResult = formatToLatex(integrate(functions[k], X))
        output.append({
                       "rawText": str(rawResult),
                       "formatted": formattedResult,
                       "label": "f" + str(k)
                       })
    return output
    
    
    