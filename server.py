"""Script server based on SimpleHTTPServer
Handles GET and POST requests, in-memory session management,
HTTP redirection

Python scripts are executed in a namespace made of :
- request : for the data received from the query string or the request body. 
            Calling 'http://host/myScript.py?foo=bar' will make 
            request = {'foo':['bar']} available in the namespace of myScript
- headers : the http request headers
- resp_headers : the http response headers
- Session() : a function returning the session object
- HTTP_REDIRECTION : an exception to raise if the script wants to redirect
to a specified URL (raise HTTP_REDIRECTION, url)

A simple templating system is provided, using the Python string substitution
mechanism introduced in Python 2.4 (syntax $name). Template files must have
the extension .tpl

Hello world programs : will print "Hello world !" if called with the query
string ?name=world
- hello.py (Python script) [ http://localhost/hello.py?name=world ]
   print "Hello",request['name'][0],"!"
- hello.tpl (template)  [ http://localhost/hello.tpl?name=world ]
   Hello $name !

Other extensions can be handled by adding methods self.run_(extension)
"""

import sys
import os
import string
import cStringIO
import random
import cgi
import select
import SimpleHTTPServer
import Cookie
import SimulationFactory, Simulation
import getopt
import atexit

chars = string.ascii_letters + string.digits
sessionDict = {} # dictionary mapping session id's to session objects

class SessionElement(object):
   """Arbitrary objects, referenced by the session id"""
   pass

def generateRandom(length):
    """Return a random string of specified length (used for session id's)"""
    return ''.join([random.choice(chars) for i in range(length)])

def release_port(s):
   s.serve_forever()
   
class HTTP_REDIRECTION(Exception):
    pass

class ScriptRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """One instance of this class is created for each HTTP request"""

    def do_GET(self):
       """Begin serving a GET request"""
       # build self.body from the query string
       self.body = {}
       if self.path.find('?')>-1:
          qs = self.path.split('?',1)[1]
          self.body = cgi.parse_qs(qs, keep_blank_values=1)

       print ("request: %s"%(self.path.split('?',1)[0]))
       if (self.path.split('?',1)[0] == '/SimulationProgress'):
          self.get_simulation_progress()
       elif self.path.split('?',1)[0] == '/StartSimulation':
          self.start_simulation()
       elif (self.path.split('?',1)[0] == '/SimulationResults'):
          self.get_simulation_results()
       elif (self.path.split('?',1)[0] == '/SimulationOutput'):
          self.get_simulation_output()
       else:
          self.handle_data()
        
    def do_POST(self):
        """Begin serving a POST request. The request data is readable
        on a file-like object called self.rfile"""
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        length = int(self.headers.getheader('content-length'))
        self.body = {}
        if ctype == 'multipart/form-data':
            self.body = cgi.parse_multipart(self.rfile, pdict)
        if ctype == 'application/x-www-form-urlencoded':
            qs = self.rfile.read(length)
            self.body.update( cgi.parse_qs(qs, keep_blank_values=1) )
        #else:
        #    self.body = {}
        # Unknown content-type
        # some browsers send 2 more bytes...
        [ready_to_read,x,y] = select.select([self.connection],[],[],0)
        if ready_to_read:
            self.rfile.read(2)
        if self.path.split('?',1)[0] == '/StartSimulation':
           self.start_simulation()
        else:
           self.handle_data()
           
    def get_simulation_output(self):
       msg = ""
       if( not 'projectId' in self.body ):
          msg = msg + 'Must include the projectId'
       else:
          projectId = self.body['projectId'][0]
          msg = SimulationFactory.getSimulationOutput(projectId)
       try:
          self.resp_headers = {"Content-type":'text/html'} # default
          self.resp_headers['Content-length'] = len(msg)
           
          self.send_response(200)
          for (k,v) in self.resp_headers.items():
             self.send_header(k,v)
          self.end_headers()
          self.wfile.write(msg)
       except IOError:
          self.send_error(404, "Exception Getting Simulation Progress")
          
    def get_simulation_results(self):
       msg = ""
       if( not 'projectId' in self.body ):
          msg = msg + 'Must include the projectId'
       else:
          projectId = self.body['projectId'][0]
          msg = SimulationFactory.getSimulationResults(projectId)
       try:
          self.resp_headers = {"Content-type":'text/html'} # default
          self.resp_headers['Content-length'] = len(msg)
           
          self.send_response(200)
          for (k,v) in self.resp_headers.items():
             self.send_header(k,v)
          self.end_headers()
          self.wfile.write(msg)
       except IOError:
          self.send_error(404, "Exception Getting Simulation Progress")
          
    def get_simulation_progress(self):
       msg = ""
       if( not 'projectId' in self.body ):
             msg = msg + 'Must include the projectId'
       else:
          projectId = self.body['projectId'][0]
          msg = SimulationFactory.getSimulationProgress(projectId)
       try:
          #os.popen('gridlabd IEEE_13_house_vvc.glm > testSUCCESS')
          self.resp_headers = {"Content-type":'text/html'} # default
          self.resp_headers['Content-length'] = len(msg)
          #self.done(200,msg)

          self.send_response(200)
          for (k,v) in self.resp_headers.items():
            self.send_header(k,v)
          self.end_headers()
          self.wfile.write(msg)
       except IOError:
          self.send_error(404, "Exception Getting Simulation Progress")
          
    def start_simulation(self):
       try:
          msg = ""
          if( not 'filepath' in self.body ):
             msg = msg + 'Must include the file' 
          elif( not 'projectId' in self.body ):
             msg = msg + 'Must include the projectId'
          else:
             projectId = self.body['projectId'][0]
             msg = SimulationFactory.newSimulation( self.body['file'][0], projectId )
          #os.popen('gridlabd IEEE_13_house_vvc.glm > testSUCCESS')
          self.resp_headers = {"Content-type":'text/html'} # default
          self.resp_headers['Content-length'] = len(msg)
          #self.done(200,msg)

          self.send_response(200)
          for (k,v) in self.resp_headers.items():
            self.send_header(k,v)
          self.end_headers()
          self.wfile.write(msg)
       except IOError:
          self.send_error(404, "Exception starting simulation")

    def list_active_simulations():
        pass
    
    def handle_data(self):
        """Process the data received"""
        self.resp_headers = {"Content-type":'text/html'} # default
        self.cookie=Cookie.SimpleCookie()
        if self.headers.has_key('cookie'):
            self.cookie=Cookie.SimpleCookie(self.headers.getheader("cookie"))
        path = self.get_file() # return a file name or None
        if os.path.isdir(path):
            # list directory
            dir_list = self.list_directory(path)
            self.copyfile(dir_list, self.wfile)
            return
        ext = os.path.splitext(path)[1].lower()
        if len(ext)>1 and hasattr(self,"run_%s" %ext[1:]):
            # if run_some_extension() exists
            exec ("self.run_%s(path)" %ext[1:])
        else:
            # other files
            ctype = self.guess_type(path)
            if ctype.startswith('text/'):
                mode = 'r'
            else:
                mode = 'rb'
            try:
                f = open(path,mode)
                self.resp_headers['Content-type'] = ctype
                self.resp_headers['Content-length'] = str(os.fstat(f.fileno())[6])
                self.done(200,f)
            except IOError:
                self.send_error(404, "File not found in handle_data")

    def done(self, code, infile):
        """Send response, cookies, response headers 
        and the data read from infile"""
        self.send_response(code)
        for morsel in self.cookie.values():
            self.send_header('Set-Cookie', morsel.output(header='').lstrip())
        for (k,v) in self.resp_headers.items():
            self.send_header(k,v)
        self.end_headers()
        infile.seek(0)
        self.copyfile(infile, self.wfile)

    def get_file(self):
        """Set the Content-type header and return the file open
        for reading, or None"""
        path = self.path
        if path.find('?')>1:
            # remove query string, otherwise the file will not be found
            path = path.split('?',1)[0]
        path = self.translate_path(path)
        if os.path.isdir(path):

            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
        return path

    '''def run_py(self, script):
        """Run a Python script"""
        # redirect standard output so that the "print" statements 
        # in the script will be sent to the web browser
        sys.stdout = cStringIO.StringIO()

        # build the namespace in which the script will be run
        namespace = {'request':self.body, 'headers' : self.headers,
            'resp_headers':self.resp_headers, 'Session':self.Session,
            'HTTP_REDIRECTION':HTTP_REDIRECTION}
        try:
            execfile (script,namespace)
        except HTTP_REDIRECTION, url:
            self.resp_headers['Location'] = url
            self.done(301,cStringIO.StringIO())
        except:
            # print a traceback
            # first reset the output stream
            sys.stdout = cStringIO.StringIO()
            exc_type,exc_value,tb=sys.exc_info()
            msg = exc_value.args[0]
            if tb.tb_next is None:     # errors (detected by the parser)
                line = exc_value.lineno
                text = exc_value.text
            else:                      # exceptions
                line = tb.tb_next.tb_lineno
                text = open(script).readlines()[line-1]
            print '%s in file %s : %s' %(exc_type.__name__,
                os.path.basename(script), cgi.escape(msg))
            print '<br>Line %s' %line
            print '<br><pre><b>%s</b></pre>' %cgi.escape(text)
        self.resp_headers['Content-length'] = sys.stdout.tell()
        self.done(200,sys.stdout)'''

    '''def run_tpl(self,script):
        """Templating system with the string substitution syntax
        introduced in Python 2.4"""

        # values must be strings, not lists
        dic = dict([ (k,v[0]) for k,v in self.body.items() ])
        # first check if the string.Template class is available
        if hasattr(string,"Template"): # Python 2.4 or above
            try:
                data = string.Template(open(script).read()).substitute(dic)
            except:
                exc_type,exc_value,tb=sys.exc_info()
                msg = exc_value.args[0]
                data = '%s in file %s : %s' \
                    %(exc_type.__name__,os.path.basename(script), 
                    cgi.escape(msg))
        else:
            data = "Unable to handle this syntax for " + \
                "string substitution. Python version must be 2.4 or above"
        self.resp_headers['Content-length'] = len(data)
        self.done(200,cStringIO.StringIO(data))'''

    '''def Session(self):
        """Session management
        If the client has sent a cookie named sessionId, take its value and 
        return the corresponding SessionElement objet, stored in 
        sessionDict
        Otherwise create a new SessionElement objet and generate a random
        8-letters value sent back to the client as the value for a cookie
        called sessionId"""
        if self.cookie.has_key("sessionId"):
            sessionId=self.cookie["sessionId"].value
        else:
            sessionId=generateRandom(8)
            self.cookie["sessionId"]=sessionId
        try:
            sessionObject = sessionDict[sessionId]
        except KeyError:
            sessionObject = SessionElement()
            sessionDict[sessionId] = sessionObject
        return sessionObject'''

if __name__=="__main__":
   try:
      opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
   except getopt.GetoptError, err:
      # print help information and exit:
      print str(err) # will print something like "option -a not recognized"
      usage()
      sys.exit(2)
   output = None
   verbose = False
   port = 2150
   for o, a in opts:

      if o in ("-h", "--help"):
         usage()
         sys.exit()
      elif o in ("-o", "--output"):
         port = int(a)
      else:
         assert False, "unhandled option"

   # launch the server on the specified port
   import SocketServer
   s=SocketServer.TCPServer(('',port),ScriptRequestHandler)
   print "ScriptServer running on port %s" % port
   atexit.register(release_port, s)
   s.serve_forever()
   #s.socket.close()

   

   
