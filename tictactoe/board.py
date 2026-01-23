# Tic Tac Toe
def display_board(dboard:dict)->None:
    """Display the board"""

    d = dboard
    
    print(f"{d[0]:2s}|{d[1]:2s}|{d[2]:2s}")
    print("--+---+---")

    print(f"{d[3]:2s}|{d[4]:2s}|{d[5]:2s}")
    print("--+---+---")

    print(f"{d[6]:2s}|{d[7]:2s}|{d[8]:2s}")
def player_turn(player:str, dboard:dict)->int:
    """ask player for a move
    """
    valid_move = False
    user_input = input(f"{player}'s turn. Enter a number between 0 and 8: ")
    user_input = int(user_input)
    print(f"Value entered: {user_input} type: {type(user_input)}")
    if user_input in dboard.keys():
        if dboard[user_input] not in ["X", "O"]:
            dboard[user_input] = player
            valid_move = True
        else:
            print("Invalid move")
    else:
        print("Invalid move")
    return valid_move

        
    
if   __name__ == "__main__":
    board = {x:str(x) for x in range(9)}
    display_board(board)
    move = player_turn("X", board)
    print(f"Move: {move}")
    #board[0] = "X"
    #board[4] = "O"
    #board[8] = "X"
    move = player_turn("O", board)
    print(f"Move: {move}")
    move = player_turn("X", board)
    print(f"Move: {move}")
    print(board)
    #display_board(board)
