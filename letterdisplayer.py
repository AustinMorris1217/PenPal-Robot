import numpy as np
from PIL import Image
def show_image(image_array):

    letter_grid_height, letter_grid_width = np.shape(image_array)
    test_image = Image.new("RGB", (letter_grid_width, letter_grid_height), color=(255, 255, 255))
    

    for y in range(letter_grid_height):
        for x in range(letter_grid_width):
            if image_array[y,x] == 1:
                test_image.putpixel((x,y),(0,0,0))
    test_image.show()


def show_neg_image(image_array):
    letter_grid_height, letter_grid_width = np.shape(image_array)
    test_image = Image.new("RGB", (letter_grid_width, letter_grid_height), color=(255, 255, 255))
    
    normal_array = image_array/np.max(image_array)

    for y in range(letter_grid_height):
        for x in range(letter_grid_width):
            pixel_value = int(255*(1-normal_array[y,x])),int(255*(1-normal_array[y,x])),int(255*(1-normal_array[y,x]))
            test_image.putpixel((x,y),pixel_value)
    test_image.show()

def show_color_image(image_array):
    letter_grid_height, letter_grid_width, letter_grid_depth = np.shape(image_array)
    test_image = Image.new("RGB", (letter_grid_width, letter_grid_height), color=(255, 255, 255))
    

    for y in range(letter_grid_height):
        for x in range(letter_grid_width):
            [r,g,b] = image_array[y][x]
            test_image.putpixel((x,y),(r,g,b))
    test_image.show()

def show_digital_color_image(image_array):
    letter_grid_height, letter_grid_width = np.shape(image_array)
    test_image = Image.new("RGB", (letter_grid_width, letter_grid_height), color=(255, 255, 255))
    


    for y in range(letter_grid_height):
        for x in range(letter_grid_width):
            if image_array[y,x] == 1:
                test_image.putpixel((x,y),(0,0,0))
            if image_array[y,x] == 2:
                test_image.putpixel((x,y),(255,0,0))
            if image_array[y,x] == 3:
                test_image.putpixel((x,y),(0,255,0))
            if image_array[y,x] == 4:
                test_image.putpixel((x,y),(0,0,255)) 
            if image_array[y,x] == 5:
                test_image.putpixel((x,y),(255,255,0))
            if image_array[y,x] == 6:
                test_image.putpixel((x,y),(0,255,255)) 
            if image_array[y,x] == 7:
                test_image.putpixel((x,y),(255,165,0))
    test_image.show()