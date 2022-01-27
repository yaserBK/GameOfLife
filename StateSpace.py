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


    def cell_growth(self, x, y):
    # takes cell coordinates [x][y] and produces a map of the cells neighborhood
    # x -> row position  of cell
    # y -> column position of cell
        cell = self.state_space[x][y] # cell specified through passed in parameters
        neigborhood_map = [ # a coordinate map of all cell(x,y)'s neighbors
            [[x-1, y-1], [x-1, y+0], [x-1, y+1]], 
            [[x+0, y-1], [x+0, y+0], [x+0, y+1]],
            [[x+1, y-1], [x+1, y+0], [x+1, y+1]]
        ]

        # pruning the nieghborhood based on edge cases (i.e. if cell is touching wall or vertex in the grid)
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
        
        neighborcount = 0 # variable to hold count of all existing neighbors 
        for i in neigborhood_map:
                for n in i:
                    n_x = n[0] # height coordinate for neighbor
                    n_y = n[1] # width coordinate for neighhbor
                    if self.state_space[n_x][n_y] == 1:
                        neighborcount += 1

        if cell == 1:
        # removing cell(x,y) from count. This was the easest way to not have issues with map dimensions while pruning. 
            neighborcount -= 1

        
        # Cell(x,y) either dies (0) or lives (1), based of its neighborcount 
        # within the constraints of the game of life
        if cell == 1 and neighborcount < 2 or neighborcount > 3:
        # too many or too few neighbors for a living cell to stay alive
            return 0
        elif cell == 0 and neighborcount != 3: 
        # not enough neighbors for reproduction/ a dead cell to spring to life
            return 0
        else: # all other conditions just right for reproduction. 
            return 1 

    def run(self, iterations):
    # runs the game for specified number of iterations
        for i in range(iterations):
            self.take_step() 
            print("iteration:", i) # outputs iteration count to screen. 

    def take_step(self):
    # generates next state and populates it based off of 
    # current living/dead cells and their nieghborhoods 
        fresh_space = self.dead_state_init() 
        # i -> every row in the gridworld/state_space
        for i in range(self.height):
            # j -> every column in the gridworld/state_space
            for j in range(self.width):
                fresh_space[i][j] = self.cell_growth(i, j) 
        self.state_space = fresh_space
        print(self.render())
        time.sleep(.02)
        cls()

    def render(self):
    # pretty-printing state_space to screen
        render_string = ""
        for i in self.state_space:
            render_string += " | " 
            for j in i:
                if j == 1:
                    render_string += "[.]"
                else:
                    render_string += "   "
            render_string += " |\n"
        return render_string

def cls() -> None:
# clears screen -> used to "flipbook" the output to create a video effect 
    os.system('cls' if os.name=='nt' else 'clear')

