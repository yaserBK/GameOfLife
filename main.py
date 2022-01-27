from StateSpace import StateSpace


# Grid dimensions
width = 40
height = 30

def main():
    # instantiating State Space with defined 
    world = StateSpace(width, height)
    world.run(40000)

if __name__ =="__main__":
    main()
