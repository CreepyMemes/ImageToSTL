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
    # Loads the pixel data of the image and normalizes it to the range [0, 1]
    img_name  = 'input.png'
    img       = Image.open(img_name).convert('L')
    pixels    = img.load() 
    cols      = img.width  # Total amount of pixels in each row
    rows      = img.height # Total amount of rows in the image
    pixels    = [ [(pixels[x, y] / 255) for x in range(cols)] for y in range(rows) ]

    # Calculates the average of every pixel in the image
    average = sum(pixel for row in pixels for pixel in row) / (cols * rows)

    # Converts the image into a normalized height map
    height_map = getHeightMap(pixels, average)

    # Outputs the height map image
    out_img = Image.new( 'L', (cols, rows) )
    for y, row in enumerate(height_map):
        for x, pixel in enumerate(row):
            out_img.putpixel( (x, y), int(255 * pixel) )
    out_img.save( f"{img_name.split('.')[0]}-HeightMap.png" )

    # Mesh size constraints
    width     = 100                         # Mesh width
    scale     = -width * 0.1                 # Height map scale
    increment = width     / (cols-1)        # Distance between each vertex
    height    = increment * (rows-1)        # Mesh height
    triangles = (cols-1)  * (rows-1) * 2    # Total amount of triangles in the height map mesh

    # Declares a 2D numpy array that will contain all the vertices of the height map mesh
    vertices  = np.zeros((rows, cols, 3))

    # Defines the coordinates of each vertex
    for i, row in enumerate(height_map):
        for j, pixel in enumerate(row):
            vertices[i][j] = ( j*increment - width/2, pixel * scale, height - i*increment )
    
    # Creates the STL mesh
    surface = mesh.Mesh(np.zeros(triangles, dtype=mesh.Mesh.dtype))

    # Tesselates the mesh by combining all the vertexes through triangles
    count = 0 # Count each triangle
    for i in range(rows-1):
        for j in range(cols-1):
            surface.vectors[count][0] = vertices[i][j]
            surface.vectors[count][1] = vertices[i][j+1]
            surface.vectors[count][2] = vertices[i+1][j]
            count += 1
    for i in range(rows-1, 0, -1):
        for j in range(cols-1, 0, -1):
            surface.vectors[count][0] = vertices[i][j]
            surface.vectors[count][1] = vertices[i][j-1]
            surface.vectors[count][2] = vertices[i-1][j]
            count += 1

    # Saves the mesh to an file STL file
    surface.save(f"{img_name.split('.')[0]}.stl")

if __name__ == '__main__':
    main()
