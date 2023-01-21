import PySimpleGUI as sg
import numpy as np
from PIL import Image
from stl import mesh
from functions import *

# Window black theme
sg.ChangeLookAndFeel('black')

# Main program function
def main(): 
    # Main window layout
    layout = [
        [ sg.Text('Select an image:',          size = (20,  1)),                                      sg.In(size = (40, 1), key='-FILE-',   enable_events = True),                sg.FileBrowse() ],
        [ sg.Text('Folder to save your STL:',  size = (20,  1), visible=False, key='-FOLDER_TEXT-'),  sg.In(size = (40, 1), key='-FOLDER-', enable_events = True, visible=False), sg.FolderBrowse(visible=False, key='-FOLDER_BROWSE-') ],
        [ sg.Text() ],
        [ sg.Text('Width:',         size = (15,  1), visible=False, key="-WIDTH_TEXT-"),   sg.In(size = (7,  1), key="-WIDTH-",  enable_events = True, visible=False),                     sg.Text('mm', visible=False, key="-WIDTH_MM-")  ],
        [ sg.Text('Height:',        size = (15,  1), visible=False, key="-HEIGHT_TEXT-"),  sg.In(size = (7,  1), key='-HEIGHT-', enable_events = True, visible=False),                     sg.Text('mm', visible=False, key="-HEIGHT_MM-") ],
        [ sg.Text('Nozzle height:', size = (15,  1), visible=False, key="-NOZZLE_TEXT-"),  sg.In(size = (7,  1), key='-NOZZLE-', enable_events = True, visible=False, default_text="0.2"), sg.Text('mm', visible=False, key="-NOZZLE_MM-") ],
        [ sg.Text() ],
        [ sg.Button('Generate STL!', visible=False, key="-GENERATE-"), sg.Text('STL File Generated!', visible=False, key="-GENERATED_TEXT-")]
    ]

    # Create the window object
    window = sg.Window("ImageToSTL", layout, size=(700,300), finalize=True)

    # Make window object react to pressing enter or clicking them with left mouse button
    window['-WIDTH-' ].bind("<Return>",   "ENTER-")
    window['-WIDTH-' ].bind("<Button-1>", "CLICK-")
    window['-HEIGHT-'].bind("<Return>",   "ENTER-")
    window['-HEIGHT-'].bind("<Button-1>", "CLICK-")
    window['-NOZZLE-'].bind("<Return>",   "ENTER-")
    window['-NOZZLE-'].bind("<Button-1>", "CLICK-")

    # Initialize None variables
    img, temp, width, height = (None, None, None, None)

    # Main program loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
    
        if event == '-FILE-':
            # Opens the image and converts it to grayscale
            img = Image.open(values['-FILE-']).convert('L')

            # Shows hidden folder inputs
            window['-FOLDER_TEXT-' ].Update(visible = True)
            window['-FOLDER-' ].Update(visible = True)
            window['-FOLDER_BROWSE-' ].Update(visible = True)
            # Hide generation confirmation if file is changed
            window['-GENERATED_TEXT-'].Update(visible = False) 
            # Update ratio if new image is put
            if len(values['-WIDTH-']) > 0 and len(values['-HEIGHT-']) > 0:
                height = round( float(values['-WIDTH-']) * img.size[1] / img.size[0], 2 )
                window['-HEIGHT-'].Update(height)
                values['-HEIGHT-'] = str(height)

        if event == '-FOLDER-':
            # Shows hidden text inputs
            window['-WIDTH_TEXT-' ].Update(visible = True)
            window['-WIDTH-'      ].Update(visible = True)
            window['-WIDTH_MM-'   ].Update(visible = True)
            window['-HEIGHT_TEXT-'].Update(visible = True)
            window['-HEIGHT-'     ].Update(visible = True)
            window['-HEIGHT_MM-'  ].Update(visible = True)
            window['-NOZZLE_TEXT-'].Update(visible = True)
            window['-NOZZLE-'     ].Update(visible = True)
            window['-NOZZLE_MM-'  ].Update(visible = True)  

        # Check if input values are legal
        if not isnumber(values['-WIDTH-']):
            window['-WIDTH-'].Update(values['-WIDTH-'][:-1])
        if not isnumber(values['-HEIGHT-']):
            window['-HEIGHT-'].Update(values['-HEIGHT-'][:-1])
        if not isnumber(values['-NOZZLE-']):
            window['-NOZZLE-'].Update(values['-NOZZLE-'][:-1])
        
        if event == '-WIDTH-CLICK-' or event == '-HEIGHT-CLICK-' or event == '-NOZZLE-CLICK-' or event == '-WIDTH-ENTER-' or event == '-HEIGHT-ENTER-':
            if temp != event and temp:
                # Adjust height to maintain original aspect ratio
                if temp == '-WIDTH-CLICK-' and len(values['-WIDTH-']) > 0:
                    height = round( float(values['-WIDTH-']) * img.size[1] / img.size[0], 2 )
                    window['-HEIGHT-'].Update(height)
                    values['-HEIGHT-'] = str(height)
                # Adjust width to maintain original aspect ratio
                if temp == '-HEIGHT-CLICK-' and len(values['-HEIGHT-']) > 0:
                    width = round( float(values['-HEIGHT-']) * img.size[0] / img.size[1], 2 )
                    window['-WIDTH-'].Update(width)
                    values['-WIDTH-'] = str(width)

            if event != '-WIDTH-ENTER-' or event != '-HEIGHT-ENTER-' or event != '-NOZZLE-CLICK-':
                temp = event

        if len(values['-WIDTH-']) > 0 and len(values['-HEIGHT-']) > 0 and len(values['-NOZZLE-']) > 0:
            window['-GENERATE-'   ].Update(visible = True)

        if event == '-GENERATE-':
            width, height = ( float(values['-WIDTH-']),  float(values['-HEIGHT-']))
            rows          = int( height / (float(values['-NOZZLE-']) * 2) )                    # Auto resizing image pixels per row
            cols          = int( rows * height / width )                                       # Auto resizing image pixels per column
            img           = img.resize( (cols, rows) )                                         # Resizes the image with the previous values
            pixels        = img.load()                                                         # Loads the image data into pixels
            pixels        = [ [pixels[x, y] / 255 for x in range(cols)] for y in range(rows) ] # Converts the image data into a normalized list of lists
        
            # Calculates the average of every pixel in the image
            average = sum(pixel for row in pixels for pixel in row) / (cols * rows)

            # Converts the image into a normalized height map
            height_map = getHeightMap(pixels, average)
        
            # Mesh variables
            thickness = width / 40                                                                             # Solid mesh thickness
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
            surface.save(f"{values['-FOLDER-']}/{values['-FILE-'].split('/')[-1].split('.')[0]}.stl")
            window['-GENERATED_TEXT-'].Update(visible = True)  

    window.close()

if __name__ == '__main__':
    main()
