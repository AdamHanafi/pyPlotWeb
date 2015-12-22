import math
from grapherUtils.utils import isNumBetween


def generateGrid(rangeObj, canvasSize):
    xInterval = canvasSize["width"] / 20
    yInterval = canvasSize["height"] / 20
    gridPaths = []
    tempString = ""
    #Create the vertical grid lines
    for k in range(0, 20):
        tempString += "M" + str(xInterval * k) + " 0" + "V" + str(canvasSize["height"])
        gridPaths.append({
                          "path": tempString,
                          "attr": {
                                   "opacity": "0.5",
                                   "stroke-width": "1px"
                                   }
                          })
        tempString = ""
    #Create the horizontal grid lines
    for k in range(0, 20):
        tempString += "M 0 " + str(yInterval * k) + "H" + str(canvasSize["width"])
        gridPaths.append({
                          "path": tempString,
                          "attr": {
                                   "opacity": "0.5",
                                   "stroke-width": "1px"
                                   }
                          })
        tempString = ""
    
    #Create major axes if needed
    if (isNumBetween(0, rangeObj["xMin"], rangeObj["xMax"])):
        tempString += "M" + str(math.fabs(xInterval * rangeObj["xMin"])) + " 0 V" + str(canvasSize["height"])
        gridPaths.append({
                          "path": tempString,
                          "attr": {
                                   "opacity": "1"
                                   }
                          })
        tempString = ""
    if (isNumBetween(0, rangeObj["yMin"], rangeObj["yMax"])):
        tempString += "M 0 " + str(math.fabs(yInterval * rangeObj["yMin"])) + " H " + str(canvasSize["width"])
        gridPaths.append({
                          "path": tempString,
                          "attr": {
                                   "opacity": "1"
                                   }
                          })
        tempString = ""
    #print("grid", gridPaths)
    return gridPaths
        