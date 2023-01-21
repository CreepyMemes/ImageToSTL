What is ImageToSTL?
=====

ImageToSTL is an easy-to-use single program that allows users to quickly and easily convert their favorite images into 3D printable STL files. hether you're a professional 3D designer or a hobbyist, ImageToSTL is the perfect tool for creating beautiful and unique 3D printed objects.

The program works by first taking an image as input, the nozzle height you are going to 3D print with and the model's size in mm, then it analyzes the image to create a height map with the information taken previously. This height map is then used to generate an STL file that is ready to be 3D printed.

The main function of this script is the creation of highly detailed and accurate lithophane-like models. The model it generates is an image that shows up when it's illuminated from the left. 

Usage
=====

![Usage](https://i.imgur.com/cxM0RFu.png)

Select the image you want to convert and the folder you want your STL to be generated in.

![Usage](https://i.imgur.com/SeT4hjN.png)

Insert the width and height values in mm (they will be automatically adjusted to maintain the original aspect ratio of your image)
Then enter the Layer Height you are going to 3D Print with (0.2 mm is set default). 

To confirm the entered values click Generate STL. ImageToSTL will generates an STL file called `imagename.stl` in the folder you've selected.
When printing on FDM, the heightmap should be oriented vertically (the STL file should already be oriented correctly).
