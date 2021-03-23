import Advanced_Agent, Basic_Agent
import Extra_Credit_AA as Extra_Credit
import sys

'''
Run_Agent Main Driver

Description: Driver to initate the agent that the user wants to start via:
    1. ba for the basic agent
    2. aa for the advanced agent
    3. ec for the extra credit
All for the third argument given in the terminal.
'''

if __name__ == "__main__":

    # the driver needs 4 arguments to start otherwise it will exit with failure
    if len(sys.argv) != 4:
        print("Usage Error:")
        print("For the basic agent: python Run_Agent.py <dimension of board> <mine density> ba")
        print("For the advance agent: python Run_Agent.py <dimension of board> <mine density> aa")
        print("For the advance agent (Extra Credit): python Run_Agent.py <dimension of board> <mine density> ec")
        sys.exit(1)

    # check if the third argument is "ba" to start the basic agent
    if sys.argv[3] == "ba":
        Basic_Agent.start_basic_agent(int(sys.argv[1]), int(sys.argv[2]))
    
    # check if the third argument is "aa" to start the advanced agent
    if sys.argv[3] == "aa":
        Advanced_Agent.start_advance_agent(int(sys.argv[1]), int(sys.argv[2]))

    # check if the third argument is "ec" to start the extra credit utilizing the advanced agent
    if sys.argv[3] == "ec":
        Extra_Credit.start_ec_agent(int(sys.argv[1]), int(sys.argv[2]))