LiDAR-Importer
==============

This is a Blender LiDAR Importer I built for importing LASer (LAS) point cloud data sets.  This addon currently ONLY supports the LAS file format and requires the liblas python module (see below).

![Screenshot of Imported LiDAR Data](http://i.imgur.com/h2cUBfH.png)

## BEFORE YOU BEGIN: Please understand that this importer will delete everything within the current scene, so please import your data into a fresh .blend file to reduce the risk of data loss.

## Installation Instructions:

### Install Blender.
You can optionally compile Blender from source for bleeding edge functinality, but it is not necessary.  If you want to compile Blender from source, the documentation can be found here: https://wiki.blender.org/index.php/Dev:Doc/Building_Blender/Linux/Ubuntu/CMake

### Compile and Install LibLAS.
The LibLAS python module is necessary for the importer to function.  You can compile and install LibLAS by following the instructions here: http://www.liblas.org/compilation.html#get-the-source-code

_Note: when installing LibLAS, be sure to install the Boost library, as it's a mandatory dependancy for LibLAS to compile properly.  Be sure to install this before running the cmake command durring the liblas build process.  You can install Boost on Debian/Ubuntu with the following command:_
```
sudo apt-get install libboost-all-dev
```
Once you have liblas compiled and installed, copy the /liblas/python/liblas/ folder into blender's /build_linux/bin/2.77/python/lib/python3.5/ directory.

_Note: Do NOT install it into the site-packages directory, as you will end up getting an error when trying to enable the addon regarding liblas being missing._  

### Obtain and install the Importer plugin.
You can either download the zip file from this GitHub repo, or clone the repo and compress the files yourself to a zip.
```
git clone https://github.com/bchynds/LiDAR-Importer.git
zip -r LiDAR-Importer.zip LiDAR-Importer
```
Then use the generated zip file to install the Addon in Blender.  After enabling the addon, you'll find the importer available at File > Import > LiDAR Format (.las)

Tip: if you open Blender from a terminal window, you can see progress output from the addon.  I haven't added much of any loading indication within Blender yet, so this is the only way to view when the file has completed processing.

Example output:
```
running read_lidar_data
3265110  verticies in file
3265110  verticies imported
Total time to process (seconds):  103.49237489700317
File:  /home/bchynds/Downloads/Serpent Mound Model LAS Data.las
completed read_lidar_data...
Percentage of points imported:  100
```


## License:
This code is available under the MIT License (see [LICENSE.txt](LICENSE.txt) for more information)
