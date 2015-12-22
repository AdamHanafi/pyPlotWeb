from grapherUtils.utils import clampNumber

def getMaxMin(plots, rangeObj):
    minVal = 0
    maxVal = 0
    for k in range (0, len(plots)):
        for n in range(0, len(plots[k])):
            if (plots[k][n] > maxVal):
                maxVal = plots[k][n]
            if (plots[k][n] < minVal):
                minVal = plots[k][n]
    return {
            "max": clampNumber(maxVal, rangeObj["zMin"], rangeObj["zMax"]),
            "min": clampNumber(minVal, rangeObj["zMin"], rangeObj["zMax"])
            }

def pointInRange(value, rangeObj):
    if ((value - rangeObj["zMin"]) < -1):
        return False
    if ((value - rangeObj["zMax"]) > 1 ):
        return False
    return True

#Normalize the z value from 0 to 1 based on its value relative to zMin/zMax
def normalizeZ(z, rangeObj):
    #normalizedVal = clampNumber( ((z - rangeObj["zMin"]) / (rangeObj["zMax"] - rangeObj["zMin"])) - 0.5, 0, 1)
    normalizedVal = ((z - rangeObj["zMin"]) / (rangeObj["zMax"] - rangeObj["zMin"])) - 0.5
    #print(z,"\t",normalizedVal)
    return normalizedVal


def createPlots(rangeObj, plots, colors, resolution):
    result = {
              "vectors": [],
              "minMax": []
              }
    
    yInterval = (rangeObj["yMax"] - rangeObj["yMin"]) / resolution
    xInterval = (rangeObj["xMax"] - rangeObj["xMin"]) / resolution
    #For each function
    for k in range(0, len(plots)):
        result["vectors"].append([])
        result["minMax"].append([])
        maxMin = getMaxMin(plots[k], rangeObj)
        result["minMax"][k].append({
                                    "min": maxMin["min"],
                                    "max": maxMin["max"]
                                    })
        #For each row
        for n in range(0, len(plots[k])):
            #For each element in the row
            for l in range(0, len(plots[k][n])):
                #if (pointInRange(plots[k][n][l], rangeObj)):
                zVal = ((plots[k][n][l] - rangeObj["zMin"]) / (rangeObj["zMax"] - rangeObj["zMin"]) * 20)
                normalizedZVal = normalizeZ(zVal, rangeObj)
                #result["colors"][k].append(getVertexColor(normalizedZVal, maxMin, colors))
                result["vectors"][k].append([xInterval * l, yInterval * n, normalizedZVal])
    return result
        