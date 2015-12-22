import copy

defaultOptions = {
                   "start": 0,
                   "delta" : 1
                   }

def getDefault():
    return defaultOptions

def combineOptions(newOptions):
    finalOptions = copy.deepcopy(defaultOptions)
    for k in defaultOptions:
        if (k in newOptions):
            if (not(newOptions[k] == None)):
                finalOptions[k] = newOptions[k]
    
    return finalOptions