import numpy, random, sys
from collections import defaultdict, deque

'''
Advanced Agent Class
Description: A class that holds all the information needed by the advanced agent and its logic.
'''

q = []  # stack of all the neighbors of a cell that has clue value of 0
numbers = deque()  # queue of all the neighbors of a cell that has clue value of 0, these neighbors have a clue value of > 0

class Advanced_Agent:
    
    dim = 10  # define a blank dimension size for the start
    # define a blank board for the start (with the placements)
    board = numpy.zeros((dim, dim), dtype=object)
    # this is the board that the agent is going to use to solve
    bot_board = numpy.zeros((dim, dim), dtype=object)
    mines = 0  # default value for the number of mines to be placed
    # {"open": T/F, "nghbr": num, "mine": T/F}
    # can use the mine_dict by mine_dict[x][y][key] where x and y are coordinates and key the value you want in return
    # initialize the beginning of the board for when we have to build it
    mine_dict = defaultdict(dict)
    possible_coordinates = [] # lists all the possible coordinates for the board 
    visited = 0 # keeps track of the cells visited in the advance agent 

    # initiizes the board upon starting the program
    def __init__(self, dim, mines):
        self.dim = dim # set the dim size for the board
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
        # to track the mines for the board
        mines = self.mines

        # dim array is utilized to pick a random index value for the game board
        dim_array = list(range(0, self.dim))
        
        # iterate through the board and choose randomly distinct points to add the mines for a more randomized board
        while mines != 0:
            i = random.choice(dim_array) # randomly choose a i value (rows)
            j = random.choice(dim_array) # randomly choose a j value (columns)
            arr = [0, 1]  # these will represent random choices
            if random.choice(arr) == 0 and mines != 0 and self.board[i][j] == 0:
                # if the condition is met the program should put a mine at the (i, j) spot and decrement the number of mines needed to be placed
                self.board[i][j] = 'm'
                mines -= 1

        # now for the rest of the board add empty spots and clues based on the positions of the mines on the board
        # the clue value in a certain cell ranges based on the neighbors that have a mine so that can be from 1-8 based on the density
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                count = 0 # to keep track of the clue value that should be placed
                self.bot_board[i][j] = ' '
                if self.board[i][j] == 0: # initially the board is set to all 0s
                    # check the up direction for a mine
                    if self.check_constraints(i - 1, j) and self.board[i - 1][j] == 'm':
                        count += 1
                    # check the down direction for a mine
                    if self.check_constraints(i + 1, j) and self.board[i + 1][j] == 'm':
                        count += 1
                    # check the left direction for a mine
                    if self.check_constraints(i, j - 1) and self.board[i][j - 1] == 'm':
                        count += 1
                    # check the right direction for a mine
                    if self.check_constraints(i, j + 1) and self.board[i][j + 1] == 'm':
                        count += 1
                    # check the upper left region for a mine
                    if self.check_constraints(i - 1, j - 1) and self.board[i - 1][j - 1] == 'm':
                        count += 1
                    # check the upper right region for a mine
                    if self.check_constraints(i - 1, j + 1) and self.board[i - 1][j + 1] == 'm':
                        count += 1
                    # check the bottom left region for a mine
                    if self.check_constraints(i + 1, j - 1) and self.board[i + 1][j - 1] == 'm':
                        count += 1
                    # check the bottom right region for a mine
                    if self.check_constraints(i + 1, j + 1) and self.board[i + 1][j + 1] == 'm':
                        count += 1

                    # if the count is 0 don't write a hint otherwise write the hint
                    if count == 0:
                        self.board[i][j] = ' '
                    else:
                        self.board[i][j] = str(count)

    # initializes all the possible coordinates for a given dimension (d)
    def coordinate_init(self): 
        possible_x = list(range(0, self.dim)) # obtain all the x values
        possible_y = list(range(0, self.dim)) # obtain all the y values
        # iterate through each x value and add the corresponding y value
        for i in range(0, len(possible_x)):
            for j in range(0, len(possible_y)):
                self.possible_coordinates.append((possible_x[i], possible_y[j]))

    # Initialize the dictionary to keep track of what's opened and at which cells there is a mine
    def dictionary_init(self):  
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                self.mine_dict[i][j] = {"open": False, "mine": False} # sample of how the dictionary is represented

    # check the bot_board to check if there is a neighbor that is already marked as a mine by the agent
    def mine_updater(self, i, j):
        count = 0 # keeps track of the number of mines at a given index value
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
        x = one[0] # x corresponds to the first element in the one array
        y = one[1] # y corresponds to the second element in the array
        z = [] # to assist in building the equation at the end
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

    # finds the difference between 2 given equations
    def set_difference(self, eq1, eq2): 

        if len(eq1) == 2 and len(eq2) == 2:

            eq1_neighbors = eq1.pop()  # list of all the neighbors of cell 1
            eq2_neighbors = eq2.pop()  # list of all the neighbors of cell 2
            num1 = eq1.pop()
            num2 = eq2.pop()
            if isinstance(num1, int) and isinstance(num2, int):
                set1 = {eq1_neighbors}  # covert the list into set
                set2 = {eq2_neighbors}
                diff = set1.difference(set2)  # difference between 2 sets
                num_diff = num1 - num2  # difference between the clue additions
                if any(diff):
                    # return a new equation that is the difference of the 2 input equations
                    return {diff.pop(), abs(num_diff)}

            elif isinstance(num1, int) and isinstance(eq1_neighbors, int):
                set1 = {num2}  # covert the list into set
                set2 = {eq2_neighbors}
                diff = set1.difference(set2)  # difference between 2 sets
                num_diff = num1 - eq1_neighbors  # difference between the clue additions
                if any(diff):
                    # return a new equation that is the difference of the 2 input equations
                    return {diff.pop(), abs(num_diff)}
            elif isinstance(num1, int) and isinstance(eq2_neighbors, int):
                set1 = {eq1_neighbors}  # covert the list into set
                set2 = {num2}
                diff = set1.difference(set2)  # difference between 2 sets
                num_diff = num1 - eq2_neighbors  # difference between the clue additions
                if any(diff):
                    # return a new equation that is the difference of the 2 input equations
                    return {diff.pop(), abs(num_diff)}
            elif isinstance(num2, int) and isinstance(eq2_neighbors, int):
                set1 = {eq1_neighbors}  # covert the list into set
                set2 = {num1}
                diff = set1.difference(set2)  # difference between 2 sets
                num_diff = num2 - eq2_neighbors  # difference between the clue additions
                if any(diff):
                    # return a new equation that is the difference of the 2 input equations
                    return {diff.pop(), abs(num_diff)}
            elif isinstance(num2, int) and isinstance(eq1_neighbors, int):
                set1 = {eq1_neighbors}  # covert the list into set
                set2 = {num2}
                diff = set1.difference(set2)  # difference between 2 sets
                num_diff = num2 - eq1_neighbors  # difference between the clue additions
                if any(diff):
                    # return a new equation that is the difference of the 2 input equations
                    return {diff.pop(), abs(num_diff)}

            else:  # for edge cases where the set has switched values
                set1 = {num1}
                set2 = {num2}
                diff = set1.difference(set2)
                num_diff = eq1_neighbors - eq2_neighbors
                if any(diff):
                    # return a new equation that is the difference of the 2 input equations
                    return {diff.pop(), abs(num_diff)}

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

    # takes 2 formed equation and tries to create a solution from them
    def solver_2(self, eq1, eq2):

        # creates a variable to hold the value of the equations
        c1 = eq1.copy()  # create a copy to be used together
        c2 = eq2.copy()
        tracker = False # to see if a solution is feasible

        diff_1_2 = self.set_difference(eq1, eq2)
        if diff_1_2 is not None and self.solver_1(diff_1_2):
            tracker = True

        if self.solver_1(c1):
            tracker = True

        if self.solver_1(c2):
            tracker = True

        return tracker

    # takes 3 cell locations and tries to find a solution from them 
    # then finds the difference from the solution it found
    def solver_3(self, p1, p2, p3):

        # create the 3 equations from the 3 points
        eq1 = self.build_eq(p1)
        eq2 = self.build_eq(p2)
        eq3 = self.build_eq(p3)

        # find solutions from the local knowledge of the cell
        self.solver_1(eq1)
        self.solver_1(eq2)
        self.solver_1(eq3)

        # difference of the given equations
        diff_1_2 = self.set_difference(self.build_eq(p1), self.build_eq(p2))
        diff_1_3 = self.set_difference(self.build_eq(p1), self.build_eq(p3))
        diff_2_3 = self.set_difference(self.build_eq(p2), self.build_eq(p3))

        if diff_1_2 is not None and diff_2_3 is not None:  # find a solution from the differences
            self.solver_2(diff_1_2, diff_2_3)
        if diff_1_2 is not None and diff_1_3 is not None:
            self.solver_2(diff_1_2, diff_1_3)
        if diff_1_3 is not None and diff_2_3 is not None:
            self.solver_2(diff_1_3, diff_2_3)

        return

    # This is the acronym we decided for the Advanced Agent: nsfm (Not Safe for Minesweeper) because
    # how powerful the advance agent is.
    def nsfm(self, x, y):
        c = 0 # keep track of the amount of mines the advance agent triggers
        while self.visited != self.dim * self.dim:  # keep going until all the cells are visited
            value = self.board[x][y]  # value on the current cell
            if value == 'm':  # if it's a mine we update the knowledge base accordingly
                self.bot_board[x][y] = 'm'
                self.mine_dict[x][y] = {"open": True, "mine": True}
                self.visited += 1
                # remove the cell from the possible coordinates
                self.possible_coordinates.remove((x, y))
                c += 1

            elif value.isnumeric():  # if the cell has value that's a clue > 0 we update the knowledge base
                if not self.mine_dict[x][y]["open"]: # if its not already open it should be added to the knowledge base and update the bot board accordingly
                    self.mine_dict[x][y] = {"open": True, "mine": False}
                    self.bot_board[x][y] = value
                    self.possible_coordinates.remove((x, y))
                    numbers.append((x, y))
                    self.visited += 1

            elif value == ' ':  # if the cell is empty, meaning the clue value is 0, we open the cell around it given they haven't been opened before
                # if the cell hasn't been opened before we update the knowledge base
                if self.mine_dict[x][y]["open"] is False and (x, y) not in q:
                    self.bot_board[x][y] = value
                    self.mine_dict[x][y] = {"open": True, "mine": False}
                    self.possible_coordinates.remove((x, y))
                    self.visited += 1

                    # check all the directions because if its ' ' that would entail the rest of its neighbors are not mines
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

                # go through the q stack, and open the neighbors, if they have neighbors that have a clue value of 0 we open them too
                while len(q) != 0:  
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

                tempnum = []
                # now we use the border of numeric clue values to find solutions
                if len(numbers) >= 3:  # go through the queue that has cells with clue value > 0
                    first = numbers.pop()  # pop the first one se it can be saved for the end
                    tempnum.append(first)
                    for x in range(0, len(numbers) - 1):
                        if x == 0:
                            for y in range(0, 2):
                                tempnum.append(numbers.popleft())
                        else:
                            tempnum.remove(tempnum[0])
                            tempnum.append(numbers.popleft())
                        self.solver_3(tempnum[0], tempnum[1],
                                      tempnum[2])  # send 3 point to the solver_3 function to find solution

                    tempnum.remove(tempnum[0])
                    tempnum.append(first)
                    # solve with the last 2 and the first cell
                    self.solver_3(tempnum[0], tempnum[1], tempnum[2])
                elif len(numbers) == 2:  # if the queue only has 2 value we use the solver_2
                    one = numbers.popleft()
                    tempnum.append(one)
                    two = numbers.popleft()
                    tempnum.append(two)
                    self.solver_2(self.build_eq(
                        tempnum[0]), self.build_eq(tempnum[1]))
                elif len(numbers) == 1:  # if the queue has only 1 value we use solver_1
                    three = numbers.popleft()
                    tempnum.append(three)
                    self.solver_1(self.build_eq(tempnum[0]))

            bln = True  # to see if there is a solution found or not in the iteration

            while bln:
                old_visited = self.visited
                for i in range(0, self.dim):
                    for j in range(0, self.dim):
                        val = self.bot_board[i][j]
                        if val.isnumeric() and self.mine_updater(i, j) != self.bot_board[i][j]:
                            numbers.append((i, j))

                            '''
                            A A A A A  
                            A a a a A 
                            A a C a A 
                            A a a a A 
                            A A A A A

                            C - origin cell
                            a - first neighbors
                            A - neighbors of neighbors, i.e. bigger box 
                            '''
                            # check for values in the bigger box - meaning neighbors of neighbors, as shown in the box it will compare equations from 3 cells at max
                            if self.check_constraints(i - 2, j - 2) and self.bot_board[i - 2][
                                    j - 2].isnumeric() and self.mine_updater(i - 2, j - 2) != self.bot_board[i - 2][j - 2]:
                                numbers.append((i - 2, j - 2))
                            if self.check_constraints(i - 2, j - 1) and self.bot_board[i - 2][
                                    j - 1].isnumeric() and self.mine_updater(i - 2, j - 1) != self.bot_board[i - 2][j - 1]:
                                numbers.append((i - 2, j - 1))
                            if self.check_constraints(i - 2, j) and self.bot_board[i - 2][
                                    j].isnumeric() and self.mine_updater(i - 2, j) != self.bot_board[i - 2][j]:
                                numbers.append((i - 2, j))
                            if self.check_constraints(i - 2, j + 1) and self.bot_board[i - 2][
                                    j + 1].isnumeric() and self.mine_updater(i - 2, j + 1) != self.bot_board[i - 2][j + 1]:
                                numbers.append((i - 2, j + 1))
                            if self.check_constraints(i - 2, j + 2) and self.bot_board[i - 2][
                                    j + 2].isnumeric() and self.mine_updater(i - 2, j + 2) != self.bot_board[i - 2][j + 2]:
                                numbers.append((i - 2, j + 2))
                            if self.check_constraints(i - 1, j + 2) and self.bot_board[i - 1][
                                    j + 2].isnumeric() and self.mine_updater(i - 1, j + 2) != self.bot_board[i - 1][j + 2]:
                                numbers.append((i - 1, j + 2))
                            if self.check_constraints(i, j + 2) and self.bot_board[i][
                                    j + 2].isnumeric() and self.mine_updater(i, j + 2) != self.bot_board[i][j + 2]:
                                numbers.append((i, j + 2))
                            if self.check_constraints(i + 1, j + 2) and self.bot_board[i + 1][
                                    j + 2].isnumeric() and self.mine_updater(i + 1, j + 2) != self.bot_board[i + 1][j + 2]:
                                numbers.append((i + 1, j + 2))
                            if self.check_constraints(i + 2, j + 2) and self.bot_board[i + 2][
                                    j + 2].isnumeric() and self.mine_updater(i + 2, j + 2) != self.bot_board[i + 2][j + 2]:
                                numbers.append((i + 2, j + 2))
                            if self.check_constraints(i + 2, j + 1) and self.bot_board[i + 2][
                                    j + 1].isnumeric() and self.mine_updater(i + 2, j + 1) != self.bot_board[i + 2][j + 1]:
                                numbers.append((i + 2, j + 1))
                            if self.check_constraints(i + 2, j) and self.bot_board[i + 2][
                                    j].isnumeric() and self.mine_updater(i + 2, j) != self.bot_board[i + 2][j]:
                                numbers.append((i + 2, j))
                            if self.check_constraints(i + 2, j - 1) and self.bot_board[i + 2][
                                    j - 1].isnumeric() and self.mine_updater(i + 2, j - 1) != self.bot_board[i + 2][j - 1]:
                                numbers.append((i + 2, j - 1))
                            if self.check_constraints(i + 2, j - 2) and self.bot_board[i + 2][
                                    j - 2].isnumeric() and self.mine_updater(i + 2, j - 2) != self.bot_board[i + 2][j - 2]:
                                numbers.append((i + 2, j - 2))
                            if self.check_constraints(i + 1, j - 2) and self.bot_board[i + 1][
                                    j - 2].isnumeric() and self.mine_updater(i + 1, j - 2) != self.bot_board[i + 1][j - 2]:
                                numbers.append((i + 1, j - 2))
                            if self.check_constraints(i, j - 2) and self.bot_board[i][
                                    j - 2].isnumeric() and self.mine_updater(i, j - 2) != self.bot_board[i][j - 2]:
                                numbers.append((i, j - 2))
                            if self.check_constraints(i - 1, j - 2) and self.bot_board[i - 1][
                                    j - 2].isnumeric() and self.mine_updater(i - 1, j - 2) != self.bot_board[i - 1][j - 2]:
                                numbers.append((i - 1, j - 2))

                            #  check for values in the direct neighbors
                            if self.check_constraints(i + 1, j) and self.bot_board[i + 1][
                                    j].isnumeric() and self.mine_updater(i + 1, j) != self.bot_board[i + 1][j]:
                                numbers.append((i + 1, j))
                            if self.check_constraints(i - 1, j) and self.bot_board[i - 1][
                                    j].isnumeric() and self.mine_updater(i - 1, j) != self.bot_board[i - 1][j]:
                                numbers.append((i - 1, j))
                            if self.check_constraints(i, j - 1) and self.bot_board[i][
                                    j - 1].isnumeric() and self.mine_updater(i, j - 1) != self.bot_board[i][j - 1]:
                                numbers.append((i, j - 1))
                            if self.check_constraints(i, j + 1) and self.bot_board[i][
                                    j + 1].isnumeric() and self.mine_updater(i, j + 1) != self.bot_board[i][j + 1]:
                                numbers.append((i, j + 1))
                            if self.check_constraints(i + 1, j + 1) and self.bot_board[i + 1][
                                    j + 1].isnumeric() and self.mine_updater(i + 1, j + 1) != self.bot_board[i + 1][j + 1]:
                                numbers.append((i + 1, j + 1))
                            if self.check_constraints(i + 1, j - 1) and self.bot_board[i + 1][
                                    j - 1].isnumeric() and self.mine_updater(i + 1, j - 1) != self.bot_board[i + 1][j - 1]:
                                numbers.append((i + 1, j - 1))
                            if self.check_constraints(i - 1, j - 1) and self.bot_board[i - 1][
                                    j - 1].isnumeric() and self.mine_updater(i - 1, j - 1) != self.bot_board[i - 1][j - 1]:
                                numbers.append((i - 1, j - 1))
                            if self.check_constraints(i - 1, j + 1) and self.bot_board[i - 1][
                                    j + 1].isnumeric() and self.mine_updater(i - 1, j + 1) != self.bot_board[i - 1][j + 1]:
                                numbers.append((i - 1, j + 1))

                    tempnum = []
                    if len(numbers) >= 3:  # go through the queue that has cells with clue value > 0
                        first = numbers.pop()
                        tempnum.append(first)
                        for x in range(0, len(numbers) - 1):
                            if x == 0:
                                for y in range(0, 2):
                                    tempnum.append(numbers.popleft())
                            else:
                                tempnum.remove(tempnum[0])
                                tempnum.append(numbers.popleft())
                            self.solver_3(tempnum[0], tempnum[1],
                                          tempnum[2])  # use solver_3 to find solution using 3 equations

                        # solve with the last 2 and the first cell
                        tempnum.remove(tempnum[0])
                        tempnum.append(first)
                        # solve with the last 2 and the first cell
                        self.solver_3(tempnum[0], tempnum[1], tempnum[2])
                    elif len(numbers) == 2:  # if the queue only has 2 value we use the solver_2
                        one = numbers.popleft()
                        tempnum.append(one)
                        two = numbers.popleft()
                        tempnum.append(two)
                        self.solver_2(self.build_eq(
                            tempnum[0]), self.build_eq(tempnum[1]))
                    elif len(numbers) == 1:  # if the queue has only 1 value we use solver_1
                        three = numbers.popleft()
                        tempnum.append(three)
                        self.solver_1(self.build_eq(tempnum[0]))

                if old_visited == self.visited:  # no more solution can be found from the known value so open a random cell
                    bln = False

            if self.possible_coordinates:  # open a random cell
                random_point = random.choice(self.possible_coordinates)
                x = random_point[0]
                y = random_point[1]

        print("Advanced Agent Results: {} triggered mines, {} discovered mines {} safe cells".format(c, (self.mines-c), ((self.dim*self.dim)-self.mines)))

    # this is where the advance agent will start from
    def start(self):
        print("Game Board:")
        print(self.board)
        self.dictionary_init() # initialize the dictionary 
        self.coordinate_init() # initialize all the possible coordinates
        random_point = random.choice(self.possible_coordinates) # select a random point to start from
        x = random_point[0]
        y = random_point[1]
        # start the advance agent
        self.nsfm(x, y)
        print("Solved Agent Board:")
        print(self.bot_board)

# to start the advance agent
def start_advance_agent(dim, density):
    board = Advanced_Agent(dim, density)
    board.start()
