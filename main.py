from StateSpace import StateSpace

def main():
    # world = StateSpace(len(user_state[0]), len(user_state), "user")
    # world.state_space = user_state
    world = StateSpace(40,60)
    world.run(40000)
    #  # printing neighborhood to output for sake of testing        
if __name__ =="__main__":
    main()
