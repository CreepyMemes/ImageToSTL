from gui.gui import Gui

def main(): 
    # Create the window object
    window = Gui()
   
    while True:
        # Read incoming events
        window.read()

        # Event if the window is closed
        if window.event == None:
            break
        
        # Event if a new image is selected
        if window.event == '-FILE-':
            window.open_image()
            window.show_folder_input()
            window.reset_inputs() # Resets width and height
            window.hide_confirmation()

        # Event if a new folder is selected
        if window.event == '-FOLDER-':       
            window.show_text_input()
            window.hide_confirmation() 
 
        window.is_input_legal() # Checks if input values are legal
        window.maintain_ratio() # Adjusts width and height to maintain the original aspect ratio

        # If width, height, and layer height values are all entered, a button to generate the STL is shown
        if window.is_all_present():
            window.show_generate_button()
        else:
            window.hide_generate_button()

        # Event if Generate STL button is pressed
        if window.event == '-GENERATE-':         
            window.process_image() # Generates a height map
            window.process_mesh()  # Generates the STL model
            window.show_confirmation()

    window.close_window()

if __name__ == '__main__':
    main()
