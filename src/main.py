from gui.gui import Gui

def main(): 
    window = Gui()

    while True:
        window.read_event()
        
        # Event if the window is closed
        if window.event == None:
            break
        
        # Event if a new image is selected
        if window.event == '-FILE-':
            window.open_image()
            window.show_folder_input()
            window.reset_inputs() # Resets width and height

        # Event if a new folder is selected
        if window.event == '-FOLDER-':       
            window.show_text_input()

        window.is_input_legal()    # Ignores last input value if it's illegal
        window.maintain_ratio()    # Adjusts width and height to maintain the original aspect ratio
        window.hide_confirmation() # Hides confirmation text if any event is read

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
