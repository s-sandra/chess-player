# Chess Player
This graphical chess simulator, created by Stephen Davies as part of a college AI programming tournament in fall 2019, runs a chess game 
against two `ChessPlayer` objects. The simulator executes individual player turns by calling strategies outlined by each `ChessPlayer`. 
Using Stephen’s existing framework, I inherited from the `ChessPlayer` base class as `ashtabna_ChessPlayer`, which contains tactics for move 
selection.

# Game Rules
The simulator adheres to the traditional rules of chess, but with the following exceptions.

- <b>Pawn Promotion</b> If a pawn advances to the opposite rank, it becomes a queen.
- <b><i>En Passant</i> Pawn Captures</b> Are illegal.
- <b>Castling</b> You can avoid check by swapping the king’s position with a rook if neither pieces have ever moved and all spaces in
between them are empty.
- <b>Draws</b> Stalemate occurs when the king is not in check and there are no more legal moves.
- <b>The Princess</b> There is a make-believe chess piece called the Princess, which moves like the Queen, but no more than three pieces in any direction.
- <b>The Fool</b> There is a make-believe chess piece called the Fool, which moves two spaces in any direction.

# Strategy
My `ChessPlayer` implements an iterative deepening, minimax algorithm, searching as far ahead in the game tree as possible. After a 
time limit of five seconds, it plays the best move it found. I optimized the search process by using alpha-beta pruning and storing 
previously evaluated board states in a transposition table, indexed with Zobrist keys. The algorithm rates board states using a simple 
heuristic function that computes the material balance.

# Interface
The chess game simulator has several available presets (listed below). After each game, the simulator saves a transcript in the current 
directory as a `.log` file. The file contains the starting board state, the list of moves and other game metadata. 

## Board Sizes
- <b>Reg</b> The standard 8 x 8 chess board. This is default.
- <b>Mini</b> You can play a game on a 6 x 6 chess board.
- <b>Large</b> An 8 x 10 chess board.

## Player Modes
- <b>Human v Human</b> No algorithms will be run. Human players can move chess pieces by clicking and dragging them to the desired 
position. This is the default.
- <b>Human v Computer</b> A human player competes against the selected `ChessPlayer` algorithm (chosen by the drop down menu to the 
immediate left of the “Start Game” button). Human players select moves by clicking and dragging pieces to the desired position.
- <b>Computer v Computer</b> An automated chess game, played by two competing `ChessPlayer` algorithms (chosen by the drop down 
menus to the left of the “Start Game” button). Note that you can set an algorithm against itself.

## Crazy Mode
The simulator can operate in crazy mode, where all chess positions at the beginning of the game are chosen randomly and each player’s 
positions are mirror images of each other. This mode is not enabled by default.

