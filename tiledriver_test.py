from tiledriver import *
from random import randint


def main(size=3, scramble_size=30):
	"""This function  will take advantage of the TilePuzzle's Scramble method, which will scramble a solved puzzle 
	in a random fashion. Then we can give the scrambled puzzle to solve_puzzle to see if it can solve it.
	We can vary the size of the puzzle, as well as how much we want to scramble the puzzle before attempting to solve.
	This function can provide test data for how quickly the tiledrive solves puzzles"""
	puzzle = TilePuzzle(size = size, scramble_size=scramble_size)
	optimal_path = solve_puzzle(puzzle.puzzle)
	print(optimal_path)

if __name__ == '__main__':
	iterations = 1000
	for i in range(iterations):
		main()
