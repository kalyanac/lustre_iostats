'''
Created on Jun 17, 2014

@author: kalyana
'''
import sys
from tabulate import tabulate

output = []
new_row = []

dctOSCStatsPos = {"snapshot_time":0}
dctMDCStatsPos = {
                  "snapshot_time":0, "read_bytes": 1, "write_bytes": 2,
                  "ioctl": 3, "open": 4, "close": 5, "mmap": 6, "seek": 7,
                  "fsync": 8, "readdir": 9, "setattr": 10, "truncate": 11,
                  "getattr": 12, "create": 13, "link": 14, "unlink": 15,
                  "symlink": 16, "mkdir": 17, "rmdir": 18, "rename": 19,
                  "statfs": 20, "alloc_inode": 21, "setxattr": 22, 
                  "getxattr": 23, "inode_permission": 24  
                  }

BWFileSystems = {"snx11001":"BW Home","snx11002":"BW Projects","snx11003":"BW Scratch"}


def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'PB')

def printJobMDCStats(JobMDCStats):
    global output, new_row
    
    # File data transfer stats
    output = [["File System", "File Read", "File Write"]]
    
    for filesystem in BWFileSystems:
        new_row = [BWFileSystems[filesystem]]
        stats = JobMDCStats[filesystem]
        new_row.append(sizeof_fmt(stats[dctMDCStatsPos["read_bytes"]]))
        new_row.append(sizeof_fmt(stats[dctMDCStatsPos["write_bytes"]]))
        output.append(new_row)
        
    print "File data transfer statistics for this job:"
    print tabulate (output, headers="firstrow", tablefmt="grid")
    
    #MDS stats
    
    output = [["File System", "open", "close", "create", "seek", "fsync", "getattr", "mkdir"]]
    new_row = []
    
    for filesystem in BWFileSystems:
        new_row = [BWFileSystems[filesystem]]
        stats = JobMDCStats[filesystem]
        new_row.append(stats[dctMDCStatsPos["open"]])
        new_row.append(stats[dctMDCStatsPos["close"]])
        new_row.append(stats[dctMDCStatsPos["create"]])
        new_row.append(stats[dctMDCStatsPos["seek"]])
        new_row.append(stats[dctMDCStatsPos["fsync"]])
        new_row.append(stats[dctMDCStatsPos["getattr"]])
        new_row.append(stats[dctMDCStatsPos["mkdir"]])
        output.append(new_row)
    
    print 
    print "Metadata statistics for this job:"
    print tabulate(output, headers="firstrow", tablefmt="grid")
                        

if __name__ == '__main__':
    pass

    # Test chunk 
    dctTest = {}
    dctTest["snx11001"]=[10, 1073741824, 107374]
    dctTest["snx11002"]=[20, 20347898146, 207374543]
    dctTest["snx11003"]=[30, 1073741, 1073723474]
    printJobMDCStats(dctTest)
    
    print tabulate(output, headers="firstrow", )

