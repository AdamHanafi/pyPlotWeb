import copy

defaultOptions = {
                    "colors": [
                                "#FF0000",
                                "#0000FF",
                                "#00FF00",
                                "#000000"
                               ],
                    "rangeObj": {
                                 "xMin": -10,
                                 "xMax": 10,
                                 "yMin": -10,
                                 "yMax": 10
                               },
                    "canvasSize": {
                                "height": 500.0,
                                "width": 500.0
                                   }
                  }

def getDefault():
    return defaultOptions

def combineOptions(newOptions):
    finalOptions = copy.deepcopy(defaultOptions)
    for k in defaultOptions:
        if (k in newOptions):
            for j in defaultOptions[k]:
                if (j in newOptions[k]):
                    if (not(newOptions[k][j] == None)):
                        finalOptions[k][j] = newOptions[k][j]
    
    return finalOptions