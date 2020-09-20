# Name:         
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Tile Driver
# Term:         Fall 2020

import queue
from typing import List, Tuple


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


def solve_puzzle(tiles: Tuple[int, ...]) -> str:
    """
    Return a string (containing characters "H", "J", "K", "L") representing the
    optimal set of moves to solve the given puzzle.
    """
    left = "H"
    down = "J"
    up = "K"
    right = "L" 



def make_puzzle(initial_state, size=None):
    pass


def main() -> None:
    """Optional: Use as a driver to test your program."""
    initial_state = make_puzzle(size=2)



if __name__ == "__main__":
    main()
