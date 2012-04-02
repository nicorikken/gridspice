import os, socket, sys, subprocess, time
def PickUnusedPort():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('localhost', 0))
  addr, port = s.getsockname()
  s.close()
  return port


port = PickUnusedPort()
output = subprocess.Popen( '/usr/bin/python2.6 recipe.py -o %d' % port ,shell=True )
print 'bound to port %d'%port
time.sleep(5)
print output

import httplib, urllib
glmFile =  open('test.glm','r+').read()
params = urllib.urlencode({'file': glmFile, 'projectId':1})
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost:%d" % port)
conn.request("POST", "/StartSimulation", params, headers)
response = conn.getresponse()
print response.status, response.reason
assert(response.read() == 'SUCCESS' )
time.sleep(5)
conn.request("GET", "/SimulationResults?projectId=1")
response = conn.getresponse()
print response.status, response.reason
responseStr = response.read()
print responseStr
assert( '{"test_lights_standalone.csv":'\
        '"./simulation/sim-1/results/test_lights_standalone.csv"}' in responseStr )

output.kill()

print 'passed'
conn.close()


