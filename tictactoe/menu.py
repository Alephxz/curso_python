from app import game

def display_menu():
    print("welcome to tic tac toe")
    print("1. one player")
    print("2. two players")
    print("3. exit")
    choice = input("enter your choice: ")
    return choice

def get_choice():
    choice = display_menu()
    while choice not in ["1", "2", "3"]:
        choice = display_menu()
    return choice


if __name__ == "__main__":
  get_choice()
    
 
