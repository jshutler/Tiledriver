# Name:         
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Tile Driver
# Term:         Fall 2020

import queue
from typing import List, Tuple
from random import randint


class Heuristic:

    @staticmethod
    def get(tiles: Tuple[int, ...]) -> int:
        """
        Return the estimated distance to the goal using Manhattan distance
        and linear conflicts.

        Only this static method should be called during a search; all other
        methods in this class should be considered private.

        >>> Heuristic.get((0, 1, 2, 3))
        0
        >>> Heuristic.get((3, 2, 1, 0))
        6
        """
        width = int(len(tiles) ** 0.5)
        return (Heuristic._get_manhattan_distance(tiles, width)
                + Heuristic._get_linear_conflicts(tiles, width))

    @staticmethod
    def _get_manhattan_distance(tiles: Tuple[int, ...], width: int) -> int:
        """
        Return the Manhattan distance of the given tiles, which represents
        how many moves is tile is away from its goal position.
        """
        distance = 0
        for i in range(len(tiles)):
            if tiles[i] != 0:
                row_dist = abs(i // width - tiles[i] // width)
                col_dist = abs(i % width - tiles[i] % width)
                distance += row_dist + col_dist
        return distance

    @staticmethod
    def _get_linear_conflicts(tiles: Tuple[int, ...], width: int) -> int:
        """
        Return the number of linear conflicts in the tiles, which represents
        the minimum number of tiles in each row and column that must leave and
        re-enter that row or column in order for the puzzle to be solved.
        """
        conflicts = 0
        rows = [[] for i in range(width)]
        cols = [[] for i in range(width)]
        for i in range(len(tiles)):
            if tiles[i] != 0:
                if i // width == tiles[i] // width:
                    rows[i // width].append(tiles[i])
                if i % width == tiles[i] % width:
                    cols[i % width].append(tiles[i])
        for i in range(width):
            conflicts += Heuristic._count_conflicts(rows[i])
            conflicts += Heuristic._count_conflicts(cols[i])
        return conflicts * 2

    @staticmethod
    def _count_conflicts(ints: List[int]) -> int:
        """
        Return the minimum number of tiles that must be removed from the given
        list in order for the list to be sorted.
        """
        if Heuristic._is_sorted(ints):
            return 0
        lowest = None
        for i in range(len(ints)):
            conflicts = Heuristic._count_conflicts(ints[:i] + ints[i + 1:])
            if lowest is None or conflicts < lowest:
                lowest = conflicts
        return 1 + lowest

    @staticmethod
    def _is_sorted(ints: List[int]) -> bool:
        """Return True if the given list is sorted and False otherwise."""
        for i in range(len(ints) - 1):
            if ints[i] > ints[i + 1]:
                return False
        return True



class Tile_Puzzle:
    def __init__(self, size=3, initial_state=None, scramble_size=30):
        #if initial state is provided
        if initial_state is not None:
            self.puzzle = list(initial_state)
            self.empty_location_index = self.puzzle.index(0)
       
        #if we don't provide an initial state
        else:
            self.puzzle = list(range(self.puzzle_size ** 2))
            self.empty_location_index = 0
            self.scramble(scramble_size)


        self.puzzle_size = int(len(self.puzzle)**.5)

        
        

    @property   
    def possible_moves(self):
        all_moves = ["K","J","H","L"]
        possible_moves = []

        for move in all_moves:
            move_index = self.get_move_index(move)
            
            if move_index is None:
                continue
            
            possible_moves.append(move)

        return possible_moves

            
    @property   
    def frontier_states(self):
        """Gives a dictionary of all frontiers available from this position. with the move as the key Used to make the AI"""
        frontier_states = {}

        # print(self.possible_moves)

        for move in self.possible_moves:
            frontier_state = self.get_next_state(move)
            
            if move is None:
                continue

            frontier_states[move] = frontier_state

        return frontier_states

    def __repr__(self):
        return ' '.join([str(i) for i in self.puzzle])

    def get_move_index(self, move: str) -> int or None:
        """Gives us the index of the piece we want to move"""

        move_dict = {"K": 3, "J": -3, "H": -1, "L": 1}  

        # print(move)

        move_index = self.empty_location_index + move_dict[move]

        #if we are outside the bounds of the puzzle, return None
        invalid_move = (move_index < 0 or move_index >= self.puzzle_size) or \
        ((self.empty_location_index == 2 or self.empty_location_index == 5) and move_dict[move] == 1) or \
        ((self.empty_location_index == 3 or self.empty_location_index == 6) and move_dict[move] == -1)


        if invalid_move: 
            return None

        return move_index

   
    def get_next_state(self, move: str) -> list:
        """Returns the puzzle in a state of what the given move woould make it"""
        index_of_piece_moving = self.get_move_index(move)

        
        if index_of_piece_moving is None:
            return None 

        #gives us a copy of the puzzle
        copy_of_puzzle = self.puzzle[:]

        copy_of_puzzle[self.empty_location_index] = copy_of_puzzle[index_of_piece_moving]

        copy_of_puzzle[index_of_piece_moving] = 0

        return copy_of_puzzle


    def move_piece(self, move: str) -> bool:



        index_of_piece_moving = self.get_move_index(move)

        
        if index_of_piece_moving is None:
            return False 
        
        self.puzzle[self.empty_location_index] = self.puzzle[index_of_piece_moving]

        self.puzzle[index_of_piece_moving] = 0

        self.empty_location_index = index_of_piece_moving

        return True
        

    def scramble(self, scramble_size=30) -> None:
        possible_moves = ['K', 'J', 'H', 'L']

        #ensures the scramble can be even or odd 
        scramble_size = randint(scramble_size, scramble_size+1)

        i = 0

        while i <= scramble_size:
            move = possible_moves[randint(0,3)]

            piece_is_moved = self.move_piece(move)

            if piece_is_moved:
                i += 1


class State_Node:
    #defining what a node will be for our a_star_search_tree
    def __init__(self, state, previous_state, g, h):
        self.state = state
        self.visited = False
        self.previous = previous_state
        self.frontiers = []
        self.path_from_initial = []

        #distance from initial state
        self.g = g
        #estimated distance to goal
        self.h = h
        #most important distance
        self.f = g + h


        def __repr__(self):
            return self.state

class A_Star_Search:
    def __init__(self, initial_state: Tuple[int, ...]):
        self.puzzle = Tile_Puzzle(initial_state = initial_state)
        self.frontiers = self.puzzle.frontier_states






        



def solve_puzzle(tiles: Tuple[int, ...]) -> str:
    """
    Return a string (containing characters "H", "J", "K", "L") representing the
    optimal set of moves to solve the given puzzle.

    """
    puzzle = A_Star_Search(tiles)



def main() -> None:
    """Optional: Use as a driver to test your program."""
    # initial_state = make_puzzle(size=3)
    solve_puzzle((1,2,0,3,4,5,6,7,8))






          



if __name__ == "__main__":
    main()
