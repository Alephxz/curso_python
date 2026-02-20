import random
from Team import Team
from Game import Game

class Group:
    """ Group class represents a group of teams. """
    def __init__(self, name):
        """ Custom constructor for Group class. """
        self.name = name
        self.teams = []
    def add_team(self, team):
        """ Add a team to the group. """
        for i in range(len(team)):
            for j in range(i + 1, len(self.teams)):
                game = Game(self.teams[i], self.teams[j])
                self.add_game(game)
    def add_game(self, game):
        """ Add a game to the group. """
       
    def __str__(self):
        """ String representation of the Group class. """
        return f"Group: {self.name}, Teams: {len(self.teams)}"
    def __repr__(self):
        """ String representation of the Group class. """
        return f"Group(name={self.name}, teams={repr(self.teams)})"
    def to_json(self):
        """ Convert the Group object to a JSON string. """
        return {
            "name": self.name,
            "teams": [team.to_json() for team in self.teams]
        }