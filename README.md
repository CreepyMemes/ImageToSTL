What is ImageToSTL?
=====

ImageToSTL is a user-friendly program that allows users to easily convert their favorite images into 3D printable STL files. Users can quickly and easily generate high-quality STL files that are perfect for printing on any FDM printer.

The program works by first taking an image as input, then analyzing the image to create a height map. This height map is then used to generate an STL file that is ready to be 3D printed.

One of the key features of ImageToSTL is its ability to create highly detailed and accurate STL files, which are perfect for creating lithophane-like models. The model it generates is an image that shows up when it's illuminated from the left. This makes ImageToSTL an ideal tool for creating beautiful and unique 3D printed gifts and keepsakes.

Overall, ImageToSTL is an easy-to-use program that allows users to quickly and easily convert their favorite images into 3D printable STL files. Whether you're a professional 3D designer or a hobbyist, ImageToSTL is the perfect tool for creating beautiful and unique 3D printed objects.

Note
=====

This project is still a work in progress, and I'm planning to add a GUI to make the program even more user-friendly.

Usage
=====

`python ImageToSTL.py`

Put the script and the image you want to convert in the same folder. ImageToSTL will generates an STL file called `imagename.stl` in the same folder.
When printing on FDM, the heightmap should be oriented vertically (the STL file should already be oriented correctly).
The printed surface will show the original image when illuminated from the left.
