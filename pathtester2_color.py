import numpy as np
import letterdisplayer
import sys

title = sys.argv[1]
file_name = f'W_code/{title}_wcode.txt'



def reconstruct(file_name):
    w_code = open(file_name, 'r')
    first_line = w_code.readline()
    dimensions = first_line.split()
    grid_width = int(dimensions[0][1:])
    grid_height = int(dimensions[1][1:])
    rebuilt_grid = np.zeros((grid_height,grid_width))
    w_code.close()

    colornumber = 0
    with open(file_name, 'r') as w_code:
        for line in w_code:
            if line[0] == 'I':
                pass

            elif line[0] == 'P':
                colornumber = colornumber + 1

            elif line[0] == 'W':
                if line[1] == '0':
                    #pass
                    letterdisplayer.show_digital_color_image(rebuilt_grid)

            elif line[0] == 'X':
                position = line.split()
                x_position = int(position[0][1:])
                y_position = int(position[1][1:])
                rebuilt_grid[y_position,x_position] = colornumber


    letterdisplayer.show_digital_color_image(rebuilt_grid)
reconstruct(file_name)

