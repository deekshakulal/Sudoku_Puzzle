import pygame
import time

class Sudoku:

    
    def isValid(self,grid):
        self.validrow = False
        self.validcolumn = False
        self.column = list()

        for i in range ( 0 , 9 ):

            for j in range ( 0 , 9 ):
                self.column.append( grid[ j ] [ i ])

            self.validcolumn = self.validRow(self.column)
            self.validrow = self.validRow(grid[i])

            if( self.validcolumn == False or self.validrow == False ):
                return False

            self.column.clear()

        return self.validrow and self.validcolumn


    def validRow(self,column):

        for i in range(0,len(column)-1):

            for j in range(i+1,len(column)):

                if(column[i] == column[j] and column[j] != 0):
                    return False

        return True


    def validBlock(self,grid):

        col=list()

        for block in range(0,9):
            col.clear()

            for i in range(((block//3) *3),(((block) //3) *3) +3):

                for j in range((block%3) *3,((((block) %3) *3) +3)):

                    if ( grid[i][j] != 0 ):
                        col.append(grid[i][j])

            if(not self.validRow(col)):
                return False

        return True


    def findEmptyspaces(self,grid,block):

        emptyspaces = list()
        emptyspaces.clear()
        for i in range(((block//3) *3),(((block)//3) *3) +3):

            for j in range((block%3) *3,((((block)%3) *3) +3)):

                if( grid [i][j] == 0 ):
                    emptyspaces.append((i,j))

        return emptyspaces


    def InsertInemptySpace(self,grid,emptyspace):
        self.i = 0
        self.j = 0
        self.m = 0
        self.n = 0
        
        canInsert = False
        for empty in emptyspace:
            self.i = empty[0]
            self.j = empty[1]
            
            for value in range(1,10):
                canInsert = False
                grid[self.i][self.j] = value

                if(self.isValid(grid) and self.validBlock(grid)):
                    for emp in emptyspace:
                        if(len(emptyspace) == 1):
                            canInsert = False
                            break

                        self.m = emp[0]
                        self.n = emp[1]

                        if( emp != empty and grid[self.m][self.n] == 0 ):

                            grid[self.i][self.j] = 0
                            grid[self.m][self.n] = value

                            if(self.isValid(grid) and self.validBlock(grid)):
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

                            
    def Findempty(self,grid):

        self.grid = grid

        for i in range(0,9):
            for j in range(0,9):
                if( grid[i][j] == 0):
                    return(i,j)

        return False
    
    def valid(self,grid,val,pos):

        for i in range(0,9):
            if(self.grid[pos[0]][i] == val and pos[1] != i):
                return False
        for i in range(0,9):
            if(self.grid[i][pos[1]] == val and pos[0] != i):
                return False
        
        box_x = pos[1]//3
        box_y = pos[0]//3

        for i in range(box_y*3,box_y*3+3):
            for j in range(box_x*3,box_x*3+3):
                if(self.grid[i][j] == val and (i,j) != pos):
                    return False
        return True



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



    def SudokuSolve(self,grid): 

        emptyspace=list()
        n=0
        while(n<9):

            for block in range(0,9):
                emptyspace.clear()
                emptyspace=self.findEmptyspaces(grid,block)
                grid=self.InsertInemptySpace(grid,emptyspace)
            n=n+1

        self.EnteratLast(grid)


if __name__ == "__main__":

    grid=[[0 for x in range(9)]for y in range(9)]

    grid1=    [[5,3,0,0,7,0,0,0,0],
              [6,0,0,1,9,5,0,0,0],
              [0,9,8,0,0,0,0,6,0],
              [8,0,0,0,6,0,0,0,3],
              [4,0,0,8,0,3,0,0,1],
              [7,0,0,0,2,0,0,0,6],
              [0,6,0,0,0,0,2,8,0],
              [0,0,0,4,1,9,0,0,5],
              [0,0,0,0,8,0,0,7,9]]

    grid=  [[2,5,0,0,0,3,0,9,1],
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

    #sudoku.SudokuSolve(grid)

    sudoku.EnteratLast(grid)
    end = time.time()
    print("Solution")
    print("    ")
    sudoku.print_grid(grid)

    print(end-start)
