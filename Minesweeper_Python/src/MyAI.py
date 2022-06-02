# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import time
import random

totalTime = 10.0 		# seconds allowed for one game
totalTimeElapsed = 0.0

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		# print("START: ", startX, startY)
		self.__rowDimension = rowDimension
		self.__colDimension = colDimension
		self.totalMines = totalMines
		self.minesLeft = totalMines
		self.coveredTilesLeft = rowDimension * colDimension
		self.board = list() 	# list of list of lists
		self.__lastX = startX	# x = column coordinate
		self.__lastY = startY	# y = row coordinate
		self.__frontier = {}	# dictionary (x, y):[a,b,c]
		self.__safe = {}		# dictionary (x, y):[a,b,c]
		self.__uncovered = {}
		self.guess = {}

		# */M/n : Effective Label : # adjacent covered/unmarked tiles
		# * = Covered/Unmarked / M = Mine(Covered/Marked) / n = label(Uncovered)
		# Effective Label = Label - NumMarkedNeighbors
		# initialize board to *:None:#
		for y in range(rowDimension):
			row = []
			for x in range(colDimension):
				if (y == 0 or y == rowDimension - 1) and (
					x == 0 or x == colDimension -1):
					row.append(['*', None, 3]) 	# numCovered = 3
				elif y == 0 or y == rowDimension - 1 or x == 0 or \
					x == colDimension -1:
					row.append(['*', None, 5]) 	# numCovered = 5
				else: 
					row.append(['*', None, 8]) 	# numCovered = 8
			self.board.append(row)

		self.coveredTilesLeft -= 1				# decrement tile count

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		# exit condition
		if self.coveredTilesLeft <= self.totalMines:
			return Action(AI.Action.LEAVE)

		# update board (using previous getAction result)
		self._updateBoard(self.__lastX, self.__lastY, number)
		# print("Covered Tiles left: ", self.coveredTilesLeft)
		
		# rule of thumb
		if self.getEffectiveLabel(self.__lastX, self.__lastY) == \
			self.getNumUnmarkedNeighbors(self.__lastX, self.__lastY):
			self.FlagAdjacent(self.__lastX, self.__lastY)
			# flag all adjacent covered tiles as mines
		
		
		#if rules of thumb don't yield results, model check
		if self.__frontier and self.__uncovered and not self.__safe: 
			check = self.modelCheck()
			#check[0] is list of safe tiles
			for tile in check[0]:
				if tile not in self.__safe:
					self.__safe[tile] = self.board[tile[1]][tile[0]]
			#check[1] is list of mine tiles, flag each mine tile and update flagNeighbors
			for tile in check[1]:
				flag_x, flag_y = tile[0], tile[1]
				self.board[flag_y][flag_x][0] = 'M'
				self.board[flag_y][flag_x][1] = None
				self.minesLeft -= 1
				self._updateFlagNeighbors(flag_x, flag_y)
				if tile in self.__frontier:
					self.__frontier.pop(tile)
			if len(check[2]) != 0:
				for tile in check[2]:
					self.guess[tile] = self.board[tile[1]][tile[0]]
		''''''
		global totalTimeElapsed 
		remainingTime = totalTime - totalTimeElapsed
		if remainingTime < 3:
			# random move
			action = AI.Action(1)
			x = random.randrange(self.__colDimension)
			y = random.randrange(self.__rowDimension)
			self.coveredTilesLeft -= 1
			self.__lastX = x
			self.__lastY = y
			return Action(action, x, y)
		else :
			timeStart = time.time()

			# next uncover
			action = AI.Action(1)
			if self.__safe:
				x, y = self.__safe.popitem()[0]
			elif self.__frontier:
				x, y = self.__frontier.popitem()[0]
				while (self.__frontier):
					if self.getLabel(x, y) == '*':
						break
					else:
						x, y = self.__frontier.popitem()[0]
			else:
				if self.guess:
					x, y = self.guess.popitem()[0]
				else:
					x = random.randrange(self.__colDimension)
					y = random.randrange(self.__rowDimension)

				# print("x, y: ", x, y)
			self.guess.clear() 
			self.coveredTilesLeft -= 1

			self.__lastX = x
			self.__lastY = y

			timeEnd = time.time()
			timeDifference = timeStart - timeEnd
			totalTimeElapsed += timeDifference	# update time used for call

			return Action(action, x, y)


		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def getLabel(self, x, y):
		""" 
		get label helper function
			input - 
				x (int): column index
				y (int): row index			
			return -  
				label (string/int): 
					* = Covered/Unmarked
					M = Mine(Covered/Marked)
					n = label(Uncovered)
		"""
		return self.board[y][x][0]

	def getEffectiveLabel(self, x, y):
		""" 
		get effective label helper function
		Effective Label = Label - NumMarkedNeighbors
			input - 
				x (int): column index
				y (int): row index
			return - 
				EffectiveLabel (int): Label - NumMarkedNeighbors
		"""
		return self.board[y][x][1]

	def getNumUnmarkedNeighbors(self, x: int, y: int) -> int:
		""" 
		get number of Unmarked Neighbor helper function
			input - 
				x (int): column index
				y (int): row index		
				NumUnmarkedNeighbors (int): number of unmarked neighbors
		"""
		return self.board[y][x][2]

	def _checkRule(self, x: int, y: int) -> None:
		"""
		checks if effectivelabel(x) = numUnMarkedNeighbors on last x, y
			input - 
				x (int): column index
				y (int): row index
		"""
		if self.getEffectiveLabel(x, y) == self.getNumUnmarkedNeighbors(x, y):
			self.FlagAdjacent(x, y)
			#flag all adjacent covered tiles as mines

	def FlagAdjacent(self, col: int, row: int) -> None:
		"""
		flag adjacent tiles as mines, label with 'M'
			input - 
				col (int): column index
				row (int): row index
		"""
		for x in [col-1, col, col+1]:
			for y in [row-1, row, row+1]:
				if (x >= 0 and y>= 0) and (x < self.__colDimension and
					y < self.__rowDimension) and (x != col or y != row) and\
					(self.getLabel(x, y) == '*'):
					self.board[y][x][0] = 'M'
					self.board[y][x][1] = None
					self._updateFlagNeighbors(x, y)
					self.minesLeft -= 1

	def _updateFlagNeighbors(self, col: int, row: int) -> None:
		""" 
		update effective label & adjacent tile number of 'M' tile neighbors
			input - 
				col (int): column index of 'M'
				row (int): row index of 'M'
		"""
		for x in [col-1, col, col+1]:
			for y in [row-1, row, row+1]:
				if (x >= 0 and y>= 0) and (x < self.__colDimension and 
					y < self.__rowDimension) and (x != col or y != row) and (
					self.getLabel(x, y) != 'M'):
					if self.getLabel(x, y) != '*':
						# update uncovered tile's effective labels
						self._updateEffectiveLabel(x, y)
					# update adjacent tile number
					self._updateAdjacentTileNum(x, y)


	def _updateNeighbors(self, col: int, row: int, number: int) -> None:
		""" 
		updates (col, row)'s neighbors adjacent covered tile number 
			input - 
				col (int): column index
				row (int): row index
				number (int): uncovered label 
		"""
		if number == 0 or self.getEffectiveLabel(col, row) == 0: 	# all neighbors are safe, add to safe dict
			self._effectiveZero(col, row, True)
		else: 	# effective label != 0 add neighbors to frontier
			for x in [col-1, col, col+1]: 
				for y in [row-1, row, row+1]:
					if (x >= 0 and y >= 0) and (x < self.__colDimension and 
						y < self.__rowDimension) and (x != col or y != row):
						self._updateAdjacentTileNum(x, y)
						# add (x, y) to frontier
						if (x, y) not in self.__safe:
							if ((x, y) not in self.__frontier and
								self.getLabel(x, y) == '*'):
								self.__frontier.update({(x,y):self.board[y][x]})
			self.__uncovered.update({(col, row):self.board[row][col]})
		# print(self.__frontier)
	
	def _effectiveZero(self, col: int, row: int, uncover = False) -> None:
		"""
		Update board after tile (col, row)'s effective label is 0
		adds safe tiles to safe dictionary and removes from frontier
			input - 
				col (int): column index
				row (int): row index
				uncover (boolean): 
					true - if getAction uncovered returned 0 label
					false - if effectivelabel = 0 after decrement 
		"""
		if uncover:		# update Adjacent Time Number
			for x in [col-1, col, col+1]: 
				for y in [row-1, row, row+1]:
					if (x >= 0 and y >= 0) and (x < self.__colDimension and 
						y < self.__rowDimension) and (x != col or y != row):
						self._updateAdjacentTileNum(x, y)
						# add (x, y) to safe dict
						if (x, y) not in self.__safe and self.getLabel(x, y) == '*':
							self.__safe.update({(x, y):self.board[y][x]})
						# remove (x, y) from frontier dict
						if (x, y) in self.__frontier:
							self.__frontier.pop((x, y))
		else:
			for x in [col-1, col, col+1]: 
				for y in [row-1, row, row+1]:
					if (x >= 0 and y >= 0) and (x < self.__colDimension and 
						y < self.__rowDimension) and (x != col or y != row):
						# add (x, y) to safe dict
						if (x, y) not in self.__safe and self.getLabel(x, y) == '*':
							self.__safe.update({(x, y):self.board[y][x]})
						# remove (x, y) from frontier dict
						if (x, y) in self.__frontier:
							self.__frontier.pop((x, y))


	
	def _updateAdjacentTileNum(self, x:int, y:int) -> None:
		"""
		decrement the internal adjacent covered tile counter
		checks rule of thumb
			input - 
				x (int): column index
				y (int): row index
		"""
		self.board[y][x][2] -= 1
		if self.board[y][x][2] == 0 and (x, y) in self.__uncovered:
			self.__uncovered.pop((x, y))
		self._checkRule(x, y)

	def _updateEffectiveLabel(self, x: int, y:int) -> None:
		"""
		decrement effective label by 1
			input - 
				x (int): column index
				y (int): row index
		"""
		if self.board[y][x][1]:
			self.board[y][x][1] -= 1
		self._checkRule(x, y)
		if self.getEffectiveLabel(x, y) == 0: 
			self._effectiveZero(x, y, False)
			

	def unmarkedNeighbors(self, colX: int, rowY:int) -> list:
		neighbors = list()
		for x in [colX-1, colX, colX+1]: 
			for y in [rowY-1, rowY, rowY+1]:
				if (x >= 0 and y >= 0) and (x < self.__colDimension and 
				y < self.__rowDimension) and (x != colX or y != rowY):
					if (self.board[y][x][0] == '*'):
						neighbors.append((x, y))

		return neighbors
	
	def _updateBoard(self, x: int, y: int, number: int) -> None:
		"""
		update board after uncover(x, y)
			input - 
				x (int): column index
				y (int): row index
				number (int): uncovered label
		"""
		# update label
		self.board[y][x][0] = number
		
		# update effective label
		self.board[y][x][1] = number - self._numMarkedNeighbors(x, y)

		# update neighbor's numCovered (following UNCOVER)
		self._updateNeighbors(x, y, number)
		#self._view()


	def _numMarkedNeighbors(self, col: int, row: int) -> int:
		"""
		calculate number of neighbors with M mine
			input - 
				col (int): column index
				row (int): row index
			return -
				count (int): number of neighbor mines
		"""
		count = 0
		for x in [col-1, col, col+1]: 
			for y in [row-1, row, row+1]:
				if (x >= 0 and y >= 0) and (x < self.__colDimension and 
				y < self.__rowDimension) and (x != col or y != row):
					if self.board[y][x][0] == 'M':
						count += 1
		return count

	def _view(self) -> None:
		"""prints board with row and col index 1 less than game board"""
		i = self.__rowDimension - 1
		for row in reversed(self.board):
			print('{i}'.format(i = i), end = '|\t')
			for x in row:
				if x[1] == None:
					print('{a}: :{c}'.format(a = x[0], c = x[2]), end = '\t')
				else:
					print('{a}:{b}:{c}'.format(a = x[0], b = x[1], c = x[2]),
						end = '\t')
			print(end = '\n')
			i -= 1
		for col in range(self.__colDimension):
			if col == 0:
				print('\t ▔▔▔', end='\t')
			else:
				print(' ▔▔▔', end='\t')
		print(end = '\n')
		for col in range(self.__colDimension):
			if col == 0:
				print('\t  {col}'.format(col = col), end='\t')
			else:
				print('  {col}'.format(col = col), end='\t')
		print(end = '\n')
	

	def getUncoveredNeighbors(self, colX: int, rowY:int) -> list:
		'''given tile (x, y), return all its neighbors that have been uncovered'''
		neighbors = list()
		for x in [colX-1, colX, colX+1]: 
			for y in [rowY-1, rowY, rowY+1]:
				if (x >= 0 and y >= 0) and (x < self.__colDimension and 
				y < self.__rowDimension) and (x != colX or y != rowY):
					if (self.board[y][x][0] != '*' and self.board[y][x][0] != 'M'):
						neighbors.append((x, y))
		return neighbors

	def modelCheck(self) -> dict:
	
		variables = list() #list of covered frontier tiles
		frontier_uncovered = dict() #uncovered frontier tiles mapping to list of unmarked neighbors
		#for tile in self.__frontier:

			#if self.board[tile[1]][tile[0]][0] == '*':
				#variables.append(tile)
				#break
		
		start = self.__frontier.popitem()
		self.__frontier.update({start[0]:start[1]})
		starting_tile = start[0]
		#frontier_uncovered[starting_tile] = list()
		variables.append(starting_tile)
		x = list()
		x.append(starting_tile)
		while x:
			tile = x.pop()
			neighbors = self.unmarkedNeighbors(tile[0], tile[1])
			for n in neighbors:
				if n in self.__frontier and n not in variables:
					variables.append(n)
					x.append(n)

		for tile in variables: #get uncovered frontier tiles (constraint tiles)
			uncovered = self.getUncoveredNeighbors(tile[0], tile[1])
			for neighbor in uncovered:
				if neighbor not in frontier_uncovered:
					frontier_uncovered[neighbor] = list()

		for tile in frontier_uncovered: #append covered tiles in frontier to tile in frontier_uncovered if it is a neighbor
			covered = self.unmarkedNeighbors(tile[0], tile[1])
			for c in covered:
				if c not in variables:
					variables.append(c)
			frontier_uncovered[tile] = self.unmarkedNeighbors(tile[0], tile[1])
			
		assignment = dict()
		var_num = len(variables)
		solution_dict = dict() #counts how many times a tile is a mine in a given solution
		models = self.getSolutions(assignment, frontier_uncovered, variables, var_num)
		num_of_solutions = len(models)

		for v in variables:
			solution_dict[v] = 0

		solutions = dict()
		solutions[0] = list() #list of tiles that are guaranteed safe
		solutions[1] = list() #list of tiles that are guaranteed mines
		solutions[2] = list() #list containing tile that is most likely to be safe

		for solution in models:
			for tile in solution_dict:
				if solution[tile] == 1: #each time tile is assigned 1 (mine), update solution_dict 
					solution_dict[tile] += 1
	
		for tile in solution_dict:
			if (solution_dict[tile]/num_of_solutions) == 1: #if tile was assigned a mine in every solution, append to mines list
				solutions[1].append(tile)
			elif (solution_dict[tile]/num_of_solutions) == 0: #if tile was safe in every solution, append to safe list
				solutions[0].append(tile)

		if len(solutions[0]) == 0 and len(solutions[1]) == 0:
			#if no tile is guaranteed safe or mine, find tile most likely to be safe
			guessTile = min(solution_dict, key = lambda x: x[1])
			solutions[2].append(guessTile)

		return solutions

	def satisfyConstraint(self, variables, constraint):
		'''
		given an assignment of variables, check if that assignment satisifies given constraints. return false if constraints 
		are violated. 
		'''
		for c in constraint:
			sum = 0 
			num = len(constraint[c])
			i = 0
			x, y = c
			label = self.getEffectiveLabel(x, y) #effective label acts as constraint
			for var in constraint[c]:
				if var in variables:
					sum += variables[var]
					i += 1
			if i == num and sum != label:
				return False
			elif i < num and sum > label:
				return False
		return True
	
	def getSolutions(self, assign, constraints, vars, num) -> list:
		'''
		recursive solver, assigns variables and checks constraints on each assignment. When a complete assignment is reached, it is added to 
		the solutions list. solutions list is returned
		'''
		solutions = [] #list of variable assignments that satisfy constraints
	
		if num == 0:
			return [assign] #if num is 0, then all variables have been assigned and the current assignment satisifes all constraints
		
		for v in vars: 
			#for each variable, assign it if it hasn't been assigned
			if v in assign: 
				continue
			assign[v] = 0
			#check if assignment of 0 satisfies constraint
			#if constraints not violated, copy current assignment and continue assigning variables in recursive call
			if self.satisfyConstraint(assign, constraints): 
				assign_copy = assign.copy()
				solutions += self.getSolutions(assign_copy, constraints, vars, num-1) 
			assign[v] = 1
			#check if assigning the variable to 1 satisfies constraint
			if self.satisfyConstraint(assign, constraints):
				assign_copy = assign.copy()
				solutions += self.getSolutions(assign_copy, constraints, vars, num-1)

			return solutions		
				