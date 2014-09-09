lustre_iostats
==============

_Job IO statistics on Lustre file systems for HPC Clusters_

A quick and dirty utility to get raw job IO statistics on Lustre file systems. This utility is written in Python.

*How to use:*

Refer to the sample job script on how to use this utility.

*External Dependencies:*

* [python-jsonrpc](https://pypi.python.org/pypi/python-jsonrpc/)
    * [bunch](https://pypi.python.org/pypi/bunch/1.0.1)
* [tabulate](https://pypi.python.org/pypi/tabulate/0.7.2)

*Site Customizations:*

   In ```iostats_client.py```, update the following to reflect the file system names at your site


   ```
   MDCPath = "/proc/fs/lustre/llite/snx1100*"
   
   OSCPath = "/proc/fs/lustre/osc/snx1100*"
   ```
   
   The server picks a port to listen to based on the job id. The job id format I worked with is _server.jobid_. The _jobid_ portion is numeric. If your job ID's are not numeric, customize the ```Port``` variable in ```iostats_client.py``` & ```iostats_server.py``` to match your needs. Using _jobid_ is convenient as there will never be a conflict when multiple jobs are using this utility. 

*Issues*

   Error handling is not extensively tested. Espeically if permissions restrict the script from reading the necessary files in ```/proc```, there maybe issues with the server waiting forever. 

Sample output
-------------
<pre>

+---------------+-------------+--------------+
| File System   | File Read   | File Write   |
+===============+=============+==============+
| BW Home       | 320.0 MB    | 0.0 bytes    |
+---------------+-------------+--------------+
| BW Scratch    | 32.0 GB     | 32.0 GB      |
+---------------+-------------+--------------+
| BW Projects   | 0.0 bytes   | 0.0 bytes    |
+---------------+-------------+--------------+

Metadata statistics for this job:
+---------------+--------+---------+----------+-------------+---------+-----------+---------+
| File System   |   open |   close |   create |        seek |   fsync |   getattr |   mkdir |
+===============+========+=========+==========+=============+=========+===========+=========+
| BW Home       |    160 |     160 |        0 | 0           |       0 |       448 |       0 |
+---------------+--------+---------+----------+-------------+---------+-----------+---------+
| BW Scratch    |    256 |     256 |        0 | 1.67772e+07 |       0 |       256 |       0 |
+---------------+--------+---------+----------+-------------+---------+-----------+---------+
| BW Projects   |      0 |       0 |        0 | 0           |       0 |         0 |       0 |
+---------------+--------+---------+----------+-------------+---------+-----------+---------+

</pre>

This work was developed while at [NCSA](http://www.ncsa.illinois.edu). Please provide attribution as needed. 
