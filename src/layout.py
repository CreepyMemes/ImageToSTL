import PySimpleGUI as sg

# Window black theme
sg.ChangeLookAndFeel('black')

# Main window layout
layout = [
    [ 
        sg.Text('Select an image:', size = (20,  1)),
        sg.In(size = (40, 1), key='-FILE-', enable_events = True),
        sg.FileBrowse() 
    ],

    [ 
        sg.Text('Folder to save your STL:',  size = (20,  1), key='-FOLDER_TEXT-', visible=False), 
        sg.In(size = (40, 1), key='-FOLDER-', enable_events = True, visible=False), 
        sg.FolderBrowse(key='-FOLDER_BROWSE-', visible=False) 
    ],

    [ 
        sg.Text() 
    ],

    [ 
        sg.Text('Width:', size = (15, 1), key="-WIDTH_TEXT-", visible=False,), 
        sg.In(size = (7, 1), key="-WIDTH-", enable_events = True, visible=False),
        sg.Text('mm', key="-WIDTH_MM-", visible=False)  
    ],

    [ 
        sg.Text('Height:', size = (15, 1), key="-HEIGHT_TEXT-", visible=False,),  
        sg.In(size = (7, 1), key='-HEIGHT-', enable_events = True, visible=False), 
        sg.Text('mm', visible=False, key="-HEIGHT_MM-") 
    ],

    [ 
        sg.Text('Layer Height:', size = (15, 1), key="-NOZZLE_TEXT-", visible=False,),  
        sg.In(size = (7, 1), key='-NOZZLE-', enable_events = True, default_text="0.2", visible=False), 
        sg.Text('mm', key="-NOZZLE_MM-", visible=False) 
    ],

    [ 
        sg.Text() 
    ],

    [ 
        sg.Button('Generate STL!', key="-GENERATE-", visible=False), 
        sg.Text('STL File Generated!', key="-GENERATED_TEXT-", visible=False)
    ]
]
