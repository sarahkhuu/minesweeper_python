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

totalTime = 5.0 		# seconds allowed for one game
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
		self.coveredTilesLeft = rowDimension * colDimension
		self.board = list() 	# list of list of lists
		self.__lastX = startX	# x = column coordinate
		self.__lastY = startY	# y = row coordinate
		self.__frontier = {}	# dictionary (x,y):[a,b,c]
		self.__safe = {}		# dictionary (x,y):[a,b,c]

		# */M/n : Effective Label : # adjacent covered/unmarked tiles
		# * = Covered/Unmarked / M = Mine(Covered/Marked) / n = label(Uncovered)
		# Effective Label = Label - NumMarkedNeighbors
		# initialize board to all *:None:0
		for y in range(rowDimension):
			row = []
			for x in range(colDimension):
				if (y == 0 or y == rowDimension - 1) and (
					x == 0 or x == colDimension -1):
					row.append(['*', None, 3]) # numCovered = 3
				elif y == 0 or y == rowDimension - 1 or x == 0 or \
					x == colDimension -1:
					row.append(['*', None, 5]) # numCovered = 5
				else: 
					row.append(['*', None, 8]) # numCovered = 8
			self.board.append(row)

		self.coveredTilesLeft -= 1

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

		# update board (previous getAction result)
		self._updateBoard(self.__lastX, self.__lastY, number)
		print("Covered Tiles left: ", self.coveredTilesLeft)

		# rule of thumb
		if self.getEffectiveLabel(self.__lastX, self.__lastY) == \
			self.getNumUnmarkedNeighbors(self.__lastX, self.__lastY):
			self.FlagAdjacent(self.__lastX, self.__lastY)
			#flag all adjacent covered tiles as mines
		
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

			# CHANGE THIS:
			action = AI.Action(1)
			if self.__safe:
				x, y = self.__safe.popitem()[0]
			else:
				x, y = self.__frontier.popitem()[0]
				while (self.__frontier):
					if self.getLabel(x,y) == '*':
						break
					else:
						x, y = self.__frontier.popitem()[0]

				print("x, y: ", x, y)
			 
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
				x: int column index
				y: int row index			
			return -  
				label: 	* = Covered/Unmarked
						M = Mine(Covered/Marked)
						n = label(Uncovered)
		"""
		return self.board[y][x][0]

	def getEffectiveLabel(self, x, y):
		""" 
		get effective label helper function
		Effective Label = Label - NumMarkedNeighbors
			input - 
				x: int column index
				y: int row index
			return - 
				int EffectiveLabel: Label - NumMarkedNeighbors
		"""
		return self.board[y][x][1]

	def getNumUnmarkedNeighbors(self, x, y):
		""" 
		get number of Unmarked Neighbor helper function
			input - 
				x: int column index
				y: int row index		
			return - 
				NumUnmarkedNeighbors: int
		"""
		return self.board[y][x][2]

	def _checkRule(self, x, y):
		"""checks if effectivelabel(x) = numUnMarkedNeighbors on last x, y"""
		if self.getEffectiveLabel(x, y) == self.getNumUnmarkedNeighbors(x, y):
			self.FlagAdjacent(x, y)
			#flag all adjacent covered tiles as mines

	def FlagAdjacent(self, col, row):
		"""flag adjacent tiles as mines"""
		for x in [col-1, col, col+1]:
			for y in [row-1, row, row+1]:
				if (x >= 0 and y>= 0) and (x < self.__colDimension and
					y < self.__rowDimension) and (x != col or y != row) and\
					(self.getLabel(x,y) == '*'):
					self.board[y][x][0] = 'M'
					self.board[y][x][1] = None
					self._updateFlagNeighbors(x,y)

	def _updateFlagNeighbors(self, col, row) -> None:
		""" Update Effective label of flagged 'M' Tile"""
		for x in [col-1, col, col+1]:
			for y in [row-1, row, row+1]:
				if (x >= 0 and y>= 0) and (x < self.__colDimension and 
					y < self.__rowDimension) and (x != col or y != row) and (
					self.getLabel(x,y) != 'M' and self.getLabel(x,y) != '*'):
					self._updateEffectiveLabel(x,y)


	def _updateNeighbors(self, colX, rowY, number) -> None:
		""" updates (colX, rowY)'s neighbors' adjacent covered tile number """
		if (number == 0): 	# all neighbors are safe, add to safe
			for x in [colX-1, colX, colX+1]: 
				for y in [rowY-1, rowY, rowY+1]:
					if (x >= 0 and y >= 0) and (x < self.__colDimension and 
						y < self.__rowDimension) and (x != colX or y != rowY):
						self._updateAdjacentTileNum(x, y)
						self._checkRule(x,y)
						# update safe dict
						if not ((x,y) in self.__safe) and self.getLabel(x,y) == '*':
							self.__safe.update({(x,y):self.board[y][x]})
		else: 	# effective label != 0 add neighbors to frontier
			for x in [colX-1, colX, colX+1]: 
				for y in [rowY-1, rowY, rowY+1]:
					if (x >= 0 and y >= 0) and (x < self.__colDimension and 
						y < self.__rowDimension) and (x != colX or y != rowY):
						self._updateAdjacentTileNum(x, y)
						self._checkRule(x,y)
						# update frontier
						if not ((x,y) in self.__safe):
							if not ((x,y) in self.__frontier) and\
								self.getLabel(x,y) == '*':
								self.__frontier.update({(x,y):self.board[y][x]})
		# print(self.__frontier)
	
	def _updateAdjacentTileNum(self, x:int, y:int) -> None:
		""" decreases the internal adjacent covered tile counter by one"""
		self.board[y][x][2] -= 1

	def _updateEffectiveLabel(self, x: int, y:int) -> None:
		"""decrease effective label by 1"""
		if self.board[y][x][1]:
			self.board[y][x][1] -= 1

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
		"""update board with previous uncover of x, y tile"""
		# update label
		self.board[y][x][0] = number
		
		# update effective label
		self.board[y][x][1] = number 
		- self._numMarkedNeighbors(x, y)

		# update neighbor's numCovered (following UNCOVER)
		self._updateNeighbors(x, y, number)
		self._view()

		

	def _numMarkedNeighbors(self, colX: int, rowY: int) -> int:
		"""returns number of neighbors with M mine """
		count = 0
		for x in [colX-1, colX, colX+1]: 
			for y in [rowY-1, rowY, rowY+1]:
				if (x >= 0 and y >= 0) and (x < self.__colDimension and 
				y < self.__rowDimension) and (x != colX or y != rowY):
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
					print('{a}:{b}:{c}'.format(a = x[0], b = x[1], c = x[2]), end = '\t')
			print(end = '\n')
			i -= 1
		for col in range(self.__colDimension):
			if col == 0:
				print('\t  {col}'.format(col = col), end='\t')
			else:
				print('  {col}'.format(col = col), end='\t')
		print(end = '\n')
			