"""
Docstring for game_tournament.Game
Game class represents a game in the tournament. It has a name, a sport, and a list of teams.
"""
import random
from Team import Team
from Sport import Sport
from Athlete import Athlete

class Game:
    """ Game class represents a game in the tournament. It has two teams and a score"""
    def __init__(self, A:Team, B:Team):
        """ Custom constructor for Game class. """
        self.set_team(A, "local")
        self.set_team(B,"visitor")
        self.score = {
            A.name: 0, B.name: 0
            }
    def set_team(self, team, role):
        """ Set a team for the game. """
        if isinstance(team, Team):
            if role == "local":
                self.team_a = team
            elif role == "visitor":
                self.team_b = team
            else:
                raise ValueError("Role must be 'local' or 'visitor'.")
        else:
            raise ValueError("Only Team objects can be set as a team.")
    def play(self):
        """ Simulate playing the game by randomly assigning scores to each team. """
        self.score[self.team_a.name] = random.randint(0, Sport.max_score[self.team_a.sport.name])
        self.score[self.team_b.name] = random.randint(0, Sport.max_score[self.team_b.sport.name])
    def __str__(self):
        """ String representation of the Game class. """
        return f"{self.team_a.name} vs {self.team_b.name} - Score: {self.score[self.team_a.name]}:{self.score[self.team_b.name]}"
    def __repr__(self):
        """ String representation of the Game class. """
        return f"Game(team_a={self.team_a}, team_b={self.team_b}, score={self.score})"
    def to_json(self):
        """ Convert the Game object to a JSON string. """
        return {
            "team_a": self.team_a.to_json(),
            "team_b": self.team_b.to_json(),
            "score": self.score
        }
   
def a_game():
    players_mex=["chicharito", "piojo", "guardado", "hector moreno", "rafa marquez", "salcido", "vela", "dos santos", "herrera", "layun", "corona"]
    players_arg=["messi", "di maria", "aguero", "higuain", "mascherano", "biglia", "dybala", "paredes", "tagliafico", "otamendi", "zabaleta"]
    sport = Sport("Futbol",11,"FIFA")
    team_mex = Team("Mexico",sport)
    team_arg = Team("Argentina",sport)
    for player in players_mex:
        team_mex.add_athlete(Athlete(player))
    for player in players_arg:
        team_arg.add_athlete(Athlete(player))
    game = Game(team_mex, team_arg)
    game_string = game.to_json()
    return game_string
def save_game_to_json(game_data, filename):
    """ Save the Game object to a JSON file. """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(game_data, f, indent=4)   
if __name__ == "__main__":
    string_game = a_game()
    save_game_to_json(string_game, "game.json")