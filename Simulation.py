import os, sys, subprocess, re, shutil
class Simulation(object):
    """ Wrapper class for GridSpice simulations """
    def __init__( self, simulationDirectory, simulationId ):
        self.simulationDirectory = simulationDirectory
        self.simulationId = simulationId
        self.resultsDirectory =  simulationDirectory + '/results'
        self.glmDirectory = simulationDirectory + '/glm'
        self.glmFile = self.glmDirectory + '/model.glm'
        self.logFile = self.simulationDirectory + '/output.log'
        self.errFile = self.simulationDirectory + '/error.log'
        self.serverLocation = 'http://dev03.gridspice.org/rev2'
        #Set valid to false,  we will set it to true at the end of init
        self.valid = False
        
        # If we are starting the simulation, make sure to clear our directory
        if os.path.exists( self.simulationDirectory ):
            shutil.rmtree( self.simulationDirectory )
        os.mkdir( simulationDirectory )
        os.mkdir( self.resultsDirectory )
        os.mkdir( self.glmDirectory )
        #self.child_pid = os.fork()

            
        self.gridsimulation = subprocess.Popen(['/usr/lib/gridlabd/gridlabd.bin',self.glmFile], \
                                               cwd=self.resultsDirectory, stdout=self.output.fileno(),\
                                               stderr=self.error.fileno() )
        ## Fork a new process to run the simulation, but store the
        ## child's pid
        #if self.child_pid == 0:
        self.output = open( self.logFile, 'w+' )
        self.error = open( self.errFile, 'w+' )
        print "Child Process: PID# %s" % os.getpid()
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
            if 'FATAL' or 'ERROR' in line:
                return False
            else:
                print 'FATAL or ERROR not contained in "%s"'%line
        print 'PROCESS IS VALID: %s'%lines
        return True
    # This function determines if the simulation process has terminated
    def getTerminated(self):
        # if the simulation is null, we probably already waited on the
        # zombie process 
        if not self.gridsimulation:
            return True
        exitCode = self.gridsimulation.poll()
        if exitCode is not None:
            # If the simulation has completed, wait on the pid to free
            # the zombie process
            self.gridsimulation.wait()
            self.gridsimulation = []
            return True
        return False

    # Returns a 2-line response.  The first line is either 'COMPLETED', 'FAILED', or 'IN PROGRESS'
    # The second line is either the timestamp, or N/A
    def getProgress(self):
        msg = ""
        if self.getTerminated() and self.getValid():
            msg = msg+ 'COMPLETED,'
        elif self.getValid():
            msg = msg + "IN PROGRESS,"
        else:
            msg = msg + 'FAILED,'
        lines = os.popen("tac "+self.logFile)
        for line in lines:
            match = re.search('\AProcessing \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',line)
            if match:
                print 'found match'
                time = match.group(0)[10:]
                msg = msg + time
                return msg
            else:
                print "unmatch"+line
        msg = msg +'N/A'
        return msg
        
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
        
