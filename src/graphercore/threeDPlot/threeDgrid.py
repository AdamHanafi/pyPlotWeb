import math
from grapherUtils.utils import isNumBetween


def generateGrid(rangeObj, options):
    result = {
              "xy": [],
              "yz": [],
              "xz": [],
              "color": options["color"],
              "lineWidth": options["lineWidth"]
              }
    cellSize = options["cellSize"]
    #Create the x-y grid first
    for k in range(0, 21):
        result["xy"].append([ [0, k * cellSize, 0], [20 * cellSize, k * cellSize, 0] ])
        result["xy"].append([ [k * cellSize, 0, 0], [k * cellSize, 20 * cellSize, 0] ])
        
    #Create the y-z grid
    for k in range(0, 21):
        result["yz"].append([ [0, k * cellSize, 0], [0, k * cellSize, 20 * cellSize] ])
        result["yz"].append([ [0, 0, k * cellSize], [0, 20 * cellSize, k * cellSize] ])
        
    #Create the x-z grid first
    for k in range(0, 21):
        result["xz"].append([ [0, 20 * cellSize, k * cellSize], [20 * cellSize, 20 * cellSize, k * cellSize] ])
        result["xz"].append([ [k * cellSize, 20 * cellSize, 0], [k * cellSize, 20 * cellSize, 20 * cellSize] ])
    
    return result
        
        