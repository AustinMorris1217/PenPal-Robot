import numpy as np
import sys
import pictureprocess2
import letterdisplayer
from collections import deque

def w_coder():


    def findnearbys(slim_grid, x, y,currentcolornumber):
        nearbys = 0
        TM,BM,MR,ML,TR,TL,BR,BL = 0,0,0,0,0,0,0,0
        if slim_grid[y-1,x-1] == currentcolornumber:
            nearbys = nearbys + 1
            TL = currentcolornumber
        if slim_grid[y-1,x] == currentcolornumber:
            nearbys = nearbys + 1
            TM = currentcolornumber
        if slim_grid[y-1,x+1] == currentcolornumber:
            nearbys = nearbys + 1
            TR = currentcolornumber
        if slim_grid[y,x-1] == currentcolornumber:
            nearbys = nearbys + 1
            ML = currentcolornumber
        if slim_grid[y,x+1] == currentcolornumber:
            nearbys = nearbys + 1
            MR = currentcolornumber
        if slim_grid[y+1,x-1] == currentcolornumber:
            nearbys = nearbys + 1
            BL = currentcolornumber
        if slim_grid[y+1,x] == currentcolornumber:
            nearbys = nearbys + 1
            BM = currentcolornumber
        if slim_grid[y+1,x+1] == currentcolornumber:
            nearbys = nearbys + 1
            BR = currentcolornumber
           
        neararray = np.array([[TL,TM,TR],
                              [ML,None,MR],
                              [BL,BM,BR]])
        
        return neararray,nearbys



    def searchnewstart(slimmed_grid,currentcolornumber):
        foundstart = False
        grid_height, grid_width = slimmed_grid.shape
        for y in range(grid_height):
            for x in range(grid_width):
                if slimmed_grid[y,x] == currentcolornumber:
                    if slimmed_grid[y,x+1] == currentcolornumber:
                        file.write('X'+ str(x+1)+ ' ' + 'Y' + str(y) + '\n')
                        file.write('W'+str(1) + '\n')
                        slimmed_grid[y,x+1] = None
                        x = x + 1
                        foundstart = True
                        break
                    else:
                        file.write('X'+ str(x)+ ' ' + 'Y' + str(y) + '\n')
                        file.write('W'+str(1) + '\n')
                        slimmed_grid[y,x] = None
                        x = x 
                        foundstart = True
                        break
                    
            if foundstart == True:
                break
        if foundstart == False:
            x = None
            y = None
        return slimmed_grid,x,y
    



    def leavingbreadcrumbs(slimmed_grid,x,y):
        file.write('X'+ str(x)+ ' ' + 'Y' + str(y) + '\n')
        slimmed_grid[y,x] = None
        return slimmed_grid
    
    def savingsomebreadcrumbsforlater(x,y):
        file.write('X'+ str(x)+ ' ' + 'Y' + str(y) + '\n')
        return 
    
    def find_nearest_direction(previousdirection, directions,currentcolornumber):
        i = 0
        n_forward = 0
        n_backward = 0
        while True:
            if (previousdirection + i) >= len(directions):
                position = previousdirection + i - len(directions)
                if directions[position] == currentcolornumber:
                    forwardspot = position
                    break
            if (previousdirection + i) < len(directions):
                if directions[previousdirection + i] == currentcolornumber:
                    forwardspot = previousdirection + 1
                    break
            i = i + 1
            n_forward = n_forward + 1
        i = 0
        while True:
            if (previousdirection - i) < 0:
                position = previousdirection - i + len(directions)
                if directions[position] == currentcolornumber:
                    backwardspot = position
                    break
            if (previousdirection - i) >= 0:
                if directions[previousdirection - i] == None:
                    backwardspot = previousdirection - i
                    break
            i = i + 1
            n_backward = n_backward + 1

        if n_forward >= n_backward:
            directiontogo = backwardspot
        else:
            directiontogo = forwardspot
        
        return directiontogo



    hand_written_letter_filename = 'writtenletters/' + sys.argv[1]
    slimmed_grid, amount_of_colors = pictureprocess2.cluster_colors(hand_written_letter_filename)
    currentcolornumber = 1



    user_input = sys.argv[1]
    title = user_input.split('.')[0]
    file_name = f'W_code/{title}_wcode.txt'


    file = open(file_name, 'w')
    grid_height, grid_width = slimmed_grid.shape
    file.write('I'+ str(grid_width)+ ' ' + 'J' + str(grid_height) + '\n')
    file.write('W'+str(0) + '\n')
    file.write('P1' +'\n')

    bigpicture = True
    littlepicture = True

    while bigpicture == True:
        slimmed_grid,x,y = searchnewstart(slimmed_grid,currentcolornumber)
        
        if x is None:
            if currentcolornumber == amount_of_colors:
                file.write('X'+ str(0)+ ' ' + 'Y' + str(0) + '\n')
                file.write(';')
                bigpicture = False
                littlepicture = False
                break
            else:
                currentcolornumber = currentcolornumber + 1
                if currentcolornumber == amount_of_colors:
                    file.write('P0' + '\n')
                else:
                    file.write('P'+ str(currentcolornumber) + '\n')
        else:
            littlepicture = True
            
        


        previousdirection = None
        lastdirections = deque(maxlen=10)
        while littlepicture == True:
            neararray, nearbys = findnearbys(slimmed_grid,x,y,currentcolornumber)
            zero = neararray[0][1]
            one = neararray[0][2]
            two = neararray[1][2]
            three = neararray[2][2]
            four = neararray[2][1]
            five = neararray[2][0]
            six = neararray[1][0]
            seven = neararray[0][0]

            directions = [zero,one,two,three,four,five,six,seven]
            presentnumbereddirections = []
            i=0
            while i < len(directions):
                if directions[i] == currentcolornumber:
                    presentnumbereddirections.append(i)
                i = i + 1

            if nearbys == 0:
                file.write('W'+str(0) + '\n')
                littlepicture = False
                break

            
            elif (nearbys > 1) and (previousdirection == None):
                index = directions.index(currentcolornumber)
                if index == 0:
                    x=x
                    y=y-1
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 0
                    lastdirections.append(previousdirection)
                if index == 1:
                    x=x+1
                    y=y-1
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 1
                    lastdirections.append(previousdirection)
                if index == 2:
                    x=x+1
                    y=y
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 2
                    lastdirections.append(previousdirection)
                if index == 3:
                    x=x+1
                    y=y+1
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 3
                    lastdirections.append(previousdirection)
                if index == 4:
                    x=x
                    y=y+1
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 4
                    lastdirections.append(previousdirection)
                if index == 5:
                    x=x-1
                    y=y+1
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 5
                    lastdirections.append(previousdirection)
                if index == 6:
                    x=x-1
                    y=y
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 6
                    lastdirections.append(previousdirection)
                if index == 7:
                    x=x-1
                    y=y-1
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 7
                    lastdirections.append(previousdirection)




            elif (nearbys == 1):
                index = directions.index(currentcolornumber)
                if index == 0:
                    x=x
                    y=y-1
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 0
                    lastdirections.append(previousdirection)
                if index == 1:
                    x=x+1
                    y=y-1
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 1
                    lastdirections.append(previousdirection)
                if index == 2:
                    x=x+1
                    y=y
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 2
                    lastdirections.append(previousdirection)
                if index == 3:
                    x=x+1
                    y=y+1
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 3
                    lastdirections.append(previousdirection)
                if index == 4:
                    x=x
                    y=y+1
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 4
                    lastdirections.append(previousdirection)
                if index == 5:
                    x=x-1
                    y=y+1
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 5
                    lastdirections.append(previousdirection)
                if index == 6:
                    x=x-1
                    y=y
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 6
                    lastdirections.append(previousdirection)
                if index == 7:
                    x=x-1
                    y=y-1
                    slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                    previousdirection = 7
                    lastdirections.append(previousdirection)

            elif (nearbys == 3) and (previousdirection != None):
                if (previousdirection in presentnumbereddirections):
                    if previousdirection == 0:
                        x=x
                        y=y-1
                        savingsomebreadcrumbsforlater(x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 1:
                        x=x+1
                        y=y-1
                        savingsomebreadcrumbsforlater(x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 2:
                        x=x+1
                        y=y
                        savingsomebreadcrumbsforlater(x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 3:
                        x=x+1
                        y=y+1
                        savingsomebreadcrumbsforlater(x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 4:
                        x=x
                        y=y+1
                        savingsomebreadcrumbsforlater(x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 5:
                        x=x-1
                        y=y+1
                        savingsomebreadcrumbsforlater(x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 6:
                        x=x-1
                        y=y
                        savingsomebreadcrumbsforlater(x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 7:
                        x=x-1
                        y=y-1
                        savingsomebreadcrumbsforlater(x,y)
                        lastdirections.append(previousdirection)
                if (previousdirection not in presentnumbereddirections):

                    closest_value = find_nearest_direction(previousdirection,directions,currentcolornumber)

                    if closest_value == 0:
                        x=x
                        y=y-1
                        savingsomebreadcrumbsforlater(x,y)
                        previousdirection = 0
                        lastdirections.append(previousdirection)
                    if closest_value == 1:
                        x=x+1
                        y=y-1
                        savingsomebreadcrumbsforlater(x,y)
                        previousdirection = 1
                        lastdirections.append(previousdirection)
                    if closest_value == 2:
                        x=x+1
                        y=y
                        savingsomebreadcrumbsforlater(x,y)
                        previousdirection = 2
                        lastdirections.append(previousdirection)
                    if closest_value == 3:
                        x=x+1
                        y=y+1
                        savingsomebreadcrumbsforlater(x,y)
                        previousdirection = 3
                        lastdirections.append(previousdirection)
                    if closest_value == 4:
                        x=x
                        y=y+1
                        savingsomebreadcrumbsforlater(x,y)
                        previousdirection = 4
                        lastdirections.append(previousdirection)
                    if closest_value == 5:
                        x=x-1
                        y=y+1
                        savingsomebreadcrumbsforlater(x,y)
                        previousdirection = 5
                        lastdirections.append(previousdirection)
                    if closest_value == 6:
                        x=x-1
                        y=y
                        savingsomebreadcrumbsforlater(x,y)
                        previousdirection = 6
                        lastdirections.append(previousdirection)
                    if closest_value == 7:
                        x=x-1
                        y=y-1
                        savingsomebreadcrumbsforlater(x,y)
                        previousdirection = 7
                        lastdirections.append(previousdirection)



            elif (nearbys > 1) and (previousdirection != None):
                if (previousdirection in presentnumbereddirections):
                    if previousdirection == 0:
                        x=x
                        y=y-1
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 1:
                        x=x+1
                        y=y-1
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 2:
                        x=x+1
                        y=y
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 3:
                        x=x+1
                        y=y+1
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 4:
                        x=x
                        y=y+1
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 5:
                        x=x-1
                        y=y+1
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 6:
                        x=x-1
                        y=y
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        lastdirections.append(previousdirection)
                    if previousdirection == 7:
                        x=x-1
                        y=y-1
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        lastdirections.append(previousdirection)
                if (previousdirection not in presentnumbereddirections):

                    closest_value = find_nearest_direction(previousdirection,directions,currentcolornumber)


                    if closest_value == 0:
                        x=x
                        y=y-1
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        previousdirection = 0
                        lastdirections.append(previousdirection)
                    if closest_value == 1:
                        x=x+1
                        y=y-1
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        previousdirection = 1
                        lastdirections.append(previousdirection)
                    if closest_value == 2:
                        x=x+1
                        y=y
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        previousdirection = 2
                        lastdirections.append(previousdirection)
                    if closest_value == 3:
                        x=x+1
                        y=y+1
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        previousdirection = 3
                        lastdirections.append(previousdirection)
                    if closest_value == 4:
                        x=x
                        y=y+1
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        previousdirection = 4
                        lastdirections.append(previousdirection)
                    if closest_value == 5:
                        x=x-1
                        y=y+1
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        previousdirection = 5
                        lastdirections.append(previousdirection)
                    if closest_value == 6:
                        x=x-1
                        y=y
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        previousdirection = 6
                        lastdirections.append(previousdirection)
                    if closest_value == 7:
                        x=x-1
                        y=y-1
                        slimmed_grid = leavingbreadcrumbs(slimmed_grid,x,y)
                        previousdirection = 7
                        lastdirections.append(previousdirection)

            
            

    file.close()



w_coder()