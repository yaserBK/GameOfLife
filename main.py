from StateSpace import StateSpace


# world dimensions
width = 40 # Number of columns.
height = 30 # Number of rows.

def main():
    # instantiating State Space with defined dimensions
    world = StateSpace(width, height)
    world.run(40000)

if __name__ =="__main__":
    main()
