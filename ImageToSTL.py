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

# Algorithm that generates the path to stitch the back of the STL mesh to make it a 3D printable solid
def getStitchingCoords(rows, cols):
    coords = []
    xa, za = (0, 0)
    for i in range(cols + rows - 2):
        if i < rows:
            z = i
        else: 
            z = rows - 1
            xa += 1      
        if i+1 < cols:
            x = i+1
        else: 
            x = cols - 1
            za += 1      
        coords.append((z, xa))
        coords.append((za, x))
    return coords

# Main program
def main():

    # Main input Constants 
    img_name      = 'dwayne.png'                                                       # Image file name
    layer_height  = 0.2                                                                # Nozzle layer height to print the object with
    width         = 50                                                                 # Object width  size in mm

    # Image Loader
    img           = Image.open(img_name).convert('L')                                  # Opens the image and converts it to grayscale        
    width, height = ( width, width * img.size[1] / img.size[0] )                       # Actual object size in mm with original aspect ratio
    rows          = int( height/ (layer_height * 2) )                                  # Image resizing pixels per row
    cols          = int( rows * height / width )                                       # Image resizing pixels per column
    img           = img.resize( (cols, rows) )                                         # Resizes the image with the previous values
    pixels        = img.load()                                                         # Loads the image data into pixels
    pixels        = [ [pixels[x, y] / 255 for x in range(cols)] for y in range(rows) ] # Converts the image data into a normalized list of lists

    # Calculates the average of every pixel in the image
    average = sum(pixel for row in pixels for pixel in row) / (cols * rows)

    # Converts the image into a normalized height map
    height_map = getHeightMap(pixels, average)

    # Saves the height map image into PNG file
    out_img = Image.new( 'L', (cols, rows) )
    for y, row in enumerate(height_map):
        for x, pixel in enumerate(row):
            out_img.putpixel( (x, y), int(255 * pixel) )
    out_img.save( f"{img_name.split('.')[0]}_heightmap.png" )
    print("Height Map File Generated!")
    
    # Mesh variables
    thickness = width / 30                                                                             # Solid mesh thickness
    triangles = 2 * ( ((cols-1) * (rows-1) + 2 * ( (cols-1) + (rows-1))) + ((cols-1) + (rows-1) - 1) ) # Total amount of triangles in the whole mesh
    count = 0                                                                                          # Variable that counts each triangle

    # Declares a 3D numpy array that will contain all the vertices of the height map mesh
    vertices_heightmap  = np.zeros( (rows, cols, 3) )
    
    # Defines the coordinates of each height map vertex
    for i, row in enumerate(height_map):
        for j, pixel in enumerate(row):
            vertices_heightmap[i][j] = ( j * (width / (cols-1)) - width/2, pixel * width / -10, height - i * (height / (rows-1)) ) # (x, y, z)
    
    # Creates the STL mesh
    surface = mesh.Mesh( np.zeros(triangles, dtype=mesh.Mesh.dtype) )
    
    # Tesselates the main surface mesh by combining all the height map vertices through triangles
    for i in range(rows-1):
        for j in range(cols-1):
            surface.vectors[count]   [0] = vertices_heightmap[i]    [j]
            surface.vectors[count]   [1] = vertices_heightmap[i]    [j+1]
            surface.vectors[count]   [2] = vertices_heightmap[i+1]  [j]
            surface.vectors[count+1] [0] = vertices_heightmap[i+1]  [j+1]
            surface.vectors[count+1] [1] = vertices_heightmap[i]    [j+1]
            surface.vectors[count+1] [2] = vertices_heightmap[i+1 ] [j]
            count += 2

    # Tesselates the frame mesh by combining all the frame vertices through triangles
    for i in range(cols-1): # Top/Bottom row frame
        surface.vectors[count]   [0] =   vertices_heightmap[0]      [i]
        surface.vectors[count]   [1] = ( vertices_heightmap[0]      [i]      [0], thickness, vertices_heightmap[0]      [i]      [2] )
        surface.vectors[count]   [2] =   vertices_heightmap[0]      [i+1]
        surface.vectors[count+1] [0] = ( vertices_heightmap[0]      [i]      [0], thickness, vertices_heightmap[0]      [i]      [2] )
        surface.vectors[count+1] [1] =   vertices_heightmap[0]      [i+1]
        surface.vectors[count+1] [2] = ( vertices_heightmap[0]      [i+1]    [0], thickness, vertices_heightmap[0]      [i+1]    [2] )
        surface.vectors[count+2] [0] =   vertices_heightmap[rows-1] [i]
        surface.vectors[count+2] [1] = ( vertices_heightmap[rows-1] [i]      [0], thickness, vertices_heightmap[rows-1] [i]      [2] )
        surface.vectors[count+2] [2] =   vertices_heightmap[rows-1] [i+1]
        surface.vectors[count+3] [0] = ( vertices_heightmap[rows-1] [i]      [0], thickness, vertices_heightmap[rows-1] [i]      [2] )
        surface.vectors[count+3] [1] =   vertices_heightmap[rows-1] [i+1]
        surface.vectors[count+3] [2] = ( vertices_heightmap[rows-1] [i+1]    [0], thickness, vertices_heightmap[rows-1] [i+1]    [2] )
        count += 4
    for i in range(rows-1): # Left/Right column frame
        surface.vectors[count]   [0] =   vertices_heightmap[i]      [0]
        surface.vectors[count]   [1] = ( vertices_heightmap[i]      [0]      [0], thickness, vertices_heightmap[i]      [0]      [2] )
        surface.vectors[count]   [2] =   vertices_heightmap[i+1]    [0]
        surface.vectors[count+1] [0] = ( vertices_heightmap[i]      [0]      [0], thickness, vertices_heightmap[i]      [0]      [2] )
        surface.vectors[count+1] [1] =   vertices_heightmap[i+1]    [0]
        surface.vectors[count+1] [2] = ( vertices_heightmap[i+1]    [0]      [0], thickness, vertices_heightmap[i+1]    [0]      [2] )
        surface.vectors[count+2] [0] =   vertices_heightmap[i]      [cols-1]
        surface.vectors[count+2] [1] = ( vertices_heightmap[i]      [cols-1] [0], thickness, vertices_heightmap[i]      [cols-1] [2] )
        surface.vectors[count+2] [2] =   vertices_heightmap[i+1]    [cols-1]
        surface.vectors[count+3] [0] = ( vertices_heightmap[i]      [cols-1] [0], thickness, vertices_heightmap[i]      [cols-1] [2] )
        surface.vectors[count+3] [1] =   vertices_heightmap[i+1]    [cols-1]
        surface.vectors[count+3] [2] = ( vertices_heightmap[i+1]    [cols-1] [0], thickness, vertices_heightmap[i+1]    [cols-1] [2] )
        count += 4

    # Gets the coords to stitch the hole in the back
    coords = getStitchingCoords(rows, cols)

    # Stitches the hole in the back in order to make it a 3D printable solid
    for i in range(1, len(coords)-1):
        surface.vectors[count] [0] = ( vertices_heightmap[coords[i-1] [0]] [coords[i-1] [1]] [0], thickness, vertices_heightmap[coords[i-1] [0]] [coords[i-1] [1]] [2] )
        surface.vectors[count] [1] = ( vertices_heightmap[coords[i]   [0]] [coords[i]   [1]] [0], thickness, vertices_heightmap[coords[i]   [0]] [coords[i]   [1]] [2] )
        surface.vectors[count] [2] = ( vertices_heightmap[coords[i+1] [0]] [coords[i+1] [1]] [0], thickness, vertices_heightmap[coords[i+1] [0]] [coords[i+1] [1]] [2] )
        count += 1

    # Saves the mesh to an STL file
    surface.save(f"{img_name.split('.')[0]}.stl")
    print("STL File Generated!")

if __name__ == '__main__':
    main()
