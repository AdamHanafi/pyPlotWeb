import json
import threading
from graphercore.queryManagement import inputFormatter
from graphercore.queryManagement import commandInterpreter
from graphercore.solvers import tokenizer
from graphercore.solvers import postfix
from graphercore.twoDPlot import plotter
from graphercore.twoDPlot import parser
from graphercore.twoDPlot import grid
from graphercore.twoDPlot import twoDDefaults

from graphercore.threeDPlot import threeDparser
from graphercore.threeDPlot import threeDgrid
from graphercore.threeDPlot import threeDplotter

from graphercore.table import rangeSolver
from graphercore.table import wijmoFormatting
from graphercore.table import tableDefaults

from graphercore.sympySolver import symPySolver
from mongodriver import * 

def formatResponse(rawResponse):
    return (bytes(json.dumps(rawResponse), "utf-8"))

def login(request):
    loginStatus = loginUser(request["username"], request["password"])
    return (formatResponse(loginStatus))


def createAccount(request):
    print(request)
    #Check if the password and the confirmation are equal
    if (request["password"] != request["passwordConfirm"]):
        response = {
                    "success": False,
                    "message": "Passwords do not match!"
                    }
        return formatResponse(response)
    
    #If the passwords match, continue
    response = registerUser(request["username"], request["password"])
    
    return formatResponse(response)
    
#Login a previously authenticated user without a password
#TODO: Add IP address check
#TODO: Better still, create an unique ID for each user which is to be stored
#on the browser instead of the username for security reasons
def loginNoPassword(request):
    validSession = checkUserSession(request["username"])
    if (validSession == False):
        response = {"success": "false", "message": "Your session has expired, please log in again"}
    else:
        updateLastAction(request["username"])
        response = {"success": "true"}
        
    return formatResponse(response)
    
    
def deleteHistoryItem(request):
    deleteSingleHistoryItem(request["username"], request["index"])
    #Run a new request through the interpreter, the front-end expects an entirely new list
    return formatResponse(commandInterpreter.parseCommand("history", request["username"]))

def updateControl(request):
    response = {}
    
    #Update the table
    if (request["control"] == "table"):
        lastQuery = getLastHistoryItem(request["username"])
        tableOptions = tableDefaults.combineOptions(request["options"])
        formattedQuery = formatInput(lastQuery)
        tokens = tokenizeInput(formattedQuery["functions"])
        rpnStack = postfixInput(tokens["tokens"])
        
        tablePlots = []
        try:
            #Solve the function for all values in the range
            tablePlots = rangeSolver.getValues(rpnStack, tableOptions)
        except:
            print("Exception at table solver")
        
        tableColumns = []
        tableData = []
        try:
            #Solve the function for all values in the range
            tableColumns = wijmoFormatting.getColumns(tablePlots)
            tableData = wijmoFormatting.formatData(tablePlots, tableOptions["delta"], tableOptions["start"])
        except:
            print("Exception at table formatter")
            
        response["table"] = {
                                  "values": {},
                                  "column": tableColumns,
                                  "data": tableData
                                  }
        for k in range(0, len(tablePlots["stack"])):
            response["table"]["values"][str("f" + str(k))] = tablePlots["stack"][k]
            response["table"]["labels"] = tablePlots["labels"]
        return formatResponse(response)
        
    #Update the 2D plot
    if (request["control"] == "2dplot"):
        lastQuery = getLastHistoryItem(request["username"])
        gridOptions = twoDDefaults.combineOptions(request["options"])
        formattedQuery = formatInput(lastQuery)
        tokens = tokenizeInput(formattedQuery["functions"])
        rpnStack = postfixInput(tokens["tokens"])
        
        plots = []
        
        try:
            #Solve the function for all values in the range
            plots = parser.getPlots(gridOptions["rangeObj"], rpnStack, 1000)
        except:
            print("Exception at 2D parser")

        gridObjs = {}
        try:
            #Create the grid
            gridObjs = grid.generateGrid(gridOptions["rangeObj"], gridOptions["canvasSize"])
        except:
            print("Exception at 2D grid")
        try:
            #Get the actual points that will be placed on screen
            plotObjs = plotter.createPlots(gridOptions["rangeObj"], plots, gridOptions["canvasSize"], gridOptions["colors"])
        except:
            print("Exception at 2D plotter")
            
        response["plot2D"] = {
                                   "grid": gridObjs,
                                   "plots": plotObjs
                                   }
        
    return formatResponse(response)

def createTwoDWorkspace(finalResponse, rpnStack):
    gridOptionsObj = twoDDefaults.getDefault()
    
    try:
        #Solve the function for all values in the range
        plots = parser.getPlots(gridOptionsObj["rangeObj"], rpnStack, 1000)
    except:
        print("Exception at 2D parser")
    
    gridObjs = {}
    try:
        #Create the grid
        gridObjs = grid.generateGrid(gridOptionsObj["rangeObj"], gridOptionsObj["canvasSize"])
    except:
        print("Exception at 2D grid")
    plotObjs = []
    try:
        #Get the actual points that will be placed on screen
        plotObjs = plotter.createPlots(gridOptionsObj["rangeObj"], plots, gridOptionsObj["canvasSize"], gridOptionsObj["colors"])
    except:
        print("Exception at 2D plotter")
        
    finalResponse["plot2D"] = {
                               "grid": gridObjs,
                               "plots": plotObjs
                               }
    
    #Create table
    tableOptionsObj = tableDefaults.getDefault()
    
    tablePlots = []
    try:
        #Solve the function for all values in the range
        tablePlots = rangeSolver.getValues(rpnStack, tableOptionsObj)
    except:
        print("Exception at table solver")
    
    tableColumns = []
    tableData = []
    try:
        #Solve the function for all values in the range
        tableColumns = wijmoFormatting.getColumns(tablePlots)
        tableData = wijmoFormatting.formatData(tablePlots, tableOptionsObj["delta"], tableOptionsObj["start"])
    except:
        print("Exception at table formatter")
        
    finalResponse["table"] = {
                              "values": {},
                              "column": tableColumns,
                              "data": tableData
                              }
    
    for k in range(0, len(tablePlots["stack"])):
        finalResponse["table"]["values"][str("f" + str(k))] = tablePlots["stack"][k]
        finalResponse["table"]["labels"] = tablePlots["labels"]
    
    return finalResponse
    
def createThreeDWorkspace(finalResponse, rpnStack):
    optionsObj = {
                 "3dPlot": {
                            "colors": {
                                       "max": "#FF0000",
                                       "min": "#0000FF"
                                       },
                            
                            "grid": {
                                   "color": "#505050",
                                   "cellSize": 1,
                                   "lineWidth": 0.1
                                    }
                            },
                }
    
    rangeObj = {"xMin": -10,
       "xMax": 10,
       "yMin": -10,
       "yMax": 10,
       "zMin": -10,
       "zMax": 10
       }
    
    plots = []
    try:
        #Solve the function for all values in the range
        plots = threeDparser.getPlots(rangeObj, rpnStack, 100)
    except:
        print("Exception at 3D parser")
    TDGridObjs = {}
    try:
        #Create the grid
        TDGridObjs = threeDgrid.generateGrid(rangeObj, optionsObj["3dPlot"]["grid"])
    except:
        print("Exception at 3D grid")
        
    TDPlotObjs = []
    #try:
        #Get the actual points that will be placed on screen
    TDPlotObjs = threeDplotter.createPlots(rangeObj, plots, optionsObj["3dPlot"]["colors"], 100)
    # except:
    #    print("Exception at 3D plotter")
        
    finalResponse["plot3D"] = {
                               "grid": TDGridObjs,
                               "plots": TDPlotObjs,
                               "vertexColors": {
                                                "max": "#FF0000",
                                                "min": "#0000FF"
                                                }
                               }
    
    return finalResponse
    
def formatInput(query):
    return inputFormatter.formatInput(query)

def tokenizeInput(functions):
    tokenizerResult = []
    try: 
        #Break the statement into tokens
        tokenizerResult = tokenizer.parseToken(functions)
    except:
        print("Exception at tokenizer")
    return tokenizerResult

def postfixInput(tokens):
    rpnStack = []
    try: 
        #Create a usable stack for each function
        rpnStack = postfix.toRPN(tokens)
    except:
        print("Exception at postfix")
    return rpnStack

def newQuery(request):
    print(request)
    if (len(request["query"]) == 0):
        return formatResponse({
                             "success": "false"
                             })
    #Update the user's timeout period
    updateLastAction(request["username"])
    
    #Create the response object
    finalResponse = {}
    
    formattedQuery = formatInput(request["query"])
    
    #############################
    #START FUNCTION TYPE HANDLING
    if (formattedQuery["type"] == "function"):
        tokenizerResult = {}
        #Add the query to the user's history
        addToHistory(request["username"], request["query"])
        
        tokenizerResult = tokenizeInput(formattedQuery["functions"])

        rpnStack = postfixInput(tokenizerResult["tokens"])
        
        
        #Start 2D plot section
        if (tokenizerResult["dimension"] == 2):
            createTwoDWorkspace(finalResponse, rpnStack)
            
            
        ##################
        #End 2D plot section
        
        #Start 3D plot section
        if (tokenizerResult["dimension"] == 3):
            createThreeDWorkspace(finalResponse, rpnStack)
            
            
        #Format the original function into latex
        formattedInput = symPySolver.formatToLatex(formattedQuery["functions"])
        
        
        #Derivative and integral
        
        derivative = symPySolver.getDerivative(formattedQuery["functions"])
        
        integral = symPySolver.getIntegral(formattedQuery["functions"])
        
        
        
        finalResponse["formattedInput"] = formattedInput
        finalResponse["integral"] = integral
        finalResponse["derivative"] = derivative
        
        finalResponse["success"] = "true"
        
    
    #END FUNCTION TYPE HANDLING
    ###########################
    
    
    ############################
    #START COMMAND TYPE HANDLING
    else :
        commandResponse = commandInterpreter.parseCommand(formattedQuery["functions"], request["username"])
        finalResponse = commandResponse
    
    #END COMMAND TYPE HANDLING
    ##########################
    return(formatResponse(finalResponse))

def checkUser(username):
    if (not(checkUserExistence(username))):
        return False
    return True

def processRequest(request):
    
    #Change from bytes to string so that we can parse the request 
    convertedRequest = request.decode("utf-8")
    
    #This is the parsed request with which we can interact 
    parsedRequest = json.loads(convertedRequest)
    print(parsedRequest)
    
    if (parsedRequest["username"]):
        if (checkUser(parsedRequest["username"])):
            
            if (parsedRequest["type"] == "newQuery"):
                response = newQuery(parsedRequest)
                
            elif (parsedRequest["type"] == "deleteHistoryItem"):
                response = deleteHistoryItem(parsedRequest)
                
            elif (parsedRequest["type"] == "updateControl"):
                response = updateControl(parsedRequest)
                
            elif (parsedRequest["type"] == "loginExistingUser"):
                response = loginNoPassword(parsedRequest)
                
            elif (parsedRequest["type"] == "login"):
                response = login(parsedRequest)
                
            else:
                response = formatResponse({
                                         "success": False
                                         })
        else:
            if (parsedRequest["type"] == "register"):
                response = createAccount(parsedRequest)
                
            elif (parsedRequest["type"] == "login"):
                response = login(parsedRequest)
                
            else:
                response = formatResponse({
                                     "sucess": False
                                     })
    else:
        if (parsedRequest["type"] == "login"):
            response = login(parsedRequest)
        
        else:
            response = formatResponse({
                                     "success": False
                                     })
               

        
    #print(response)
    return response