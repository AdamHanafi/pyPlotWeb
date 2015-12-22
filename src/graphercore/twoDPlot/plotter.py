from grapherUtils.utils import clampNumber

def getVerticalPoint(point, rangeObj, canvasSize):
    yVal = 0
    #Clamp the values so that large values do not cause visual issue for the client
    clampPoints = {
                   "min": -100000,
                   "max": 100000
                   }
    #Point is above yMax
    if ((point - rangeObj["yMax"]) > 1 ):
        yVal = ((point - rangeObj["yMax"]) / (rangeObj["yMax"] - rangeObj["yMin"]) * -canvasSize["height"] )
    
    #point is below yMin
    if ((point - rangeObj["yMin"]) < -1):
        yVal = (-1 * ((point - rangeObj["yMin"]) / (rangeObj["yMax"] - rangeObj["yMin"]) * canvasSize["height"]) + canvasSize["height"])
    
    #Point must be in range
    else:
        yVal = ((canvasSize["height"] / 2) - (point / (rangeObj["yMax"] - rangeObj["yMin"]) * canvasSize["height"]))
    
    return clampNumber(yVal, clampPoints["min"], clampPoints["max"])

def createPlots(rangeObj, plots, canvasSize, colors):
    #this will hold our path strings
    functionLines = []
    n = len(plots)
    for k in range (0, n):
        functionLines.append({
                              "path": "",
                              "attr": {}
                            })
        l = len(plots[k])
        tempPath = ""
        for j in range(0, l):
            #print(j)
            #Initial point
            if (j == 0):
                if ((isinstance(plots[k][j], float)) | isinstance(plots[k][j], int)):
                    vertPoint = getVerticalPoint(plots[k][j], rangeObj, canvasSize)
                    tempPath = "M " + str((j / l) * float(canvasSize["width"])) + " " + str(vertPoint)
            #All other points
            else:
                if ((isinstance(plots[k][j], float)) | isinstance(plots[k][j], int)):
                    vertPoint = getVerticalPoint(plots[k][j], rangeObj, canvasSize)
                    tempPath += " L " + str((j / l) * float(canvasSize["width"])) + " " + str(vertPoint)

            #print(" L " + str((j / l) * float(canvasSize["width"])) + " " + str(vertPoint))
        
        functionLines[k]["path"] = tempPath
        #The colors will wrap to the beginning should there not be enough
        functionLines[k]["attr"] = {
                                 "stroke": colors[k % len(colors)]
                                 }
    #print("functionLines", functionLines)
    return functionLines
        