# Tiledriver
Project for CSC 480 (Aritificial Intelligence) Writing an AI solve the sliding tile puzzle using the A* Search algorithm.

In this project I defined 3 main classes:

1. TilePuzzle
2. Tiledriver
3. StateNode

## TilePuzzle
TilePuzzle defines the sliding puzzle game. It will allow you to set the size of the puzzle (nxn), as well as let you provide an initial state for the puzzle 
in which you want to solve. If no initial state is given, it will generate a random puzzle of a user defined size. 

## StateNode
StateNode defines all the important characteristics of a given state of the puzzle:

1. state: What the current arrangement of tiles is
2. puzzle: a TilePuzzle object
2. Previous: What the previous node was
3. path_from_start: The current set of moves that have been taken to get the from the initial node to this node
4. g: the number of moves made from the start
5. h: a Heuristic which provides an approximation this node is from the goal state. 
6. f: g + h


## Tiledriver

Tiledriver uses StateNodes to utilize the A* Search in order to find the optimal number of moves to the goal state. 
It requires an the initial state of a puzzle, and then finds the optimal path to solve it by searching StateNodes with lowest f value.




The Heuristic class was given to me by my professor, but the rest was written exclusively by me.
