import pygame


class Sudoku:

    def isValid(self,grid):
        self.validrow=False
        self.validcolumn=False
        self.column=list()
        for i in range(0,9):
            for j in range(0,9):
                self.column.append(grid[j][i])
            self.validcolumn=self.validRow(self.column)
            self.validrow=self.validRow(grid[i])
            if(self.validcolumn==False or self.validrow==False ):
                return False
            self.column.clear()
        return self.validrow and self.validcolumn

    def validRow(self,column):
        for i in range(0,len(column)-1):
            for j in range(i+1,len(column)):
                if(column[i] == column[j] and column[j]!=0):
                    return False
        return True

    def validBlock(self,grid):
        col=list()
        for block in range(0,9):
            col.clear()
            for i in range(((block//3)*3),(((block)//3)*3)+3):
                for j in range((block%3)*3,((((block)%3)*3)+3)):
                    if(grid[i][j]!=0):
                        col.append(grid[i][j])
            if(not self.validRow(col)):
                return False
        return True



    def findEmptyspaces(self,grid,block):
        emptyspaces=list()
        emptyspaces.clear()
        for i in range(((block//3)*3),(((block)//3)*3)+3):
            for j in range((block%3)*3,((((block)%3)*3)+3)):
                if(grid[i][j]==0):
                    emptyspaces.append((i,j))
        
        return emptyspaces

    def InsertInemptySpace(self,grid,emptyspace):
        self.i=0
        self.j=0
        self.m=0
        self.n=0
        
        canInsert=False
        for empty in emptyspace:
            self.i=empty[0]
            self.j=empty[1]
            
            for value in range(1,10):
                canInsert=False
                grid[self.i][self.j]=value
                if(self.isValid(grid) and self.validBlock(grid)):
                    for emp in emptyspace:
                        if(len(emptyspace)==1):
                            canInsert=False
                            break
                        self.m=emp[0]
                        self.n=emp[1]
                        if(emp!=empty and grid[self.m][self.n]==0 ):
                            grid[self.i][self.j]=0
                            grid[self.m][self.n]=value
                            if(self.isValid(grid) and self.validBlock(grid)):
                                grid[self.m][self.n]=0
                                canInsert=True
                                break
                            else:
                                grid[self.i][self.j]=value
                                grid[self.m][self.n]=0
                                canInsert=False
                    if(not canInsert):
                        grid[self.i][self.j]=value
                        break
                else:
                    grid[self.i][self.j]=0
        return grid

                            
    def FindAllEmptyspace(self,grid):
        emptyy=list()
        for i in range(0,9):
            for j in range(0,9):
                if(grid[i][j]==0):
                    emptyy.append((i,j))
        return emptyy

    def EnteratLast(self,grid,empty):
        i=0
        j=0
        #empty=self.FindAllEmptyspace(grid)
        for emp in empty:
            for value in range(1,10):
                i=emp[0]
                j=emp[1]
                grid[i][j]=value
                if(self.isValid(grid) and self.validBlock(grid)):
                    break
                else:
                    grid[i][j]=0
        return grid

    def SudokuSolve(self,grid):
        emptyspace=list()
        n=0
        while(n<10):
                
            for block in range(0,9):
                emptyspace.clear()
                emptyspace=self.findEmptyspaces(grid,block)
                grid=self.InsertInemptySpace(grid,emptyspace)
            n=n+1
        emptyspace=self.FindAllEmptyspace(grid)
        grid=self.EnteratLast(grid,emptyspace)
        
        return grid


if __name__ == "__main__":
    grid=[[0 for x in range(9)]for y in range(9)]
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
    
    print(grid)

    grid=sudoku.SudokuSolve(grid)

    print("Solution")
    print(grid)

