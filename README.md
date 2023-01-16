Setup
=====

- Install python 3.11 - https://www.python.org/downloads/
- Install requirements - `python -m pip install -r requirements.txt`

Usage
=====

`python pic3d.py my-image.png`

This will create an image called `my-image-3d.png`.
This is a heightmap for the 3d print which can be converted to STL by many tools.
I used OpenSCAD and included the file used to render to STL - `pic3d.scad`

When printing on FDM, the heightmap should be oriented vertically so the
image is facing the -y direction (as if it's a picture hanging on a wall).

The surface will show the original image when illuminated from the left.
If you want a different direction, rotate the image before running the script, so that the side you want illuminated is facing left.
