import pygame
import time

class Sudoku:

    #Returns a List of tuples while contain the position of emptyspaces in a (3 * 3) block
    def findEmptyspaces(self,grid,block):

        emptyspaces = list()
        emptyspaces.clear()
        for i in range(((block//3) *3),(((block)//3) *3) +3):

            for j in range((block%3) *3,((((block)%3) *3) +3)):

                if( grid [i][j] == 0 ):
                    emptyspaces.append((i,j))

        return emptyspaces


    '''Inserts Values using Single possibility rule i.e Inserts a value only when the value cannot be assigned to another empty
         space in the block '''
    def InsertInemptySpace(self,grid,emptyspace):

        self.i = 0
        self.j = 0
        self.m = 0
        self.n = 0
        
        canInsert = False

        for empty in emptyspace:
            self.i = empty[0]
            self.j = empty[1]
            
            #Allocates a value to an empty space
            for value in range(1,10):
                canInsert = False
                
                if(self.valid(grid,value,(self.i,self.j))):

                    grid[self.i][self.j] = value

                    #Checks if the same value can be inserted to any other empty space within the block
                    for emp in emptyspace:

                        if(len(emptyspace) == 1):
                            canInsert = False
                            break

                        self.m = emp[0]
                        self.n = emp[1]

                        if( emp != empty and grid[self.m][self.n] == 0 ):

                            grid[self.i][self.j] = 0

                            if(self.valid(grid,value,(self.m,self.n))):

                                grid[self.i][self.j] = 0
                                grid[self.m][self.n] = 0
                                canInsert = True
                                break

                            else:

                                grid[self.i][self.j] = value
                                grid[self.m][self.n] = 0
                                canInsert = False

                    if(not canInsert):

                        grid[self.i][self.j] = value
                        break
                        
                else:

                    grid[self.i][self.j] = 0

        return grid

    #returns a tuple i,j containing the position of empty space
    def Findempty(self,grid):

        self.grid = grid

        for i in range(0,9):
            for j in range(0,9):
                if( grid[i][j] == 0):
                    return(i,j)

        return False
    
    #Checks if the value assigned at position pos is valid or not
    def valid(self,grid,val,pos):

        for i in range(0,9):
            if(grid[pos[0]][i] == val and pos[1] != i):
                return False
        for i in range(0,9):
            if(grid[i][pos[1]] == val and pos[0] != i):
                return False
        
        box_x = pos[1]//3
        box_y = pos[0]//3

        for i in range(box_y*3,box_y*3+3):
            for j in range(box_x*3,box_x*3+3):
                if(grid[i][j] == val and (i,j) != pos):
                    return False
        return True


    #The Backtracking algorithm fills out the remaining spaces in the grid.
    def EnteratLast(self,grid):
        row=0
        col=0
        self.grid=grid
        empty=self.Findempty(self.grid)
        if not empty:
            return True
        else:
            row,col = empty
        
        for i in range(1,10):
            if(self.valid(self.grid, i, (row,col))):
                self.grid[row][col] = i

                if(self.EnteratLast(self.grid)):
                    return True
                
                self.grid[row][col] = 0

        return False


    #Prints the grid
    def print_grid(self,grid):

        for i in range(len(grid)):

            if(i%3==0 and i!=0):
                print("- - - - - - - - - - - -")

            for j in range(len(grid[0])):

                if( j%3 == 0 and j != 0):
                    print(" | ",end="")

                if(j == 8):
                    print(grid[i][j])

                else:
                    print(str(grid[i][j]) + " ",end="")



    #The main solving function
    def SudokuSolve(self,grid): 

        emptyspace = list()
        n = 0
        grid_prev = [ [0 for x in range(9) ] for y in range(9) ]
        #Iterates until the previous grid is same as the next one
        #First solves the sudoku using Single Value only technique
        while( grid_prev != grid ):
            grid_prev=grid
            for block in range(0,9):
                emptyspace.clear()
                emptyspace = self.findEmptyspaces(grid,block)
                grid = self.InsertInemptySpace(grid,emptyspace)
            n = n+1

        #Calls Backtracking algorithm to fill out the remaining empty spaces
        self.EnteratLast(grid)


if __name__ == "__main__":

    grid=[ [ 0 for x in range(9) ] for y in range(9) ]

    grid=    [[5,3,0,0,7,0,0,0,0],
              [6,0,0,1,9,5,0,0,0],
              [0,9,8,0,0,0,0,6,0],
              [8,0,0,0,6,0,0,0,3],
              [4,0,0,8,0,3,0,0,1],
              [7,0,0,0,2,0,0,0,6],
              [0,6,0,0,0,0,2,8,0],
              [0,0,0,4,1,9,0,0,5],
              [0,0,0,0,8,0,0,7,9]]

    grid1=  [[2,5,0,0,0,3,0,9,1],
            [3,0,9,0,0,0,7,2,0],
            [0,0,1,0,0,6,3,0,0],
            [0,0,0,0,6,8,0,0,3],
            [0,1,0,0,4,0,0,0,0],
            [6,0,3,0,0,0,0,5,0],
            [1,3,2,0,0,0,0,7,0],
            [0,0,0,0,0,4,0,6,0],
            [7,6,4,0,1,0,0,0,0]]

    sudoku=Sudoku()
    
    sudoku.print_grid(grid)

    start=time.time()

    sudoku.EnteratLast(grid)

    end = time.time()
    print("Solution")
    print("    ")
    sudoku.print_grid(grid)
    print("time taken")
    print(end-start)
