from json import load, dump

class Game_Stats:

	def __init__(self):

		#SCOREBOARD

		self.score  = 100
		self.step   = 0

		self.score_ = self.load_data()
		self.players = self.load_players()

	def load_data(self):
		with open("score.json") as f:
			self.score_ = load(f)

		return self.score_

	def load_players(self):

		with open("players.json") as f:
			self.players = load(f)

		return self.players

	def saveData(self):

		with open ("score.json","w") as f:
			dump(self.score_,f)

		with open ("players.json","w") as f:
			dump(self.players,f)

		return self.score_, self.players
