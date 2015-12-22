from mongodriver import *

#Page source is written in markdown
helpPageSource = """##Welcome to Python Grapher's help page
                
This utility is able to plot, find the derivative and integral of and generate a table of values for
functions. It can display functions with 0, 1 or 2 independent variables. Currently however, these 
independent variables must be either 'x' or 'y', with x being used in a two dimensional plot, and 
both 'x' and 'y' being used in three dimensional plots. 

Also, remember that your session will time out after 10 minutes of inactivity. 
                 
##Entering functions:

####Single functions:

Single function may be entered simply as
 
> [function]

For example, 

> x^2

or

> sin(x) * tan(y)

####Multiple functions:

Multiple function can be entered as a series of single functions which are separated by a semicolon(;)

> [function1] ; [function2] ; [function3]

For example,

>sin(x);x^2;x-5

##Helpful commands:

There are a couple of commands that can be ran, including this help page.

####Show the user history:

Shows a list of the current user's history. The user can then either re-run those
items, or delete them. 

> history

####Help page:

Shows this help page

> help

####Favorites:

Coming soon(hopefully)

> favorites
"""
                



#We must simply act according to the command
def parseCommand(command, username):
    
    if (command == "history"):
        return {
                "historySelection": getUserHistory(username),
                "success": "true"
                }
    #Simply return the help page source
    if (command == "help"):
        return {
                "helpPage": helpPageSource,
                "success": "true"
                }
    if (command == "favorites"):
        print("favorites")