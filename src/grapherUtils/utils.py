
#Define a useful loop pattern
def properLoop(start, end, step):
    while start <= end:
        yield start
        start += step

#Returns true if number is in between the bounds
def isNumBetween(ref, lowerBound, upperBound):
    if ((ref > lowerBound) & (ref < upperBound)):
        return True
    else:
        return False
    
#Clamps a number between the bounds
def clampNumber(num, lowerBound, upperBound):
    return max(lowerBound, min(num, upperBound))