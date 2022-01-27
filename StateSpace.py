import random
import os
import time
import string

debug = False

class StateSpace:
    def __init__(self, width, height, init_type = "random"):
        self.width = width # number of columns
        self.height = height # number of rows

        if init_type == "random":
            self.state_space = self.rand_state_init()
        elif init_type == "dead":
            self.state_space = self.dead_state_init()
        elif init_type == "user":
            self.state_space = None

        self.x_max = height-1 # bottom-most x coordinate in graph
        self.y_max = width-1 # right-most y coordinate in graph


    def rand_state_init(self):
        # generates and returns a randomly initiated "mixed" or "dead and alive" 
        # state_space of dimensions width*height
        state_space = []
        for i in range (self.height):
            row = []
            for j in range(self.width):
               row.append(random.randint(0,1))
            
            state_space.append(row)
        return state_space


    def dead_state_init(self):
        # generates and returns a fully "dead" state_space of dimensions width*height
        state_space = []
        for i in range (self.height):
            row = []
            for j in range(self.width):
                row.append(0)
            state_space.append(row)
        return state_space


    def build_neighborhood(self, x, y):
    # x -> height coordinate, 
    # y -> width coordinate
        neigborhood_map = [[[x-1, y-1], [x-1, y+0], [x-1, y+1]], 
                           [[x+0, y-1], [x+0, y+0], [x+0, y+1]],
                           [[x+1, y-1], [x+1, y+0], [x+1, y+1]]]
        if x == 0:
            neigborhood_map = neigborhood_map[1::]
        elif x == self.x_max:
            neigborhood_map = neigborhood_map[0:-1]
        if y == 0: 
            for i in neigborhood_map:
                del i[0]
        elif y == self.y_max:
            for i in neigborhood_map:
                del i[-1]
        return neigborhood_map

        # once the neighborhood map is returned 
        # the program needs to iterate between every list within the list within the list 
        # so n_x_coord=[i][j][0] and n_y_coord=[i][j][1]
        # thus if state_space[n_x_coord][n_y_coord] == 1 AND not [x,y] 
        #  then the count for state_space[x][y] += 1


    def cell_growth(self, x, y):
    # takes cell coordinates [x][y] and produces a map of its neighborhood
    # before counting all of the nieghbors present around it
    # if 

    # x being the height coordinate, 
    # y being the width coordinate
        cell = self.state_space[x][y]

        # generating coordinates for all neighbors
        neigborhood_map = [
            [[x-1, y-1], [x-1, y+0], [x-1, y+1]], 
            [[x+0, y-1], [x+0, y+0], [x+0, y+1]],
            [[x+1, y-1], [x+1, y+0], [x+1, y+1]]
        ]

        if x == 0:
        # north of neighborhood removed if cell is touching top wall of grid
            neigborhood_map = neigborhood_map[1::]
        elif x == self.x_max:
        # south of neighborhood removed if cell is touching top wall of grid
            neigborhood_map = neigborhood_map[0:-1]
        if y == 0: 
        # east of neighborhood removed if cell is touching left wall
            for i in neigborhood_map:
                del i[0]
        elif y == self.y_max:
        # west of neighborhood removed if cell is touching left wall
            for i in neigborhood_map:
                del i[-1]

        if debug == True:
            for n in neigborhood_map:
                print(*n) 
            for i in neigborhood_map:
                for n in i:
                    print(n[0], n[1]) # easy access to coordinates.
        
        neighborcount = 0
        for i in neigborhood_map:
                for n in i:
                    n_x = n[0] # height coordinate for neighbor
                    n_y = n[1] # width coordinate for neighhbor
                    if self.state_space[n_x][n_y] == 1:
                        neighborcount += 1

        if cell == 1:
        # removing current cell from count
            neighborcount -= 1

        # the following logic determines whether a cell lives or dies/stays dead 
        # based off of the rules of The Game of Life

        if cell == 1 and neighborcount < 2 or neighborcount > 3:
            return 0
        elif cell == 0 and neighborcount != 3:
            return 0
        else:
            return 1 

    def run(self, iterations):
        for i in range(iterations):
            self.take_step()

    def take_step(self):
        fresh_space = self.dead_state_init()

        for i in range(self.height):
            for j in range(self.width):
                fresh_space[i][j] = self.cell_growth(i, j)
        
        self.state_space = fresh_space
        print(self.render())
        time.sleep(.2)
        cls()

    def render(self):
        render_string = ""
        for i in self.state_space:
            render_string += " || " 
            for j in i:
                if j == 1:
                    render_string += "[.]"
                else:
                    render_string += "   "
            render_string += " ||\n"
        return render_string

def cls() -> None:
    # clears screen - handy for "flipbooking" the output. 
    os.system('cls' if os.name=='nt' else 'clear')

