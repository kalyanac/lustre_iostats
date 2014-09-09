lustre_iostats
==============

_Job IO statistics on Lustre file systems for HPC Clusters_

A quick and dirty utility to get raw job IO statistics on Lustre file systems. This utility is written in Python.

*How to use:*
Refer to the sample job script on how to use this utility.

External Dependencies:

* [python-jsonrpc](https://pypi.python.org/pypi/python-jsonrpc/)
    * [bunch](https://pypi.python.org/pypi/bunch/1.0.1)
* [tabulate](https://pypi.python.org/pypi/tabulate/0.7.2)


Sample output
-------------
<pre>
File data transfer statistics for this job:
+---------------+-------------+--------------+
| File System   | File Read   | File Write   |
+===============+=============+==============+
| BW Home       | 320.0 MB    | 32.0 GB      |
+---------------+-------------+--------------+
| BW Scratch    | 0.0 bytes   | 0.0 bytes    |
+---------------+-------------+--------------+
| BW Projects   | 0.0 bytes   | 0.0 bytes    |
+---------------+-------------+--------------+

Metadata statistics for this job:
+---------------+--------+---------+----------+-------------+---------+-----------+---------+
| File System   |   open |   close |   create |        seek |   fsync |   getattr |   mkdir |
+===============+========+=========+==========+=============+=========+===========+=========+
| BW Home       |    288 |     288 |        0 | 8.38861e+06 |       0 |       576 |       0 |
+---------------+--------+---------+----------+-------------+---------+-----------+---------+
| BW Scratch    |      0 |       0 |        0 | 0           |       0 |         0 |       0 |
+---------------+--------+---------+----------+-------------+---------+-----------+---------+
| BW Projects   |      0 |       0 |        0 | 0           |       0 |         0 |       0 |
+---------------+--------+---------+----------+-------------+---------+-----------+---------+

</pre>

This work was developed while at [NCSA](http://www.ncsa.illinois.edu).
