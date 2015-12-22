
def formatData(data, delta, start):
    result = []
    
    for a in range(0, len(data["stack"][0])):
        result.append([(a * delta) + start])
        
    for k in range(0, len(data["stack"])):
        for j in range(0, len(data["stack"][k])):
            
            result[j].append(data["stack"][k][j])#.append([j, data["stack"][k][j]])
    return result


def getColumns(data):
    result = []
    result.append({
                   "dataKey": 0,
                   "headerText": "X",
                   })
    for k in range(0, len(data["stack"])):
        result.append({
                       "dataKey": k + 1,
                       "headerText": "f" + str(k)
                       })
    return result