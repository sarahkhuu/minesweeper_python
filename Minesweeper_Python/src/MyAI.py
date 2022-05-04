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

totalTime = 5.0 		# time allowed for one game
totalTimeElapsed = 0.0

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		print("START: ", startX, startY)
		self.__rowDimension = rowDimension
		self.__colDimension = colDimension
		self.totalMines = totalMines
		self.flaggedTiles = 0
		self.coveredTilesLeft = rowDimension * colDimension
		self.board = list() 	# list of list of tuples
		self.__lastX = startX	# x = column coordinate
		self.__lastY = startY	# y = row coordinate

		# */M/n : Effective Label : # adjacent covered/unmarked tiles
		# * = Covered/Unmarked
		# M = Mine (Covered/Marked)
		# n = label (Uncovered)
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

		# label first uncovered tile 0:0:numCovered
		# self.board[startY][startX][0] = 0  (is updated in first getAction)
		self.board[startY][startX][1] = 0

		# update neighbor's numCovered!!
		print()
		self.__view()

		self.coveredTilesLeft -= 1
		


		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		# exit condition (FLAG OR UNCOVERED?)
		if self.flaggedTiles == self.totalMines:
			return Action(AI.Action.LEAVE)
		
		if self.coveredTilesLeft <= self.totalMines:
			return Action(AI.Action.LEAVE)

		# update board (previous getAction label)
		self.board[self.__lastY][self.__lastX][0] = number
		print(self.__view())
		
		global totalTimeElapsed 
		remainingTime = totalTime - totalTimeElapsed
		if remainingTime < 0.1:
			# random move
			action = AI.Action(1)
			x = random.randrange(self.__colDimension)
			y = random.randrange(self.__rowDimension)
			self.coveredTilesLeft += 1
			self.__lastX = x
			self.__lastY = y
			return Action(action, x, y)
		else :
			timeStart = time.time()

			# CHANGE THIS:
			action = AI.Action(1)
			x = random.randrange(self.__colDimension)
			y = random.randrange(self.__rowDimension)
			self.coveredTilesLeft += 1

			self.__lastX = x
			self.__lastY = y

			timeEnd = time.time()
			timeDifference = timeStart - timeEnd
			totalTimeElapsed += timeDifference	# update time used for call

			return Action(action, x, y)


		# rule of thumb
		if EffectiveLabel(tile) == NumUnmarkedNeighbors(tile):
			return Action(2, coordx, coordy)

		if EffectiveLabel(tile) == 0:
			next_tile = getUncoveredAdjacent(tile)
			lastX = next_tile[0]
			lastY = next_tile[1]
			return Action(1, next_tile[0], next_tile[1])
		


		
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	# Effective Label = Label - NumMarkedNeighbors
	def EffectiveLabel(x, y):
		pass

	def NumUnmarkedNeighbors(x):
		pass

	# def __updateNeighbors__(x, y):
	# 	for x in range(x)
	
	# def getUncoveredAdjacent(tile) -> (x, y):
	# 	pass
	
	def UpdateBoard(tile):
		pass

	def __view(self):
		i = self.__rowDimension
		for row in reversed(self.board):
			print('{i}: {row}'.format(i = i, row = row))
			i -= 1