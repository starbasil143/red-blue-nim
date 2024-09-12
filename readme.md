# Red Blue Nim

Nim is a classic game in which two (or more) players take turn removing some amount of objects from some pool of objects. Depending on which version you are playing, the player who takes the last object from a pool either wins or loses. This version of the game has the players taking either 2 or 3 marbles from either the red marble pile or the blue marble pile. In the "standard" version, the player who takes the final marble in either pile is the loser. In the "misère" version, that player is the winner. When the game finishes, the remaining marbles are converted into points, with blue marbles being worth three, and red marbles being worth two.

This repository provides an AI opponent to play against in red-blue nim. It uses a depth-limited minimax algorithm with alpha-beta pruning, and always selects the best possible move. Good luck.
## How to run

Run with python as:  
`py red_blue_nim.py <red> <blue> <gamemode> <firstplayer>` where red is number of red marbles, blue is number of blue marbles, gamemode is either "standard" or "misere" (defaults to standard), and firstplayer is either "human" or "computer" (defaults to computer)  

Examples:

`py red_blue_nim.py 14 3 standard human`  
`py red_blue_nim.py 5 7 misere`             (defaults to computer going first)  
`py red_blue_nim.py 3 3 hgasdlvsndjvsdnlfvb computer` (defaults to standard)  
`py red_blue_nim.py 1 1 standard computer` (kind of cheating, but works)  
`py red_blue_nim.py 0 9999 standard computer` (ok thats just kind of cruel)  

## Technical Details

Uses python 3.12.2

Mainly centers around a statenode class, which has its own 
functions, including the beginning of the minmax search. The
class automatically generates each node's children upon creation,
recursively. The max and min functions are outside of the class, and
the player input and winning/losing is within main.