import numpy as np
from stl import mesh

# Total amount of triangles in the mesh
def get_tot_triangles(cols, rows):
    return 2 * ( ((cols-1) * (rows-1) + 2 * ( (cols-1) + (rows-1))) + ((cols-1) + (rows-1) - 1) )

# Defines the coordinates of each height map vertex
def get_vertices(vertices, height_map, width, height, cols, rows):
    for i, row in enumerate(height_map):
        for j, pixel in enumerate(row):
            vertices[i][j] = ( j * (width / (cols-1)) - width/2, pixel * width / -10, height - i * (height / (rows-1)) ) # (x, y, z)
    return vertices

# Tesselates the main surface mesh by combining all the height map vertices through triangles
def tesselate_main(surface, vertices, cols, rows, count):
    for i in range(rows-1):
        for j in range(cols-1):
            surface.vectors[count]  [0] = vertices[i]   [j]
            surface.vectors[count]  [1] = vertices[i]   [j+1]
            surface.vectors[count]  [2] = vertices[i+1] [j]
            surface.vectors[count+1][0] = vertices[i+1] [j+1]
            surface.vectors[count+1][1] = vertices[i]   [j+1]
            surface.vectors[count+1][2] = vertices[i+1 ][j]
            count += 2
    return count

# Convert height map vertex, to a flat back vertex
def back_vertex(vertex, thickness):
    return ( vertex[0], thickness, vertex[2] )

# Tesselates the frame mesh by combining all the frame vertices through triangles
def tesselate_frame(surface, vertices, cols, rows, count, thickness):
    for i in range(cols-1):
         # Top row frame
        surface.vectors[count]  [0] = vertices[0][i]
        surface.vectors[count]  [1] = back_vertex(vertices[0][i],   thickness)
        surface.vectors[count]  [2] = vertices[0][i+1]
        surface.vectors[count+1][0] = back_vertex(vertices[0][i],   thickness)
        surface.vectors[count+1][1] = vertices[0][i+1]
        surface.vectors[count+1][2] = back_vertex(vertices[0][i+1], thickness)
        # Bottom row frame
        surface.vectors[count+2][0] = vertices[rows-1][i]
        surface.vectors[count+2][1] = back_vertex(vertices[rows-1][i],   thickness)
        surface.vectors[count+2][2] = vertices[rows-1][i+1]
        surface.vectors[count+3][0] = back_vertex(vertices[rows-1][i],   thickness)
        surface.vectors[count+3][1] = vertices[rows-1][i+1]
        surface.vectors[count+3][2] = back_vertex(vertices[rows-1][i+1], thickness)
        count += 4
    for i in range(rows-1):
        # Left column frame
        surface.vectors[count]  [0] = vertices[i][0]
        surface.vectors[count]  [1] = back_vertex(vertices[i]  [0], thickness)
        surface.vectors[count]  [2] = vertices[i+1][0]
        surface.vectors[count+1][0] = back_vertex(vertices[i]  [0], thickness)
        surface.vectors[count+1][1] = vertices[i+1][0]
        surface.vectors[count+1][2] = back_vertex(vertices[i+1][0], thickness)
        # Right column frame
        surface.vectors[count+2][0] = vertices[i][cols-1]
        surface.vectors[count+2][1] = back_vertex(vertices[i]  [cols-1], thickness)
        surface.vectors[count+2][2] = vertices[i+1][cols-1]
        surface.vectors[count+3][0] = back_vertex(vertices[i]  [cols-1], thickness)
        surface.vectors[count+3][1] = vertices[i+1][cols-1]
        surface.vectors[count+3][2] = back_vertex(vertices[i+1][cols-1], thickness)
        count += 4
    return count

# Algorithm that generates the path to stitch the back of the STL mesh to make it a 3D printable solid
def get_stitching_coords(rows, cols):
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

# Stitches the hole in the back in order to make it a 3D printable solid
def stitch_hole(surface, vertices, cols, rows, count, thickness):
    # Gets the coordinates of the path that stitches the hole in the back
    coords = get_stitching_coords(rows, cols)

    # Stiches the mesh hole in the back
    for i in range(1, len(coords)-1):
        surface.vectors[count][0] = back_vertex(vertices[coords[i-1][0]][coords[i-1][1]], thickness) 
        surface.vectors[count][1] = back_vertex(vertices[coords[i]  [0]][coords[i]  [1]], thickness)
        surface.vectors[count][2] = back_vertex(vertices[coords[i+1][0]][coords[i+1][1]], thickness) 
        count += 1
    return count

# Creates and completes the whole STL mesh
def get_mesh(cols, rows, width, height, height_map):

    # Solid mesh thickness, total amount of triangles in the whole mesh and a variable that counts each triangle iteration
    thickness = width / 40
    triangles = get_tot_triangles(cols, rows)
    count = 0

    # Declares the array that will contain all the vertices of the height map mesh and defines thier positions based on the height map
    vertices = np.zeros( (rows, cols, 3) )
    vertices = get_vertices( vertices, height_map, width, height, cols, rows )

    # Creates the 3D mesh
    surface = mesh.Mesh( np.zeros(triangles, dtype=mesh.Mesh.dtype) )

    # Generates the STL mesh
    count = tesselate_main  ( surface, vertices, cols, rows, count)
    count = tesselate_frame ( surface, vertices, cols, rows, count, thickness)
    count = stitch_hole     ( surface, vertices, cols, rows, count, thickness)

    return surface

# Saves the mesh to an STL file
def save_stl(mesh, path):
    mesh.save(path)