import http.server
import os
import socketserver
from graphercore import grapherrequesthandler

PORT = 8080
global absPath
absPath = ""

class requestHandler(http.server.SimpleHTTPRequestHandler):
    
    #override do_Get to set a custom path
    def do_GET(self):
        global absPath
        
        #default path is '/'
        if self.path == '/':
            
            if (absPath == ""):
                #We have to go back directories by using os since self.path will only allow us to work 
                    #    with the current directory as the root, we can't say "../../pathToIndex.html
                os.chdir( "../../front-end")
            
                absPath = os.path.abspath(".")
                self.path = 'demo/index.html'

            else:
                #Ensure that other resources that are requested will be available.
                os.chdir(absPath)
                self.path = "demo/index.html"
            
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        contentLength = int(self.headers.get("Content-Length"))
        request = self.rfile.read(contentLength)
        response = grapherrequesthandler.processRequest(request)
    
        self.send_response(200) #create header
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response) #send response
        
        
def startServer():
    handler = requestHandler
    server = socketserver.TCPServer(('0.0.0.0', PORT), handler)
    server.serve_forever()
    