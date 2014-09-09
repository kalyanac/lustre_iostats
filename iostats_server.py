#!/usr/bin/env python
# coding: utf-8

'''
Created on Jun 12, 2014
sourced from: https://pypi.python.org/pypi/python-jsonrpc/0.3.4
@author: kalyana
'''

# Standard modules
import sys
from socket import gethostname
from threading import Thread, Lock
import Queue

# Local modules
import pyjsonrpc
import json


from iostats_utils import dctOSCStatsPos, dctMDCStatsPos, BWFileSystems, printJobMDCStats

JobMDCStats = {}
JobID = None
AggrQueueDict = {}
NumNodes = 0
NodesCheckedin = 0
NodesLock = Lock()
AggrThreads = []

TotalReadBytes = 0
TotalWriteBytes = 0


def AddStats(ClientStats):
    """Test function"""
    global NodesCheckedin, NodesLock
#    print "In AddStats"
    stats = json.loads(ClientStats)

    for host in stats.keys():        
        for filesystem in stats[host]:
            if filesystem not in BWFileSystems.keys():
                sys.stderr.write ("skipping " + filesystem + ", not a known file system \n")
                continue
            else:
                AggrQueueDict[filesystem].put(stats[host][filesystem])
        
    with NodesLock:
        NodesCheckedin += 1
        
    return True

def AggregateStats(filesystem):
    """Aggregate incoming metrics"""
    global NumNodes, NodesCheckedin
    
    NodeCount = 0
    JobMDCStats[filesystem] = [0.00 for x in xrange(len(dctMDCStatsPos.keys()))]
    
    while (NodeCount != NumNodes):
        try:
            stats = AggrQueueDict[filesystem].get(True, 3)
        except Queue.Empty:
            if ((NodesCheckedin == NumNodes) and AggrQueueDict[filesystem].empty()):
                # Nothing left to process
                return
            else:
                continue
        #Calculate MDC stats first
        for Idx, stat in enumerate (stats["mdc"]):
            JobMDCStats[filesystem][Idx] += float(stat)
        NodeCount += 1
#        print "thread: " + filesystem + " node count: " , NodeCount
        
    return
    

class RequestHandler(pyjsonrpc.HttpRequestHandler):

    # Register public JSON-RPC methods
    methods = {
        "add": AddStats
    }
    
    def log_message(self, formatk, *args):
        #Skip logging connections
        return


# Threading HTTP-Server
http_server = None

def runServer():
    global http_server, Port
    
    sys.stderr.write("Starting HTTP server ... \n")
    sys.stderr.write("URL: http://" + http_server.server_name + ":" + str(http_server.server_port)+"\n")

    http_server.serve_forever()


if __name__ == '__main__':
    
    from os import environ
    from getpass import getuser
    try:
        JobID = environ["PBS_JOBID"]
    except KeyError:
        sys.stderr.write("Could not read PBS_JOBID \n")
        sys.exit(-1)
    try:
        NumNodes = environ["PBS_NUM_NODES"]
    except KeyError:
        sys.stderr.write("Could not read PBS_NUM_NODES, exiting. \n")
        sys.exit(-1)
    try:
        NumNodes = int(NumNodes)
    except ValueError:
        sys.stderr.write("Invalid PBS_NUM_NODES value,", NumNodes," exiting. \n")
        sys.exit(-1)
        
    try:
        Port = int(JobID.split(".")[0])
    except ValueError:
        sys.stderr.write("Invalid PBS_JOBID value,", JobID," exiting. \n")
        sys.exit(-1)

#    print "JobID is", JobID
    
    for fs in BWFileSystems.keys():
        AggrQueueDict[fs] = Queue.Queue()
        AggrThreads.append(Thread(target=AggregateStats, args=(fs,)))
        AggrThreads[-1].start()
        
    http_server = pyjsonrpc.ThreadingHttpServer(
                                            server_address=(gethostname(), Port),
                                            RequestHandlerClass=RequestHandler
                                            )
    
        
    # Start server in a different thread    
    ServerThread = Thread(target=runServer)
    ServerThread.start()
    
    for thrd in AggrThreads:
        thrd.join()
        
    http_server.shutdown()
    
    ServerThread.join()
    
    printJobMDCStats(JobMDCStats)


