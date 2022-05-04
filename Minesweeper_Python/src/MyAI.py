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
from collections import deque

totalTime = 5 * 60.0 		# time allowed for one game
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
		self.__frontierD = deque()

		# */M/n : Effective Label : # adjacent covered/unmarked tiles
		# * = Covered/Unmarked / M = Mine(Covered/Marked) / n = label(Uncovered)
		# Effective Label = Label - NumMarkedNeighbors
		# initialize board to all *:None:0
		for y in range(rowDimension):
			row = []
			for x in range(colDimension):
				if (y == 0 or y == rowDimension - 1) and (x == 0 or x == colDimension -1):
					row.append(['*', None, 3]) # numCovered = 3
				elif y == 0 or y == rowDimension - 1 or x == 0 or x == colDimension -1:
					row.append(['*', None, 5]) # numCovered = 5
				else: 
					row.append(['*', None, 8]) # numCovered = 8
			self.board.append(row)

		# update first uncovered tile's efffective label
		self.board[startY][startX][1] = 0

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

		# update board (previous getAction label)
		self.board[self.__lastY][self.__lastX][0] = number
		self.board[self.__lastY][self.__lastX][1] = number

		# update neighbor's numCovered (from previous UNCOVER)
		self._updateNeighbors(self.__lastX, self.__lastY)
		self._view()

		# rule of thumb
		if self.EffectiveLabel(self.__lastX, self.__lastY) == self.NumUnmarkedNeighbors(self.__lastX, self.__lastY):
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
			# x, y = self.__frontier.popitem()[0]
			x, y = self.__frontierD.popleft()[0]
			 
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

	# Effective Label = Label - NumMarkedNeighbors
	def EffectiveLabel(self, x, y):
		return self.board[y][x][1]

	def NumUnmarkedNeighbors(self, x, y):
		return self.board[y][x][2]

	def FlagAdjacent(self, col, row):
		"""flag adjacent tiles as mines"""
		for x in [col-1, col, col+1]:
			for y in [row-1, row, row+1]:
				if (x >= 0 and y>= 0) and (x < self.__colDimension and 
				y < self.__rowDimension) and (x != col or y != row) and (self.board[y][x][0] == '*'):
					self.board[y][x][0] = 'M'
		

	def _updateNeighbors(self, colX, rowY):
		""" updates (colX, rowY)'s neighbors' adjacent covered tile number """
		for x in [colX-1, colX, colX+1]: 
			for y in [rowY-1, rowY, rowY+1]:
				if (x >= 0 and y >= 0) and (x < self.__colDimension and 
				y < self.__rowDimension) and (x != colX or y != rowY):
					self._updateAdjacentTileNum(x, y)
					# update frontier
					if self.__frontier.get((x,y)) == None and self.board[y][x][0] == '*':
						self.__frontier.update({(x,y):self.board[y][x]})
					if not([(x,y),[self.board[y][x]]] in self.__frontierD)  and self.board[y][x][0] == '*':
						self.__frontierD.append([(x,y),[self.board[y][x]]])
		# print(self.__frontier)
	
	def _updateAdjacentTileNum(self, x, y):
		""" decreases the internal adjacent covered tile counter by one"""
		self.board[y][x][2] -= 1

	def _updateEffectiveLabel(self, x, y):
		"""decrease effective label by 1"""
		self.board[y][x][1] -= 1

	def unmarkedNeighbors(self, colX, rowY):
		neighbors = list()
		for x in [colX-1, colX, colX+1]: 
			for y in [rowY-1, rowY, rowY+1]:
				if (x >= 0 and y >= 0) and (x < self.__colDimension and 
				y < self.__rowDimension) and (x != colX or y != rowY):
					if (self.board[y][x][0] == '*'):
						neighbors.append((x, y))

		return neighbors
	
	def UpdateBoard(tile):
		pass

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
			