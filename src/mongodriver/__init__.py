import pymongo
from pymongo.mongo_client import MongoClient
import datetime 
from passlib.hash import sha256_crypt #@UnresolvedImport

#START GLOBAL DEFINITIONS

#The the address for the db, this is the default mongo address
#The db has a single collection named "users" at the moment
global ADDR
global PORT 
global DB
global timeout
global dateFormatString
ADDR = "localhost"
PORT = 27017
#timeout period in seconds
timeout = 600 
#The format in which to encode time
dateFormatString = "%Y-%m-%d %H:%M:%S"

#END GLOBAL DEFINITIONS


def loginUser(username, passwd):
    usersCol = DB["users"]
    userList = usersCol.find({"username": username})
    
    #check if the user actually exists
    if (checkUserExistence(username) == False):
        return {"success": False, "message": "No such user exists"}
        
    for doc in userList:
        passwordHash = doc["password"]
        if (sha256_crypt.verify(passwd, passwordHash)):
            updateLastAction(username)
            return {"success": True, "username": username}
        else:
            return {"success": False, "message": "Wrong password"}


def registerUser(username, password):
    hash = sha256_crypt.encrypt(password)
    usersCol = DB["users"]
    
    #check if the user already  exists
    if (checkUserExistence(username) == True):
        return {"success": False, "message": "User already exists"}
    
    #Insert new user
    usersCol.insert({
                     "username": username,
                     "password": hash
                     })
    #Add the lastAction field
    updateLastAction(username)
    return {
            "success": True,
            "message": "Welcome, please sign in"
            }


#updates the last action time for the given user
def updateLastAction(username):
    usersCol = DB["users"]
    userList = usersCol.find({"username": username})
    now = datetime.datetime.now()
    formattedTime = now.strftime(dateFormatString)
    for doc in userList:
        usersCol.update({"_id": doc["_id"]}, {"$set": {"lastAction" : formattedTime}})


def checkUserSession(username):
    if checkUserExistence(username):
        usersCol = DB["users"]
        userList = usersCol.find({"username": username})
        
        #Get the current time
        now = datetime.datetime.now()
        
        for doc in userList:
            lastAction = doc["lastAction"]
            #Convert the string time saved in the DB into a usable object
            then = datetime.datetime.strptime(lastAction, dateFormatString)
            end = now - then
            print(end.total_seconds())
            
            if (end.total_seconds() > timeout):
                return False
            else:
                return True
            
    return False

#Adds a new entry to the user's history
def addToHistory(username, query):
    usersCol = DB["users"]
    userList = usersCol.find({"username": username})
    
    for doc in userList:
        usersCol.update({"_id": doc["_id"]}, {"$push": {"history" : query}})
    
#Retrieve a user's history    
def getUserHistory(username):
    if checkUserExistence(username):
        usersCol = DB["users"]
        userList = usersCol.find({"username": username})
        for doc in userList:
            return doc["history"]

#Get the user's last query
def getLastHistoryItem(username):
    history = getUserHistory(username)
    return history[-1]

#Delete a single item from the user's history
def deleteSingleHistoryItem(username, index):
    if checkUserExistence(username):
        usersCol = DB["users"]
        userList = usersCol.find({"username": username})
        for doc in userList:
            #This is the only way to delete by item index
            #Note that None is actually a synonym for null in pymongo, that's why this query works
            usersCol.update({"_id": doc["_id"]}, {"$unset": {"history." + str(index) : 1}})
            usersCol.update({"_id": doc["_id"]}, {"$pull": {"history" : None}})

#Check to see if a user exists in the database
def checkUserExistence(username):
    usersCol = DB["users"]
    userList = usersCol.find({"username": username})
    if (userList.count() == 0):
        return False
    else:
        return True
    

def connectToDB():
    print("connectToDB")
    client = MongoClient(ADDR, PORT)
    global DB 
    DB = client["grapher"]


    
connectToDB()