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

# Check if a given string is a valid integer or float
def isnumber(num):
    # Check if the number is an integer with more than 3 digits
    if num.find('.') == -1 and len(num) > 3:
        return False
    # Check if the number is a valid float with more than 3 digits
    if num.find('.') > -1 and len(num.split('.')[0]) > 3:
        return False
    # Check if the number is a valid float with more than 2 decimals
    if num.find('.') > -1 and len(num.split('.')[1]) > 2:
        return False
    # Check if the number is an empty string
    if len(num) == 0:
        return False
    # Check if the number is a valid float with only one '.'
    if num.replace('.','',1).isdigit() and num.count('.') < 2:
        return True
