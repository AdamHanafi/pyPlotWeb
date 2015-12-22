validCommands = {"history", "favorites", "help"}

def formatInput(query):
    query = query.lower()
    tokens = query.split(";")
    outputTokens = []
    for k in range(0, len(tokens)):
        #Only a single command is accepted
        if (tokens[k] in validCommands):
            outputType = "command"
            outputTokens = []
            return {"type": outputType, "functions": tokens[k]}
        else:
            outputTokens.append(tokens[k])
            outputType = "function"
    return {"type": outputType, "functions": outputTokens}
            