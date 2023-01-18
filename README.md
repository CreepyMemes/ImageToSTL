Still a work in progress. Don't use this fork yet
=====

This is a simple python script that takes an image as input, then proceeds to directly output an STL file ready to 3D print.

Usage
=====

`python ImageToSTL.py`

This script generates an STL file called `imagename.stl`, ready to be 3D printed.
It also generates a height map PNG image file called `imagename-HeightMap.png`.

When printing on FDM, the heightmap should be oriented vertically (the STL should already be oriented correctly).
The printed surface will show the original image when illuminated from the left.
