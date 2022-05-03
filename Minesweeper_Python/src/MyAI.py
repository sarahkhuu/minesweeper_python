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
from time import time

time = 0
class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.__rowDimension = rowDimension
		self.__colDimension = colDimension
		self.totalMines = totalMines
		self.flaggedTiles = 0
		self.board = list() #list of list of tuples
		self.lastX = startX
		self.lastY = startY
		#initialize board to all 0's
		for i in range(rowDimension):
			board.append([(*, 0, 0)] * colDimension)

		board[startX][startY][0] = 0
		board[startX][startY][1] = 0
		board[startX][startY][2] = 8
		


		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		#update board
		board[lastX][lastY][0] = number

		#exit condition
		if self.flaggedTiles = self.totalMines:
			return Action(AI.Action.LEAVE)

		#rule of thumb
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

	def EffectiveLabel(x):
		pass

	def NumUnmarkedNeighbors(x):
		pass
	
	def getUncoveredAdjacent(tile) -> (x, y):
		pass
	
	def UpdateBoard(tile):
		pass