# Seoul-Crosswalk-Network
# Description
In Seoul pedestrian network layer, crosswalks are disconnected by overlapped network such as highway, tunnel, underpass.
When we conduct network analysis for the network, the disconnected crosswalk network prevents to deal with crosswalks.
The script finds the connected lines and merges them as one line feature.
The script is dealing with crosswalk network, but you can handle various network featuers if you change the attribute value.
Before starting the script, you should finish merging pedestrian network process in 'seoul-pedestrian-network'.
# Preprocessing
For the script, you should preapre a node layer
* The node layer for the script has nodes that on the disconnected points of crosswalk lines. you can selecte and export them with spatial tools in QGIS.
# Needed materials
- QGIS (upto 3.4 version)
- Python (upto 3 version)
