_Note: (13 February 2016) There have been reports that this importer is no longer working.  It was originally written in late 2014, and I haven't messed much with it since.  I've put it on my todo list of things to checkout when I get some time, so I'll post an update when I get a chance.  I think it's a problem with the liblas module, but I haven't troubleshooted it enough to know for sure._

LiDAR-Importer
==============

This is a Blender LiDAR Importer I built for importing LASer (LAS) point cloud data sets.  This addon currently ONLY supports the LAS file format and requires the liblas python module (see below).

![Screenshot of Imported LiDAR Data](http://i.imgur.com/h2cUBfH.png)

## Installation:

### Dependancies:
You will need the liblas python module found here: https://github.com/libLAS/libLAS/tree/master/python/liblas

### Mac OS X Instructions:
Download and move the LiDAR-Importer directory into:
```
~/Library/Application\ Support/Blender/[_version_]/scripts/addons/
```
Download the liblas python module and move the liblas directory into:
```
/Applications/Blender/blender.app/Contents/Resources/[_version_]/python/lib/python3.4/site-packages/
```
### Microsoft Windows Instructions:
Coming soon ...

### Linux Instructions:
Coming soon ...

## Version History:
* Version 0.1 (10 October 2014)

## License:
This code is available under the MIT License (see [LICENSE.txt](LICENSE.txt) for more information)
