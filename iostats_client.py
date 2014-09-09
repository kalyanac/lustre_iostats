#!/usr/bin/env python
'''
Created on Jun 14, 2014

@author: kalyana
'''

import sys
import pyjsonrpc
import os
import glob
from socket import gethostname
from getpass import getuser
import json
from iostats_utils import dctOSCStatsPos, dctMDCStatsPos

dctOSCStats = {}
dctAggrMDCStats = {}
dctAggrOSCStats = {}

#Hold all node level stats to send to server
dctNodeStats = {}
dctNodeStatsPrev = {}
dctNodeStatsDelta = {}

lstSplStats = ["read_bytes","write_bytes","ost_read","ost_write"]
MDCPath = "/proc/fs/lustre/llite/snx1100*"
OSCPath = "/proc/fs/lustre/osc/snx1100*"
JSONFileName = ""

lstMDCStats = list(xrange(25))
lstMDCStatsPrev = None


lstOSCStats = list(xrange(25))
lstOSCStatsPrev = None

myHostName = None

Port = 0


def GetOSCStats(LogFile):
    'Read stats from OSC log file'
    
    global dctOSCStats
    
    try:
        LogLines = open(LogFile).readlines()
    except OSError:
        sys.stderr.write("Cannot open ", LogFile, " on node ", gethostname())
        dctOSCStats["snapshot_time"] = None
        return False
        
    for Line in LogLines:
        Stat, StatValue = Line.strip().split(None,1)
        if (Stat not in lstSplStats):
            dctOSCStats[Stat] = StatValue.split()[0]
        else:
            dctOSCStats[Stat] = StatValue.split()[-1]
    return True

    
def GetMDCStats(LogFile):
    'Read Stats from MDC log file'
    
    global lstMDCStats
    
    try:
        LogLines = open(LogFile).readlines()
    except OSError:
        sys.stderr.write("Cannot open ", LogFile, " on node ", gethostname())
        'TODO: Send data to server and then quit so server is not waiting forever'
        return False
        
    for Line in LogLines:
        Stat, StatValue = Line.strip().split(None,1)
        if (Stat not in lstSplStats):
            StatValue = StatValue.split()[0]
        else:
            StatValue =   StatValue.split()[-1]
            
        try:
            lstMDCStats[dctMDCStatsPos[Stat]] = StatValue
        except KeyError:
            # A stat of no interest to us   
            pass

    return True
    

def CollectData():
    'Collect data'
    global dctOSCStats, dctAggrMDCStats, dctAggrOSCStats, lstMDCStats
    #Start with MDC stats
    
    for Paths in glob.glob(MDCPath):
        GetMDCStats(Paths+"/stats")
        fsName = Paths.split("/")[-1].split("-")[0]
        dctNodeStats[myHostName][fsName] = {}
        dctNodeStats[myHostName][fsName]["mdc"] = lstMDCStats
        lstMDCStats = list(xrange(25))
        
    # OSC Stats
    for Paths in glob.glob(OSCPath):
        GetOSCStats(Paths+"/stats")
        fsName = Paths.split("/")[-1].split("-")[0]
        ostID  = Paths.split("/")[-1].split("-")[1]
        try:
            dctAggrOSCStats[fsName][ostID] = dctOSCStats
        except KeyError:
            dctAggrOSCStats[fsName] = {}
            dctAggrOSCStats[fsName][ostID] = dctOSCStats
        dctOSCStats = {}

def SerializeData():
    'Serialize data'
    
    global dctAggrMDCStats, dctAggrOSCStats, JSONFileName
    
    with open(JSONFileName,"w") as outfile:
        json.dump(dctNodeStats, outfile)
                
def DeSerializeData():
    'Read data from file'
    global dctNodeStatsPrev

    with open(JSONFileName, "r") as infile:
        dctNodeStatsPrev = json.load(infile)
        
    return


def SendData(ServerURL):
    'Send Data'

    http_client = pyjsonrpc.HttpClient("http://"+ServerURL+":"+str(Port))
#    http_client = pyjsonrpc.HttpClient(url="http://localhost:8080")
#    http_client.call("add", json.dumps(dctAggrMDCStats))
    http_client.call("add", json.dumps(dctNodeStatsDelta))

    
def CalculateDelta():
    global dctNodeStatsDelta, dctNodeStats, dctNodeStatsPrev
    dctNodeStatsDelta[myHostName] = {}
    for fs in dctNodeStats[myHostName]:
        dctNodeStatsDelta[myHostName][fs] = {"mdc":[],"osc":[]}
        dctNodeStatsDelta[myHostName][fs]["mdc"] =  [float(x)-float(y) for x,y in zip(dctNodeStats[myHostName][fs]["mdc"], dctNodeStatsPrev[myHostName][fs]["mdc"])]
        
    return


if __name__ == '__main__':
    try:
        JobID = os.environ.get("PBS_JOBID", None)
    except KeyError:
        sys.stderr.write("Could not read PBS_JOBID \n")
        sys.exit(-1)

    try:
        Port = int(JobID.split(".")[0])
    except ValueError:
        sys.stderr.write("Invalid PBS_JOBID value,", JobID," exiting. \n")
        sys.exit(-1)
    
                
    step = int(sys.argv[1])
#    print "Step is ", step
    
    JSONFileName = "/tmp/iostats_"+getuser()+"_"+JobID+".json"
    
    myHostName = gethostname()
    dctNodeStats[myHostName] = {}
    
    if (step == 1):
        CollectData()
        SerializeData()
    else:
        CollectData()
        DeSerializeData()
        CalculateDelta()
        SendData(sys.argv[2])
        
#     try:
#         RunID = sys.argv[1]
#         ' RunID is used to determine if this is the last collection phase'
#         if (RunID == "stop"):
#             'Send data to the server and call it quits'
#             Send()
#             
#     except IndexError:
#         'Collect data, process it, serialize it and quit'
#         SerializeData()


