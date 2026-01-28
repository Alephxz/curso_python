"""
Tic-Tac-Toe Game
author: Alexander Morales Quiroz
version: 1.0
"""
from game_logic import game

def main():
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
    main()
