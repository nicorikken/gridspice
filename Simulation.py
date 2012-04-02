import os, sys, subprocess, re, shutil, server, SimulationFactory
class Simulation(object):
    """ Wrapper class for GridSpice simulations """
    def __init__( self, simulationDirectory, simulationId, fileURL ):
        self.simulationDirectory = simulationDirectory
        self.simulationId = simulationId
        self.resultsDirectory =  simulationDirectory + '/results'
        self.glmDirectory = simulationDirectory + '/glm'
        self.glmFile = self.glmDirectory + '/model.glm'
        self.lockFile = self.glmDirectory +'/complete'
        self.logFile = self.simulationDirectory + '/output.log'
        self.errFile = self.simulationDirectory + '/error.log'
        self.serverLocation = 'http://dev03.gridspice.org/SimulatorWrapper'
        #Set valid to false,  we will set it to true at the end of init
        self.valid = False
        
        # If we are starting the simulation, make sure to clear our directory
        if os.path.exists( self.simulationDirectory ):
            shutil.rmtree( self.simulationDirectory )
        os.mkdir( simulationDirectory )
        os.mkdir( self.resultsDirectory )
        os.mkdir( self.glmDirectory )
        self.child_pid = os.fork()
        
        self.terminated = False
        print "connecting to %s" % fileURL
        ## Fork a new process to run the simulation, but store the
        ## child's pid
        if self.child_pid == 0:
            #SimulationFactory.closeSockets()
            self.output = open( self.logFile, 'w+' )
            self.error = open( self.errFile, 'w+' )
            os.system('curl -o %s %s' % (self.glmFile, fileURL))
            file = open("%s"%self.lockFile,'w+')
            file.close()
            simulationProc = subprocess.Popen( ['/usr/lib/gridlabd/gridlabd.bin', self.glmFile], \
                       cwd=self.resultsDirectory, stdout=self.output.fileno(),\
                       stderr=self.error.fileno() )
            simulationProc.wait()
            os._exit(os.EX_OK)
        self.valid = True
        

    def name(self):
        return str(self.simulationId)

    # Determine if the simulation actually started
    def getValid(self):
        # If the process is still running we will assume its valid
        if not self.getTerminated():
            return True

        lines = os.popen("cat "+self.errFile)
        # If there is an ERROR in the output, the simulation failed
        for line in lines:
            if 'ERROR' in line or 'FATAL' in line:
                print 'failing on line: %s'%line
                return False
            else:
                print 'FATAL or ERROR not contained in "%s"'%line
        print 'PROCESS IS VALID: %s'%lines
        return True
    # This function determines if the simulation process has terminated
    def getTerminated(self):
        # if the simulation is null, we probably already waited on the
        # zombie process
        print "CHECKONG ON CHILD PID %s"%self.child_pid
        if self.terminated:
            return True
        
        pid,status = os.waitpid(self.child_pid, os.WNOHANG)
        if status == 0 and pid==0:
            return False

        self.terminated = True
        print "Process still alive %s %s"% (pid,status)
        #exitCode = self.gridsimulation.poll()
        #if exitCode is not None:
            # If the simulation has completed, wait on the pid to free
            # the zombie process
        #    self.gridsimulation.wait()
        #    self.gridsimulation = []
        #    return True
        return True

    # Returns a 2-line response.  The first line is either 'COMPLETED', 'FAILED', or 'IN PROGRESS'
    # The second line is either the timestamp, or N/A
    def getProgress(self):
        msg = ""
        if not self.glmReceived():
            msg = msg+ 'GENERATING GLM FILE,'
        elif self.getTerminated() and self.getValid():
            msg = msg+ 'COMPLETED,'
        elif self.getValid() and not self.getSimulationTime():
            msg = msg + "SIMULATION INITIALIZING"
        elif self.getValid():
            msg = msg + "SIMULATION IN PROGRESS,"
            msg += self.getSimulationTime()
        else:
            msg = msg + 'FAILED,'

        print "response: %s"%msg
        return msg

    def getSimulationTime( self ):
        lines = os.popen("tac "+self.logFile)
        for line in lines:
            match = re.search('\AProcessing \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',line)
            if match:
                print 'found match'
                time = match.group(0)[10:]
                if( time ):
                    return time
                
            else:
                print "unmatch"+line
        return ""
   
    def glmReceived(self):
        if( os.path.exists(self.lockFile)):
            return True
        return False
    
    def getResults(self):
        dirElems = os.listdir(self.resultsDirectory)
        msg = "{"
        for i in range(len(dirElems)):
            msg = msg + '"%s"'% dirElems[i]
            msg = msg + ':'
            msg = msg + '"%s/%s/%s"'% (self.serverLocation,\
                                  os.path.relpath( self.resultsDirectory ), dirElems[i])
            # Add a comma if its not the last element
            if not i == len(dirElems) -1 :
                msg = msg + ','
        msg += '}'
        return msg
        
