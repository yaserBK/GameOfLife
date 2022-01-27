from StateSpace import StateSpace


# Grid dimensions
width = 40
height = 60

def main():
    world = StateSpace(width, height)
    world.run(40000)

if __name__ =="__main__":
    main()
