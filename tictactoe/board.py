# Tic Tac Toe
def display_board(dboard:dict)->None:
    """Display the board"""

    d = dboard
    print(f"{d[0]}:2s | {d[1]}:2s | {d[2]}:2s")
    print("---+---+---")
    print(f"{d[3]}:2s | {d[4]}:2s | {d[5]}:2s")
    print("---+---+---")
    print(f"{d[6]}:2s | {d[7]}:2s | {d[8]}:2s")
def player_turn(player:str, board:dict)->int:
    "ask player for a move
    "
    
if   __name__ == "__main__":
    board = {x:str(x) for x in range(9)}
    display_board(board)
    board[0] = "X"
    board[4] = "O"
    board[8] = "X"
    display_board(board)
