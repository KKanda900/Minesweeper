import numpy, math, random, sys
from collections import defaultdict, deque

'''
Basic_Agent Class
Description: A class that holds all the information for the Basic Agent and its logic.
'''

q = []  # stack of all the neighbors of a cell that has clue value of 0
numbers = deque()  # queue of all the neighbors of a cell that has clue value of 0, these neighbors have a clue value of > 0

class Basic_Agent:
    
    dim = 10  # define a blank dimension size for the start
    # define a blank board for the start (with the placements)
    board = numpy.zeros((dim, dim), dtype=object)
    # this is the board that the agent is going to use to solve
    bot_board = numpy.zeros((dim, dim), dtype=object)  # a board to keep track of what the agent knows on the board
    mines = 0  # default value for the number of mines to be placed
    possible_coordinates = []  # lists all the possible coordinates for the board
    visited = 0  # keeps track of the cells visited in the basic agent
    # Mine Dictionary Representation: {"open": T/F, "nghbr": num, "mine": T/F}
    # can use the mine_dict by mine_dict[x][y][key] where x and y are coordinates and key the value you want in return
    # initialize the beginning of the board for when we have to build it
    mine_dict = defaultdict(dict)

    # initiizes the board upon starting the program
    def __init__(self, dim, mines):
        self.dim = dim  # set the dim size for the board
        # initialize one board to keep track of the mines, clues and empty spaces
        self.board = numpy.zeros((self.dim, self.dim), dtype=object)
        # initialize one board for the agent to go thru and reveal
        self.bot_board = numpy.zeros((self.dim, self.dim), dtype=object)
        # this is to check if the user might of initialized too many mines on the board
        if mines < self.dim * self.dim:
            self.mines = mines
        else:
            print("Can't have more mines then spots in the maze")
            sys.exit(1)
        # after setup on top we can proceed to build the actual board
        self.build_board()

    # check if what you are checking is within the constraints of the board
    def check_constraints(self, ind1, ind2):
        if ind1 >= 0 and ind1 <= self.dim - 1 and ind2 >= 0 and ind2 <= self.dim - 1:
            return True

        return False

    # using the information from the initilization step proceed to build the board with the mines information and the agent's board
    def build_board(self):
        dim_array = list(range(0, self.dim))
        mines = self.mines
        while mines != 0:
            i = random.choice(dim_array)
            j = random.choice(dim_array)
            arr = [0, 1]  # these will represent random choices
            if random.choice(arr) == 0 and mines != 0 and self.board[i][j] == 0:
                self.board[i][j] = 'm'
                mines -= 1

        for i in range(0, self.dim):
            for j in range(0, self.dim):
                count = 0
                self.bot_board[i][j] = ' '
                if self.board[i][j] == 0:
                    # check the up direction
                    if self.check_constraints(i - 1, j) and self.board[i - 1][j] == 'm':
                        count += 1
                    # check the down direction
                    if self.check_constraints(i + 1, j) and self.board[i + 1][j] == 'm':
                        count += 1
                    # check the left direction
                    if self.check_constraints(i, j - 1) and self.board[i][j - 1] == 'm':
                        count += 1
                    # check the right direction
                    if self.check_constraints(i, j + 1) and self.board[i][j + 1] == 'm':
                        count += 1
                    # check the upper left region
                    if self.check_constraints(i - 1, j - 1) and self.board[i - 1][j - 1] == 'm':
                        count += 1
                    # check the upper right region
                    if self.check_constraints(i - 1, j + 1) and self.board[i - 1][j + 1] == 'm':
                        count += 1
                    # check the bottom left region
                    if self.check_constraints(i + 1, j - 1) and self.board[i + 1][j - 1] == 'm':
                        count += 1
                    # check the bottom right region
                    if self.check_constraints(i + 1, j + 1) and self.board[i + 1][j + 1] == 'm':
                        count += 1

                    # if the count is 0 don't write a hint otherwise write the hint
                    if count == 0:
                        self.board[i][j] = ' '
                    else:
                        self.board[i][j] = str(count)

    # initializes all the possible coordinates for a given dimension (d)
    def coordinate_init(self):
        possible_x = list(range(0, self.dim))  # obtain all the x values
        possible_y = list(range(0, self.dim))  # obtain all the y values
        # iterate through each x value and add the corresponding y value
        for i in range(0, len(possible_x)):
            for j in range(0, len(possible_y)):
                self.possible_coordinates.append((possible_x[i], possible_y[j]))

    # Initialize the dictionary to keep track of what's opened and at which cells there is a mine
    def dictionary_init(self):  
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                self.mine_dict[i][j] = {"open": False, "mine": False} # sample of how the dictionary is represented

    # Counts all the neighbor mines at a given cell to keep track of local information
    def neighbor_count(self, x, y):
        count = 0 # holds the count for the amount of neighbor mines 
        if x != 0:
            if y != 0:
                if self.bot_board[x - 1][y - 1] == 'm':  # top left
                    count += 1
            if self.bot_board[x - 1][y] == 'm':  # up
                count += 1
            if x + 1 < self.dim and y + 1 < self.dim:
                if self.bot_board[x + 1][y + 1] == 'm':  # top right
                    count += 1

        if y + 1 < self.dim and x + 1 < self.dim:
            if self.bot_board[x][y + 1] == 'm':  # right
                count += 1
            if x < self.dim:
                if self.bot_board[x - 1][y + 1] == 'm':  # bottom right
                    count += 1

        if x - 1 <= 0:
            if self.bot_board[x + 1][y] == 'm':  # bottom
                count += 1
            if y != 0:
                if self.bot_board[x + 1][y - 1] == 'm':  # bottom left
                    count += 1
            if y != 0:
                if self.bot_board[x][y - 1] == 'm':  # left
                    count += 1

        return count

    # check the bot_board to check if there is a neighbor that is already marked as a mine by the agent
    def mine_updater(self, i, j):
        count = 0  # keeps track of the number of mines at a given index value
        # check the up direction for a mine
        if self.check_constraints(i + 1, j):
            if self.bot_board[i + 1][j] == 'm':
                count += 1
        # check the down direction for a mine
        if self.check_constraints(i - 1, j):
            if self.bot_board[i - 1][j] == 'm':
                count += 1
        # check the left direction for a mine
        if self.check_constraints(i, j + 1):
            if self.bot_board[i][j + 1] == 'm':
                count += 1
        # check the right direction for a mine
        if self.check_constraints(i, j - 1):
            if self.bot_board[i][j - 1] == 'm':
                count += 1
        # check the upper left region for a mine
        if self.check_constraints(i - 1, j - 1):
            if self.bot_board[i - 1][j - 1] == 'm':
                count += 1
        # check the upper right region for a mine
        if self.check_constraints(i - 1, j + 1):
            if self.bot_board[i - 1][j + 1] == 'm':
                count += 1
        # check the bottom left region for a mine
        if self.check_constraints(i + 1, j - 1):
            if self.bot_board[i + 1][j - 1] == 'm':
                count += 1
        # check the bottom right region for a mine
        if self.check_constraints(i + 1, j + 1):
            if self.bot_board[i + 1][j + 1] == 'm':
                count += 1

        return count

    # A function to build an equation given a cell location by looking at how many of it's neighbors are not opened
    def build_eq(self, one):
        x = one[0]  # x corresponds to the first element in the one array
        y = one[1]  # y corresponds to the second element in the array
        z = []  # to assist in building the equation at the end
        # to account for any solved mines in the neighbors
        value = int(self.bot_board[x][y]) - self.mine_updater(x, y)
        # down direction
        if self.check_constraints(x + 1, y) and self.mine_dict[x + 1][y]["open"] is False:
            z.append((x + 1, y))
        # up direction
        if self.check_constraints(x - 1, y) and self.mine_dict[x - 1][y]["open"] is False:
            z.append((x - 1, y))
        # right direction
        if self.check_constraints(x, y + 1) and self.mine_dict[x][y + 1]["open"] is False:
            z.append((x, y + 1))
        # left direction
        if self.check_constraints(x, y - 1) and self.mine_dict[x][y - 1]["open"] is False:
            z.append((x, y - 1))
        # bottom right direction
        if self.check_constraints(x + 1, y + 1) and self.mine_dict[x + 1][y + 1]["open"] is False:
            z.append((x + 1, y + 1))
        # bottom left direction
        if self.check_constraints(x + 1, y - 1) and self.mine_dict[x + 1][y - 1]["open"] is False:
            z.append((x + 1, y - 1))
        # upper left direction
        if self.check_constraints(x - 1, y - 1) and self.mine_dict[x - 1][y - 1]["open"] is False:
            z.append((x - 1, y - 1))
        # upper right direction
        if self.check_constraints(x - 1, y + 1) and self.mine_dict[x - 1][y + 1]["open"] is False:
            z.append((x - 1, y + 1))

        # return in the set format (((x1,y1), (x2, y2), (x3, y3)), 1) where 1 is the clue value
        return {value, tuple(z)}

    # updates the knowledge base for a given cell
    def updater(self, x, y):

        if self.board[x][y] == ' ' and (x, y) not in q and self.mine_dict[x][y]["open"] is False:
            # if the value of cell is empty we add it to the q stack
            q.append((x, y))
            self.mine_dict[x][y] = {"open": True, "mine": False}
            self.bot_board[x][y] = self.board[x][y]
            self.possible_coordinates.remove((x, y))
            return True  # return true only if there was new knowledge added

        elif (x, y) not in numbers and self.mine_dict[x][y]["open"] is False:
            # if the value of cell has a clue value > 0 we add it to the numbers queue
            numbers.append((x, y))
            self.mine_dict[x][y] = {"open": True, "mine": False}
            self.bot_board[x][y] = self.board[x][y]
            self.possible_coordinates.remove((x, y))
            return True  # return true only if there was new knowledge added

        return False

    # Solver 1 uses the pseudocode from the writeup and implements it this way:
    # Takes one equation we formed and looks at the number of variables (the number of cells in the equation) and the clue value.
    # if clue value is equal to the number of cells in the list we infer that they are all mines and if the clue value is 0 we infer that all the cells in the list are safe
    # and update the knowledge base accordingly.
    def solver_1(self, eq1):

        if len(eq1) != 2:
            return False

        neighbors = eq1.pop()
        num = eq1.pop()

        if isinstance(num, int) and isinstance(neighbors, tuple):
            if len(neighbors) == num:  # all cells are 1 meaning all cells are mines
                for i in range(0, len(neighbors)):
                    temp = neighbors[i]
                    # set (x,y) cell to 'm' to represent it is a mine
                    self.bot_board[temp[0]][temp[1]] = 'm'
                    if temp in self.possible_coordinates:
                        self.possible_coordinates.remove(temp)
                        self.mine_dict[temp[0]][temp[1]] = {
                            "open": True, "mine": True}
                        self.visited += 1
                return True  # return true if the equations is solved

            if num == 0:  # all cells are 0 meaning all cells are safe
                for i in range(0, len(neighbors)):
                    temp = neighbors[i]
                    self.bot_board[temp[0]][temp[1]] = self.board[temp[0]][
                        temp[1]]  # set (x,y) cell to 0 to represent it is safe
                    if temp in self.possible_coordinates:
                        self.possible_coordinates.remove(temp)
                        self.mine_dict[temp[0]][temp[1]] = {
                            "open": True, "mine": False}
                        self.visited += 1
                return True  # return true if the equations is solved

        # for edge cases where the set has switched values
        elif isinstance(neighbors, int) and isinstance(num, tuple):
            if len(num) == neighbors:
                for i in range(0, len(num)):
                    temp = num[i]
                    self.bot_board[temp[0]][temp[1]] = 'm'
                    if temp in self.possible_coordinates:
                        self.possible_coordinates.remove(temp)
                        self.mine_dict[temp[0]][temp[1]] = {
                            "open": True, "mine": True}
                        self.visited += 1
                return True

            if neighbors == 0:
                for i in range(0, len(num)):
                    temp = num[i]
                    self.bot_board[temp[0]][temp[1]
                                            ] = self.board[temp[0]][temp[1]]
                    if temp in self.possible_coordinates:
                        self.possible_coordinates.remove(temp)
                        self.mine_dict[temp[0]][temp[1]] = {
                            "open": True, "mine": False}
                        self.visited += 1
                return True

        return False  # false if the equation is not solved

    # the main algorithm for the basic agent as described in the writeup
    def basic_agent(self, x, y):
        c = 0 # keeps track of the number of mines that has been triggered
        while self.visited != self.dim * self.dim:  # keep going until all the cells are visited
            value = self.board[x][y]  # value on the current cell
            if value == 'm':  # if it's a mine we update the knowledge base accordingly
                self.bot_board[x][y] = 'm'
                self.mine_dict[x][y] = {"open": True, "nghbr": self.neighbor_count(x, y), "mine": True}
                self.visited += 1
                self.possible_coordinates.remove((x, y))  # remove the cell from the possible coordinates
                c += 1

            elif value.isnumeric():  # if the cell has value that's a clue > 0 we update the knowledge base
                if not self.mine_dict[x][y]["open"]: # if its not already open it should be added to the knowledge base and update the bot board accordingly
                    self.mine_dict[x][y] = {"open": True, "nghbr": self.neighbor_count(x, y), "mine": False}
                    self.bot_board[x][y] = value
                    self.possible_coordinates.remove((x, y))
                    self.solver_1(self.build_eq((x, y)))  # see if we can solve using the new knowledge
                    self.visited += 1

            elif value == ' ':  # if the cell is empty, meaning the clue value is 0, we open the cell around it given they haven't been opened before
                if self.mine_dict[x][y]["open"] is False and (x, y) not in q:  # if the cell hasn't been opened before we update the knowledge base
                    self.bot_board[x][y] = value
                    self.mine_dict[x][y] = {"open": True, "nghbr": self.neighbor_count(x, y), "mine": False}
                    self.possible_coordinates.remove((x, y))
                    self.visited += 1

                    # because we found a ' ' cell that indicates all of its neighbors are safe cells and can be visited
                    if self.check_constraints(x + 1, y):
                        if self.updater(x + 1, y):
                            self.visited += 1

                    if self.check_constraints(x - 1, y):
                        if self.updater(x - 1, y):
                            self.visited += 1

                    if self.check_constraints(x, y + 1):
                        if self.updater(x, y + 1):
                            self.visited += 1

                    if self.check_constraints(x, y - 1):
                        if self.updater(x, y - 1):
                            self.visited += 1

                    if self.check_constraints(x + 1, y + 1):
                        if self.updater(x + 1, y + 1):
                            self.visited += 1

                    if self.check_constraints(x + 1, y - 1):
                        if self.updater(x + 1, y - 1):
                            self.visited += 1

                    if self.check_constraints(x - 1, y - 1):
                        if self.updater(x - 1, y - 1):
                            self.visited += 1

                    if self.check_constraints(x - 1, y + 1):
                        if self.updater(x - 1, y + 1):
                            self.visited += 1

                while len(q) != 0:  # go through the q stack, and open the neighbors, if they have neighbors that have a clue value of 0 we open them too
                    item = q.pop()  # similar to actual game we open all the guaranteed safe cells given the origin cell has a clue value of 0
                    # we continue opening cells until we form a border with clue values of numbers > 0
                    xcord = item[0]
                    ycord = item[1]
                    
                    # iterate through all the neighbors and increment the visited accordingly
                    if self.check_constraints(xcord + 1, ycord):
                        if self.updater(xcord + 1, ycord):
                            self.visited += 1

                    if self.check_constraints(xcord - 1, ycord):
                        if self.updater(xcord - 1, ycord):
                            self.visited += 1

                    if self.check_constraints(xcord, ycord + 1):
                        if self.updater(xcord, ycord + 1):
                            self.visited += 1

                    if self.check_constraints(xcord, ycord - 1):
                        if self.updater(xcord, ycord - 1):
                            self.visited += 1

                    if self.check_constraints(xcord + 1, ycord + 1):
                        if self.updater(xcord + 1, ycord + 1):
                            self.visited += 1

                    if self.check_constraints(xcord + 1, ycord - 1):
                        if self.updater(xcord + 1, ycord - 1):
                            self.visited += 1

                    if self.check_constraints(xcord - 1, ycord - 1):
                        if self.updater(xcord - 1, ycord - 1):
                            self.visited += 1

                    if self.check_constraints(xcord - 1, ycord + 1):
                        if self.updater(xcord - 1, ycord + 1):
                            self.visited += 1

                while len(numbers) != 0:  # go through the queue that has cells with clue value > 0
                    tempnum = numbers.pop()
                    self.solver_1(self.build_eq(tempnum))  # see if there is a solution that can be found with this knowledge

            if self.possible_coordinates:  # while the array has more coordinates we can chose a random one from it
                random_point = random.choice(self.possible_coordinates)  # open a random cell
                x = random_point[0]
                y = random_point[1]
        
        print("Basic Agent Results: {} triggered mines, {} discovered mines {} safe cells".format(c, (self.mines-c), ((self.dim*self.dim)-self.mines)))

    # this is where the basic agent will start from
    def start(self):
        print("Game Board:")
        print(self.board)
        self.dictionary_init()  # initialize the dictionary
        self.coordinate_init()  # initialize all the possible coordinates
        random_point = random.choice(self.possible_coordinates) # select a random point to start from
        x = random_point[0]
        y = random_point[1]
        # start the basic agent
        self.basic_agent(x, y)
        print("Solved Agent Board:")
        print(self.bot_board)

# to start the basic agent
def start_basic_agent(dim, density):
    board = Basic_Agent(dim, density)
    board.start()
