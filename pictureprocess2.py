import numpy as np
from PIL import Image
from skimage.morphology import skeletonize
import letterdisplayer
import cv2
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

def detect_colors(pixel, threshold, factor):
        
    average = (pixel[0] + pixel[1] + pixel[2]) / 3 
    if factor*average < threshold:
        return True
    else:
        return False

def make_black_or_white(letter_filename):
    
    threshold = 250
    factor = 1.2

    written_letter = Image.open(letter_filename) 
    image_width, image_height = written_letter.size 
    letter_grid = np.zeros((image_height, image_width)) 
    
    for y in range(image_height): 
        for x in range(image_width): 
            input_pixel = written_letter.getpixel((x, y)) 
            if detect_colors(input_pixel, threshold, factor):
                letter_grid[y,x] = 1 
                
            else:
                letter_grid[y,x] = 0 

    return letter_grid



def simplify(letter_filename):
    written_letter_grid = make_black_or_white(letter_filename)
    slimmed_grid = skeletonize(written_letter_grid)

    grid_height, grid_width = slimmed_grid.shape
    new_slimmed_grid = np.zeros((grid_height,grid_width))
    for y in range(grid_height): 
        for x in range(grid_width): 
            if slimmed_grid[y,x] == True:
                new_slimmed_grid[y,x] = 1
            else:
                new_slimmed_grid[y,x] = 0
    letterdisplayer.show_image(new_slimmed_grid)
    return new_slimmed_grid







def rgb_to_lab(color): 
    rgb = np.array([[color]], dtype=np.uint8) 
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    return lab[0][0] 

def color_distance(color1, color2): 

    lab1 = rgb_to_lab(color1).astype(np.int32)  
    lab2 = rgb_to_lab(color2).astype(np.int32)

   
    rgb1 = np.array(color1, dtype=np.int32)
    rgb2 = np.array(color2, dtype=np.int32)

    rgb_distance = np.sqrt(np.sum((rgb1 - rgb2) ** 2))
    lab_distance = np.sqrt(np.sum((lab1 - lab2) ** 2))
    
    return lab_distance

 
def rgb_to_color_name(r, g, b):
    # Dictionary of general color names and their RGB ranges
    colors = {
        "Red": [(150, 0, 0), (255, 100, 100)],
        "Green": [(0, 150, 0), (100, 255, 100)],
        "Blue": [(0, 0, 150), (100, 100, 255)],
        "Yellow": [(150, 150, 0), (255, 255, 100)],
        "Cyan": [(0, 150, 150), (100, 255, 255)],
        "Magenta": [(150, 0, 150), (255, 100, 255)],
        "Black": [(0, 0, 0), (50, 50, 50)],
        "White": [(200, 200, 200), (255, 255, 255)],
        "Gray": [(100, 100, 100), (200, 200, 200)]
    }
    
    for color, (low, high) in colors.items():
        if low[0] <= r <= high[0] and low[1] <= g <= high[1] and low[2] <= b <= high[2]:
            return color
    return "Unknown color"






def only_take_what_you_need(letter_filename):
    original_color_image = Image.open(letter_filename)
    simplified_black_white_image = simplify(letter_filename)
    grid_height, grid_width = simplified_black_white_image.shape
    simplified_color_image = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)


    for y in range(grid_height): 
        for x in range(grid_width): 
            if simplified_black_white_image[y,x] == 1:
                input_pixel = original_color_image.getpixel((x, y))
                simplified_color_image[y,x] = input_pixel
            else:
                simplified_color_image[y,x] = [255,255,255]

    
    return simplified_color_image



def cluster_colors(letter_filename, threshold=75):

    simplified_color_image = only_take_what_you_need(letter_filename)

   
    image_height, image_width, image_depth = simplified_color_image.shape 

    colordictionary = {}
    color_number_grid = np.zeros((image_height, image_width)) 
    color_num = -1


    for y in range(image_height):
        for x in range(image_width):
            foundit = False
            input_pixel = tuple(simplified_color_image[y, x])  

            for key in colordictionary:
                if color_distance(input_pixel, key) < threshold:
                    color_number_grid[y,x] = colordictionary.get(key)
                    foundit = True
                    break
            if foundit == False:
                color_num = color_num + 1
                colordictionary[input_pixel] = color_num
                color_number_grid[y,x] = color_num

    amount_of_colors = len(colordictionary)
    print(colordictionary)
    print(f"Detected colors: {len(colordictionary)}")
    

    letterdisplayer.show_digital_color_image(color_number_grid)
    return color_number_grid, amount_of_colors        

