import struct as st
from math import sin, cos, pi


def bmp_header(width, height):
    filetype = 4*16**3+13*16**2+4*16+2  # 4D 42 - BM
    reserved1 = 0
    reserved2 = 0
    offset = 62
    file_size = width * height + offset
    return st.pack('<HL2HL', filetype, file_size, reserved1, reserved2, offset)


def image_info_data(width, height):
    header_size = 40
    image_width = width
    image_height = height
    planes = 1
    bits_per_pixel = 8
    compression = 0
    image_size = 0
    x_pixels_per_meter = 0
    y_pixels_per_meter = 0
    total_colors = 2
    important_colors = 0
    return st.pack('<3L2H6L', header_size, image_width, image_height, planes, bits_per_pixel, compression,
                   image_size, x_pixels_per_meter, y_pixels_per_meter, total_colors, important_colors)


def color_palette():
    black = (0, 0, 0, 0)
    white = (255, 255, 255, 0)
    return st.pack('<8B', *black, *white)


width = 500
height = 500
function_pixels = []
t = 0
increase = 0.005
x_min = float('inf')
y_min = float('inf')

while t <= pi * 10:
    x = round((cos(t)+cos(6.2*t)/6.2), 2)
    if x < x_min:
        x_min = x
    y = round((sin(t)-sin(6.2*t)/6.2), 2)
    if y < y_min:
        y_min = y
    function_pixels.append((x, y))
    t += increase

with open('formula.BMP', 'wb') as file:
    file.write(bmp_header(width, height))
    file.write(image_info_data(width, height))
    file.write(color_palette())
    y_of_pixel = y_min
    for i in range(height):
        x_of_pixel = x_min
        for j in range(width):
            if (x_of_pixel, y_of_pixel) in function_pixels:
                file.write(st.pack('<B', 0))
            else:
                file.write(st.pack('<B', 1))
            x_of_pixel = round(x_of_pixel + increase, 3)
        y_of_pixel = round(y_of_pixel + increase, 3)
