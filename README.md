Blender LiDAR Importer
==============

This is a Blender LiDAR Importer I built for importing LASer (LAS) point cloud data sets.  This addon currently ONLY supports the LAS file format.

## Update:
I have changed this plugin to use laspy instead of liblas, and it should be much easier to install now.

## Known Issues:
The points are not centered after importing, so you will need to scale the object after importing before the verticies are visible in Blender's viewport.

## Install Instructions:
Clone the repository to your local machine:
```
git clone https://github.com/nittanygeek/LiDAR-Importer.git
```
In Blender, Navigate to Edit > Preferences, and click on Add-ons tab.
Click "Install" at the top, and Select the LiDAR-Importer.py file from cloned repository.
Activate the Addon

## Usage:
File > Import > LiDAR Format (.las) > Select your LAS file and click "Import LiDAR File"
**Note: Large LAS files will take a long time to import.  Be patient.**


## License:
This code is available under the MIT License (see [LICENSE.txt](LICENSE.txt) for more information)
