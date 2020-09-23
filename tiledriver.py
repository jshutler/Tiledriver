# Name:         
# Course:       CSC 480
# Instructor:   Daniel Kauffman
# Assignment:   Tile Driver
# Term:         Fall 2020

import queue
from typing import List, Tuple
# from random import randint


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
            self.puzzle = list(range(size ** 2))
            self.puzzle_size = int(len(self.puzzle))
            self.empty_location_index = 0
            self.scramble(scramble_size)


        self.puzzle_size = int(len(self.puzzle))

        
        

    @property   
    def possible_moves(self):
        all_moves = ["K","J","H","L"]
        possible_moves = []

        for move in all_moves:
            # print(move)
            move_index = self.get_move_index(move)
            
            if move_index is None:
                continue
            
            possible_moves.append(move)

        return possible_moves

            
    @property   
    def frontier_states(self) -> dict:
        """Gives a dictionary of all frontiers available from this position. with the move as the key Used to make the AI"""
        frontier_states = {}

        # print(self.possible_moves)
        possible_moves = self.possible_moves
        for move in possible_moves:
            # print(move)
            frontier_state = self.get_next_state(move)
            
            if move is None:
                continue

            #making it a set, because prof wants a set
            frontier_states[move] = tuple(frontier_state)

        return frontier_states

    def __repr__(self):
        return ' '.join([str(i) for i in self.puzzle])

    def get_move_index(self, move: str) -> int or None:
        """Gives us the index of the piece we want to move"""

        move_dict = {"K": 3, "J": -3, "H": -1, "L": 1}  

        

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
        from random import randint
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
    #defining what a node will be for our Tiledriver_tree
    def __init__(self, state: tuple, previous=None, last_move=None, g=0):
        self.state = state
        self.puzzle = Tile_Puzzle(initial_state=state)
        self.visited = False
        self.previous = previous
        self.local_frontiers = self.puzzle.frontier_states
        
        if self.previous is None:
            self.path_from_start = []
        else:
            #gives me a copy of the previous nodes path to start
            self.path_from_start = previous.path_from_start[:]
            self.path_from_start.append(last_move)
            # print(self.path_from_start)


        #distance from start
        self.g = g

        #estimated distance to goal
        self.h = Heuristic.get(state)
        #most important distance
        self.f = self.g + self.h


    def __repr__(self):
        return " ".join([str(x) for x in self.state])

    def __lt__(self, other):
        """We need this for the Priority queue, but there is no good way to define less than or greater than
        for a state. so we will just arbitrarily return the first one"""
        return self
        pass

class Tiledriver:
    def __init__(self, initial_state: Tuple[int, ...]):
        self.initial_node = State_Node(initial_state)
        #gives what frontier to search next
        self.all_frontiers = queue.PriorityQueue()
        self.goal = tuple(sorted(list(initial_state)))

    def main(self) -> str:
        #adding the initial frontiers
            # self.add_frontiers()

        #searching our starting node
        self.add_frontiers(self.initial_node)


       #searching next node 
        next_move, new_node = self.all_frontiers.get()

        while new_node.h != 0:
            self.add_frontiers(new_node)
            #searching next node 
            next_move, new_node = self.all_frontiers.get()

        print(self.initial_node)
        print(new_node.path_from_start)
        print(new_node)

        return ''.join(new_node.path_from_start)
            


        # while current_node.state != self.goal:
        #     self.search_node()


    def add_frontiers(self, node=None):
        """Adds new frontiers to the total number of frontiers to search"""
        #lets us loop through the move that gets us to the frontier, and the frontier itself
        for move, frontier in zip(node.local_frontiers.keys(), node.local_frontiers.values()):
            frontier_node = State_Node(frontier, previous=node, last_move=move, g=node.g+1)
            self.all_frontiers.put((frontier_node.f, frontier_node))
            # print(self.all_frontiers.get())
        
        #we don't want to add a frontier state that will simply reverse us back to where we were
        opposite_move = {"K":"J", "J":"K", "L":"H", "H":"L"}






    def print_frontiers(self):
        while not self.all_frontiers.empty():
            f, frontier = self.all_frontiers.get()
            print(frontier)
            print('current_path: ', frontier.path_from_start)

        



def solve_puzzle(tiles: Tuple[int, ...]) -> str:
    """
    Return a string (containing characters "H", "J", "K", "L") representing the
    optimal set of moves to solve the given puzzle.

    """
    puzzle = Tiledriver(tiles)
    optimal_path = puzzle.main()
    return optimal_path
    # while not puzzle.all_frontiers.empty():
    #     item = puzzle.all_frontiers.get()
    #     print(item)



def main() -> None:
    """Optional: Use as a driver to test your program."""
    # initial_state = make_puzzle(size=3)
    state = (1,4,2,3,0,5,6,7,8)
    puzzle_state = Tile_Puzzle(scramble_size=1000).puzzle
    optimal_path = solve_puzzle(puzzle_state)

    print(puzzle_state)
    print(optimal_path, len(optimal_path))







          



if __name__ == "__main__":
    main()
