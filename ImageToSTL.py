from PIL import Image
from stl import mesh
import numpy as np

# Normalizes a list of lists to the range [0, 1]
def getNormalized(pixels):
    max_pix = max( pixel for row in pixels for pixel in row )
    min_pix = min( pixel for row in pixels for pixel in row )
    return [ [(pixel - min_pix) / (max_pix - min_pix) for pixel in row] for row in pixels ]

# Converts a row of the image into a height map with the average value of all pixels give as an argument
def getRowHeightMap(row, average):
    result = []
    total  = 0
    for pixel in row:
        total += pixel - average
        result.append(total)
    return [ pixel - total/2 for pixel in result ]

# Converts a whole image into a height map
def getHeightMap(pixels, average):
    return getNormalized( [ getRowHeightMap(row, average) for row in pixels ] )
    
def main():
    # Image Loader
    img_name   = 'dwayne.png'                                                         # Image file name
    img        = Image.open(img_name).convert('L')                                    # Opens the image and converts it to grayscale                                                          
    cols, rows = (200, 200)                                                           # Final image size in mm
    img        = img.resize( (cols, int(cols * img.size[1] / img.size[0])) )          # Resizes the image with while maintaining the aspect ratio
    cols, rows = img.size                                                             # Actual image size in mm with original aspect ratio   
    pixels     = img.load()                                                           # Loads the image data into pixels
    pixels     = [ [(pixels[x, y] / 255) for x in range(cols)] for y in range(rows) ] # Converts the image data into a list of lists

    # Calculates the average of every pixel in the image
    average = sum(pixel for row in pixels for pixel in row) / (cols * rows)

    # Converts the image into a normalized height map
    height_map = getHeightMap(pixels, average)

    # Saves the height map image into PNG file
    out_img = Image.new( 'L', (cols, rows) )
    for y, row in enumerate(height_map):
        for x, pixel in enumerate(row):
            out_img.putpixel( (x, y), int(255 * pixel) )
    out_img.save( f"{img_name.split('.')[0]}-HeightMap.png" )
    print("Height Map Generated!")

    # Mesh size constraints
    scale     = cols     * -0.1           # Height map scale
    increment = cols     / (cols-1)       # Distance between each vertex
    triangles = (cols-1) * (rows-1) * 2   # Total amount of triangles in the height map mesh
    count     = 0                         # Count each triangle

    # Declares a 3D numpy array that will contain all the vertices of the height map mesh
    vertices  = np.zeros((rows, cols, 3))

    # Defines the coordinates of each vertex
    for i, row in enumerate(height_map):
        for j, pixel in enumerate(row):
            vertices[i][j] = ( j * increment - cols/2, pixel * scale, rows - i * increment )
    
    # Creates the STL mesh
    surface = mesh.Mesh(np.zeros(triangles, dtype=mesh.Mesh.dtype))

    # Tesselates the mesh by combining all the vertexes through triangles
    for i in range(rows-1):
        for j in range(cols-1):
            surface.vectors[count][0] = vertices[i][j]
            surface.vectors[count][1] = vertices[i][j+1]
            surface.vectors[count][2] = vertices[i+1][j]
            count += 1
            surface.vectors[count][0] = vertices[i+1][j+1]
            surface.vectors[count][1] = vertices[i][j+1]
            surface.vectors[count][2] = vertices[i+1][j]
            count += 1

    # Saves the mesh to an STL file
    surface.save(f"{img_name.split('.')[0]}.stl")
    print("STL Generated!")

if __name__ == '__main__':
    main()
