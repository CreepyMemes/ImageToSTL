from gui.gui import Gui

def main(): 
    # Create the window object
    window = Gui()
   
    while True:
        # Read incoming events
        window.read()

        # Event if window is closed
        if window.event == None:
            break
        
        # Event if a new image is entered
        if window.event == '-FILE-':
            window.open_image()        # Opens the image and converts it to grayscale
            window.show_folder_input() # Unhides folder inputs
            window.hide_confirmation() # Hides generation confirmation
            window.reset_inputs()      # Resets width and height

        # if the folder is changed
        if window.event == '-FOLDER-':       
            window.show_text_input()   # Unhides text inputs 
            window.hide_confirmation() # Hides generation confirmation
 
        window.is_input_legal() # Checks if input values are legal
        window.maintain_ratio() # Adjusts width and height to maintain the original aspect ratio

        # If width, height, and layer height values are all entered, a button to generate the STL is shown
        if window.is_all_present():
            window.show_generate_button()
        else:
            window.hide_generate_button()

        # Event if Generate STL button is pressed
        if window.event == '-GENERATE-':         
            window.process_image()     # Processes the image to generate a height map    
            window.process_mesh()      # Creates and processes a mesh to generate an STL model
            window.show_confirmation() # Print a confirmation to generating the STL file

    window.close_window()

if __name__ == '__main__':
    main()
