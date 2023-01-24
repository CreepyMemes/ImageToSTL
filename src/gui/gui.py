import PySimpleGUI as sg

from gui   import layout 
from utils import image_processing as ip
from utils import mesh_processing  as mp
from utils import helper_functions as fn

class Gui:
    def __init__(self):
        # Create the gui object
        self.gui = sg.Window("ImageToSTL", layout.layout, size=(700,300), finalize=True)

        # Make window object react to pressing enter or clicking them with left mouse button
        self.gui['-WIDTH-' ].bind("<Return>",   "ENTER-")
        self.gui['-WIDTH-' ].bind("<Button-1>", "CLICK-")
        self.gui['-HEIGHT-'].bind("<Return>",   "ENTER-")
        self.gui['-HEIGHT-'].bind("<Button-1>", "CLICK-")
        self.gui['-LAYER-' ].bind("<Return>",   "ENTER-")
        self.gui['-LAYER-' ].bind("<Button-1>", "CLICK-")

        # Initialize None variables
        self.last_click = None

    # Read incoming events
    def read_event(self):
        self.event, self.values = self.gui.read()

    # Adjusts width and height to maintain the original aspect ratio
    def maintain_ratio(self):
        # Check if a click is registered 
        if self.event == '-WIDTH-CLICK-' or self.event == '-HEIGHT-CLICK-' or self.event == '-LAYER-CLICK-':
            clicked = True
        else:
            clicked = False
        
        # Adjust width to maintain original aspect ratio
        if self.event == '-HEIGHT-ENTER-':       
            self.update_width()
        elif self.last_click == '-HEIGHT-CLICK-' and clicked: 
            self.update_width()

        # Adjust height to maintain original aspect ratio
        if self.event == '-WIDTH-ENTER-':   
            self.update_height()
        elif self.last_click == '-WIDTH-CLICK-' and clicked: 
            self.update_height()

        # If a click is registered update previous click
        if clicked:
            self.last_click = self.event

    # Updates the width to maintain the original aspect ratio
    def update_width(self):
        if not fn.is_empty(self.values['-HEIGHT-']):
            self.values['-WIDTH-'] = ip.calculate_width(self.img, self.values['-HEIGHT-'])
            self.gui['-WIDTH-' ].Update(self.values['-WIDTH-' ])
     
    # Updates the height to maintain the original aspect ratio
    def update_height(self):
        if not fn.is_empty(self.values['-WIDTH-']):
            self.values['-HEIGHT-'] = ip.calculate_height(self.img, self.values['-WIDTH-'])
            self.gui['-HEIGHT-'].Update(self.values['-HEIGHT-'])

    # Reset inputs to ""
    def reset_inputs(self):
        self.values['-WIDTH-' ] = ""
        self.values['-HEIGHT-'] = ""
        self.gui['-WIDTH-' ].Update(self.values['-WIDTH-' ])
        self.gui['-HEIGHT-'].Update(self.values['-HEIGHT-'])
    
    # Shows hidden folder inputs
    def show_folder_input(self):
        self.gui['-FOLDER_TEXT-'  ].Update(visible = True)
        self.gui['-FOLDER-'       ].Update(visible = True)
        self.gui['-FOLDER_BROWSE-'].Update(visible = True)
    
    # Shows hidden text inputs
    def show_text_input(self):
        self.gui['-WIDTH_TEXT-' ].Update(visible = True)
        self.gui['-WIDTH-'      ].Update(visible = True)
        self.gui['-WIDTH_MM-'   ].Update(visible = True)
        self.gui['-HEIGHT_TEXT-'].Update(visible = True)
        self.gui['-HEIGHT-'     ].Update(visible = True)
        self.gui['-HEIGHT_MM-'  ].Update(visible = True)
        self.gui['-LAYER_TEXT-' ].Update(visible = True)
        self.gui['-LAYER-'      ].Update(visible = True)
        self.gui['-LAYER_MM-'   ].Update(visible = True)
    
    # Show button to generate the STL
    def show_generate_button(self):
        self.gui['-GENERATE-'].Update(visible = True)
    
    # Hide button to generate the STL
    def hide_generate_button(self):
        self.gui['-GENERATE-'].Update(visible = False)
    
    # Show confirmation of successful STL generation
    def show_confirmation(self):
        self.gui['-GENERATED_TEXT-'].Update(visible = True) 

    # Hide confirmation of successful STL generation
    def hide_confirmation(self):
        self.gui['-GENERATED_TEXT-'].Update(visible = False) 
    
    # Check if input values are legal, if not ignore last input
    def is_input_legal(self):
        if not fn.is_number(self.values['-WIDTH-']):
            self.gui['-WIDTH-' ].Update( self.values['-WIDTH-'][:-1]  )
        if not fn.is_number(self.values['-HEIGHT-']):
            self.gui['-HEIGHT-'].Update( self.values['-HEIGHT-'][:-1] )
        if not fn.is_number(self.values['-LAYER-']):
            self.gui['-LAYER-' ].Update( self.values['-LAYER-'][:-1]  )
    
    def is_all_present(self):
        return not fn.is_empty( self.values['-WIDTH-']) and not fn.is_empty(self.values['-HEIGHT-']) and not fn.is_empty(self.values['-LAYER-'] )

    # Opens an image and converts it to grayscale
    def open_image(self):
        self.img = ip.open_image( self.values['-FILE-'] )

    # Processes the image to generate a height map
    def process_image(self):
        # Converts all values to float from string and saves them for later mesh use
        self.width, self.height = ( float(self.values['-WIDTH-']),  float(self.values['-HEIGHT-']) )

        # Auto scales the image based on the layer height value and saves the new values for laeter mesh use
        self.cols, self.rows = ip.auto_scale_img_values( self.width, self.height, float(self.values['-LAYER-']) )
        pixels = ip.resize_img( self.img, self.cols, self.rows )

        # Generates the height map
        self.height_map = ip.get_height_map( pixels, self.cols, self.rows )

    # Processes the mesh to generate an STL model and saves it to folder
    def process_mesh(self):
        # Generates the STL mesh
        mesh = mp.get_mesh( self.cols, self.rows, self.width, self.height, self.height_map )

        # Saves the STl mesh in the selected folder
        path = f"{self.values['-FOLDER-']}/{self.values['-FILE-'].split('/')[-1].split('.')[0]}.stl"
        mp.save_stl( mesh, path )
        
    # Closes the window   
    def close_window(self):
        self.gui.close()
