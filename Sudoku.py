#import pygame
from random import shuffle
import time
import copy

class Sudoku:

	def __init__(self, grid):
		
		self.counter = 0
		#path is for the matplotlib animation
		self.path = []
		self.grid = grid
		self.generate_puzzle()
		self.original = copy.deepcopy(self.grid)
    
	def generate_puzzle(self):
		"""generates a new puzzle and solves it"""
		self.generate_solution(self.grid)
		self.remove_numbers_from_grid()
		self.print_grid(self.grid)
		return

	def solve_puzzle(self, grid):
		"""solve the sudoku puzzle with backtracking"""
		for i in range(0,81):
			row=i//9
			col=i%9
			#find next empty cell
			if grid[row][col]==0:
				for number in range(1,10):
					#check that the number hasn't been used in the row/col/subgrid
					if self.valid(grid,number,(row,col)):
						grid[row][col]=number
						if not self.find_empty_square(grid):
							self.counter+=1
							break
						else:
							if self.solve_puzzle(grid):
								return True
				break
		grid[row][col]=0  
		return False

	def find_empty_square(self,grid):
		"""return the next empty square coordinates in the grid"""
		for i in range(9):
			for j in range(9):
				if grid[i][j] == 0:
					return (i,j)
		return


	def generate_solution(self, grid):
		"""generates a full solution with backtracking"""
        
		number_list = [1,2,3,4,5,6,7,8,9]
		for i in range(0,81):
			row=i//9
			col=i%9
			#find next empty cell
			if grid[row][col]==0:
				shuffle(number_list)      
				for number in number_list:
					if self.valid(grid,number,(row,col)):
						self.path.append((number,row,col))
						grid[row][col]=number
						if not self.find_empty_square(grid):
							return True
						else:
							if self.generate_solution(grid):
								#if the grid is full
								return True
				break
		grid[row][col]=0  
		return False

	def get_non_empty_squares(self,grid):
		"""returns a shuffled list of non-empty squares in the puzzle"""
		non_empty_squares = []
		for i in range(len(grid)):
			for j in range(len(grid)):
				if grid[i][j] != 0:
					non_empty_squares.append((i,j))
		shuffle(non_empty_squares)
		return non_empty_squares

	def remove_numbers_from_grid(self):
		"""remove numbers from the grid to create the puzzle"""
		#get all non-empty squares from the grid
		non_empty_squares = self.get_non_empty_squares(self.grid)
		non_empty_squares_count = len(non_empty_squares)
		rounds = 3
		while rounds > 0 and non_empty_squares_count >= 17:
			#there should be at least 17 clues
			row,col = non_empty_squares.pop()
			non_empty_squares_count -= 1
			#might need to put the square value back if there is more than one solution
			removed_square = self.grid[row][col]
			self.grid[row][col]=0
			#make a copy of the grid to solve
			grid_copy = copy.deepcopy(self.grid)
			#initialize solutions counter to zero
			self.counter=0      
			self.solve_puzzle(grid_copy)   
			#if there is more than one solution, put the last removed cell back into the grid
			if self.counter!=1:
				self.grid[row][col]=removed_square
				non_empty_squares_count += 1
				rounds -=1
		return
	
	#Returns a List of tuples while contain the position of emptyspaces in a (3 * 3) block
	def findEmptyspaces(self, grid, block):

		emptyspaces = list()
		emptyspaces.clear()
		for i in range(((block//3) * 3), (((block)//3) * 3) + 3):

			for j in range((block % 3) * 3, ((((block) % 3) * 3) + 3)):

				if(grid[i][j] == 0):
					emptyspaces.append((i, j))

		return emptyspaces

	'''Inserts Values using Single possibility rule i.e Inserts a value only when the value cannot be assigned to another empty
		 space in the block '''

	def InsertInemptySpace(self, grid, emptyspace):

		self.i = 0
		self.j = 0
		self.m = 0
		self.n = 0

		canInsert = False

		for empty in emptyspace:
			self.i = empty[0]
			self.j = empty[1]

			#Allocates a value to an empty space
			for value in range(1, 10):
				canInsert = False

				if(self.valid(grid, value, (self.i, self.j))):

					grid[self.i][self.j] = value

					#Checks if the same value can be inserted to any other empty space within the block
					for emp in emptyspace:

						if(len(emptyspace) == 1):
							canInsert = False
							break

						self.m = emp[0]
						self.n = emp[1]

						if(emp != empty and grid[self.m][self.n] == 0):

							grid[self.i][self.j] = 0

							if(self.valid(grid, value, (self.m, self.n))):

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
	def Findempty(self, grid):

		self.grid = grid

		for i in range(0, 9):

			for j in range(0, 9):
				if(grid[i][j] == 0):
					return(i, j)

		return False

	#Checks if the value assigned at position pos is valid or not
	def valid(self, grid, val, pos):

		for i in range(0, 9):
			if(grid[pos[0]][i] == val and pos[1] != i):
				return False

		for i in range(0, 9):
			if(grid[i][pos[1]] == val and pos[0] != i):
				return False

		box_x = pos[1] // 3
		box_y = pos[0] // 3

		for i in range(box_y * 3, box_y * 3 + 3):
			for j in range(box_x * 3, box_x * 3 + 3):
				if(grid[i][j] == val and (i, j) != pos):
					return False
		return True

	#The Backtracking algorithm fills out the remaining spaces in the grid.
	def EnteratLast(self, grid):
		row = 0
		col = 0
		self.grid = grid
		empty = self.Findempty(self.grid)
		if not empty:
			return True
		else:
			row, col = empty

		for i in range(1, 10):
			if(self.valid(self.grid, i, (row, col))):
				self.grid[row][col] = i

				if(self.EnteratLast(self.grid)):
					return True

				self.grid[row][col] = 0

		return False

	#Prints the grid
	def print_grid(self, grid):

		for i in range(len(grid)):

			if(i % 3 == 0 and i != 0):
				print("- - - - - - - - - - - -")

			for j in range(len(grid[0])):

				if(j % 3 == 0 and j != 0):
					print(" | ", end="")

				if(j == 8):
					print(grid[i][j])

				else:
					print(str(grid[i][j]) + " ", end="")


	#The main solving function
	def SudokuSolve(self, grid):

		emptyspace = list()
		n = 0
		grid_prev = [[0 for x in range(9)] for y in range(9)]
		#Iterates until the previous grid is same as the next one
		#First solves the sudoku using Single Value only technique
		while(grid_prev != grid):
			grid_prev = grid
			for block in range(0, 9):
				emptyspace.clear()
				emptyspace = self.findEmptyspaces(grid, block)
				grid = self.InsertInemptySpace(grid, emptyspace)
			n = n+1

		#Calls Backtracking algorithm to fill out the remaining empty spaces
		self.EnteratLast(grid)


if __name__ == "__main__":

	grid = [[0 for x in range(9)] for y in range(9)]
	print("Solve this")
	sudoku = Sudoku(grid)
	start = time.time()

	sudoku.SudokuSolve(grid)

	end = time.time()
	print("Solution")
	print("    ")
	sudoku.print_grid(grid)
	print("time taken")
	print(end-start)
