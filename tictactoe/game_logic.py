import board

def check_winner(d:dict, combo_list:list)->bool:
    """
    Check if there is a winner
    """
    for combo in combo_list:
        if d[combo[0]] == d[combo[1]] == d[combo[2]]:
            return True
    return False

def game()->str:
    """
    Here lives the main game loop
    """
    turns = 0
    dboard = {x:str(x) for x in range(9)}
    combo_list = [
        [0,1,2], [3,4,5], [6,7,8], # rows
        [0,3,6], [1,4,7], [2,5,8], # columns
        [0,4,8], [2,4,6]           # diagonals
    ]
    x_player = 'X'
    o_player = 'O'
    current_player = x_player
    winner = False
    w_player = ''
    while turns < 9 and not winner:
        board.display_board(dboard)
        valid_move = False
        while not valid_move:
            valid_move = board.player_turn(current_player, dboard)
        turns += 1
        winner = check_winner(dboard, combo_list)
        if winner:
            w_player = current_player
            print(f"Player {current_player} wins!")
            break
        if current_player == x_player:
            current_player = o_player
        else:
            current_player = x_player
    board.display_board(dboard)
    return w_player
    #if winner:
    #    print(f"Winner: {current_player}")
    #else:
    #    print("its a draw")
    print("Game Over")
    
def two_players():
    playing = True
    score = {"X": 0, "O": 0, "draw": 0}
    while playing:
        winner = game()
        if len(winner) > 0:
            print(f"Player {winner} wins!")
            score[winner] += 1
        else:
            print("its a draw")   
            score["draw"] += 1
        play_again = input("Play again? (y/n): ")
        if play_again.lower() != "y":
            playing = False
            print("Final Score:")
            print(f"X: {score['X']}")
            print(f"O: {score['O']}")
            print(f"Draws: {score['draw']}")

if __name__ == "__main__":
    win = game()
    if len(win) > 0:
        print(f"Player {win} wins!")
    else:
        print("its a draw")