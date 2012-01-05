import shutil, Simulation, os


simulationRootDirectory = '%s/simulation' % os.getcwd()
allSimulations = {}
print "init Simulation Factory"
#nextSimulationId = 0
# Remove old simulations
try:
    print "flushing directory: %s" % simulationRootDirectory
    shutil.rmtree( simulationRootDirectory )
    os.mkdir( simulationRootDirectory )
except Exception, e:
    print "Could not flush simulation directory %s" % e
    pass
         
# Iterate through the simulation directory and find an unused id
def getUnusedSimulationId():
    maxSimulationId = 0
    dirElems = os.listdir( simulationRootDirectory )
    print dirElems
    for elem in dirElems:
        try:
            currentSimulationId = int(elem.split("-")[1])
            if (currentSimulationId > maxSimulationId):
                maxSimulationId = currentSimulationId
        except:
            print 'corrupted simulation directory'
            return maxSimulationId + 1
        
def getSimulationProgress( projectId ):
    if( not projectId in allSimulations ):
        return 'unknown project id'
    return allSimulations[projectId].getProgress()

def getSimulationResults( projectId ):
    if( not projectId in allSimulations ):
        return 'unknown project id'
    return allSimulations[projectId].getResults()

# The server should not run more than 16 simulations at once
# so we make sure that less than 16 are available.
def activeSimulationCount():
    activeSimulations = 0;
    for projectId in allSimulations.keys():
        if( not allSimulations[projectId].getTerminated() ):
            activeSimulations = activeSimulations + 1
    return activeSimulations

def newSimulation( file,projectId, rootFileName ):
    global simulationRootDirectory
    #nextSimulationId = nextSimulationId + 1
    #simId = nextSimulationId
    if( activeSimulationCount() > 16 ):
        return 'Error: Server Busy.  Too many simulations running'
    if( projectId in allSimulations and not allSimulations[projectId].getTerminated() ):
        return 'Error: Simulation already started'
    simulationDirectory = simulationRootDirectory+ "/sim-" + str(projectId)
    simulation = Simulation.Simulation( simulationDirectory, projectId, rootFileName )
    allSimulations[projectId] = simulation
    return 'SUCCESS'

def beginSimulation( projectId ):
    allSimulations[projectId].startSimulationProess()
    return 'SUCCESS'

def addModelData( projectId, file, fileName ):
    if projectId in allSimulations:
        allSimulations[projectId].addFile( fileName, file )
        return "SUCCESS"
    else:
        return "CANNOT ADD %s, NO SIMULATION FOR PROJECT ID %s"%(fileName, projectId)
    
