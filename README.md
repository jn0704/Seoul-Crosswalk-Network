# Seoul-Crosswalk-Network
# Description
In Seoul pedestrian network layer, crosswalks are disconnected by overlapped network such as highway, tunnel, underpass.
When we conduct network analysis for the network, the disconnected crosswalk network prevents to deal with crosswalks.
The script fineds the connected lines and merges them as one line feature.
Before starting the script, you should finish merging pedestrian network process in 'seoul-pedestrian-network'.
# Preprocessing
For the script, you should preapre some layers
* The node layer for the script has nodes that on the disconnected points of crosswalk lines. you can selecte and export them with spatial tools in QGIS.
* The pedestrian road layer for the script has lines that remove overlapped network. The lines have 1 or 2 or 3 or 6 value in "LINK_FACIL" of attribute table.
# Needed materials
- QGIS (upto 3.4 version)
- Python (upto 3 version)
