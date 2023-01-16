from PIL import Image
import sys

input_filename = sys.argv[1]
output_filename = input_filename.split('.')[0] + '-3d.png'
img = Image.open(input_filename)

if type(img.getpixel((0, 0))) == int:
    values = [
        [
            img.getpixel((x, y))
            for x in range(img.width)
        ]
        for y in range(img.height)
    ]
else:
    values = [
        [
            sum(img.getpixel((x, y)))
            for x in range(img.width)
        ]
        for y in range(img.height)
    ]

def normalized(values):
    max_val = max(v for row in values for v in row)
    min_val = min(v for row in values for v in row)

    return [
        [
            (v - min_val) / (max_val - min_val)
            for v in row
        ]
        for row in values
    ]

values = normalized(values)

def row2heightmap(l, inc):
    total = sum(l)
    res = [0]
    s = 0
    for x in l:
        s += x + inc
        res.append(s)
    offset = -s/2
    return [r+offset for r in res]

inc = -sum(v for row in values for v in row) / len(values) / len(values[0])
height_map = [row2heightmap(row, inc) for row in values]
height_map = normalized(height_map)

out_img = Image.new('RGB', (len(height_map[0]), len(height_map)))
for y, row in enumerate(height_map):
    for x, h in enumerate(row):
        c = int(255.5*h)
        out_img.putpixel((x, y), (c,c,c))

out_img.save(output_filename)
