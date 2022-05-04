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
import random

totalTime = 5.0 # time allowed for one game
totalTimeElapsed = 0.0

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.__rowDimension = rowDimension
		self.__colDimension = colDimension
		self.totalMines = totalMines
		self.flaggedTiles = 0
		self.coveredTilesLeft = rowDimension * colDimension
		self.board = list() #list of list of tuples
		self.__lastX = startX
		self.__lastY = startY

		# */M/n : Effective Label : # adjacent covered/unmarked tiles
		# * = Covered/Unmarked
		# M = Mine (Covered/Marked)
		# n = label (Uncovered)
		# Effective Label = Label - NumMarkedNeighbors
		# initialize board to all *:0:0
		for i in range(rowDimension):
			self.board.append([['*', 0, 0]] * colDimension)

		# label first tile 0:0:8
		self.board[startX][startY][0] = 0
		self.board[startX][startY][1] = 0
		self.board[startX][startY][2] = 8

		self.coveredTilesLeft -= 1
		


		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		# update board
		self.board[self.__lastX][self.__lastY][0] = number

		# exit condition
		if self.flaggedTiles == self.totalMines:
			return Action(AI.Action.LEAVE)
		
		if self.coveredTilesLeft <= self.totalMines:
			return Action(AI.Action.LEAVE)
		
		action = AI.Action(random.randrange(len(AI.Action)))
		x = random.randrange(self.__colDimension)
		y = random.randrange(self.__rowDimension)
		self.coveredTilesLeft += 1
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

	def EffectiveLabel(x):
		pass

	def NumUnmarkedNeighbors(x):
		pass
	
	# def getUncoveredAdjacent(tile) -> (x, y):
	# 	pass
	
	def UpdateBoard(tile):
		pass