from PIL import Image

# Opens an image and converts to grayscale
def open_image(file):
    img = Image.open(file).convert('L')
    return img

# Calculate height value to maintain the original aspect ratio
def calculate_height(img, width):
    return str( round( float(width) * img.size[1] / img.size[0], 2 ) )

# Calculate width value to maintain the original aspect ratio
def calculate_width(img, height):
    return str( round( float(height) * img.size[0] / img.size[1], 2 ) )

# Get new pixel rows and columns values for auto scaling
def auto_scale_img_values(width, height, layer):
    rows = int( height / layer )
    cols = int( rows * height / width )
    return ( cols, rows )

# Resizes the image,and loads it to a normalized list of lists 
def resize_img(img, cols, rows):
    img    = img.resize( (cols, rows) ) 
    pixels = img.load() 
    return [ [pixels[x, y] / 255 for x in range(cols)] for y in range(rows) ] 

# Normalizes a list of lists to the range [0, 1]
def normalize(pixels):
    max_pix = max( pixel for row in pixels for pixel in row )
    min_pix = min( pixel for row in pixels for pixel in row )
    return [ [(pixel - min_pix) / (max_pix - min_pix) for pixel in row] for row in pixels ]

# Calculates the average of every pixel in the image
def get_average(pixels, cols, rows):
    return sum(pixel for row in pixels for pixel in row) / (cols * rows)

# Converts a row of the image into a height map with the average value of all pixels give as an argument
def get_row_height_map(row, average):
    result = []
    total  = 0
    for pixel in row:
        total += pixel - average
        result.append(total)
    return [ pixel - total/2 for pixel in result ]

# Converts a whole image into a height map
def get_height_map(pixels, cols, rows):
    average = get_average(pixels, cols, rows)
    return normalize( [ get_row_height_map(row, average) for row in pixels ] )
    
