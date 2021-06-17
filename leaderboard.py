import tkinter as tk
import tkinter.ttk
from game_stats import Game_Stats

class Leaderboard(tk.Frame):

	def __init__(self, parent, Game):

		self.game   = Game
		self.config = Game.config # config yang ada di class Battleship ( bukan window )
		self.row    = self.config.row
		self.column = self.config.column

		self.stats  = Game_Stats()
		self.stats.load_data()

		self.stats.score_.sort(reverse = True)

		# CONFIG FRAME
		super().__init__(parent) # parent -=> container
		self.grid(row = 0, column = 0, sticky = "snew")

		parent.grid_rowconfigure   (0, weight = 1)
		parent.grid_columnconfigure(0, weight = 1)

		self.create_main_frame()

		self.btn_back = tk.Button(self, text='Back',width=71, height=2, bg='gray50', fg='black', command=self.game.change_to_play)
		self.btn_back.grid(row=1, column=1)


	def create_main_frame(self):

		self.main_frame = tk.Frame(self, bg="white", width = self.config.side, height = self.config.side + 10)
		self.main_frame.grid(row=0, column=1, sticky="nsew")

		self.create_header()
		self.create_leaderboard()

	def create_header(self):

		self.header = tk.Frame(self.main_frame, width=self.config.side, height=self.config.side // 6, bg="magenta")
		self.header.pack()

		self.detail_header = tk.Frame(self.header, width=self.config.side, height=self.config.side // 6, bg="magenta")
		self.detail_header.grid(row=0, column=0, sticky="nsew")

		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.label = tk.Label(self.detail_header, text="Top Highest Score", font=("Arial", 18), width=self.config.side, height=self.config.side // 6, image=self.virt_img, compound="c", bg="gray")
		self.label.pack()

		tkinter.ttk.Separator(self.detail_header, orient = "horizontal").pack()

		self.header.grid_columnconfigure(0, weight=1)
		self.header.grid_rowconfigure(0, weight=1)

	def create_leaderboard(self):
		self.content = tk.Frame(self.main_frame, width=self.config.side, height=self.config.side // 6 * 5, bg="gray")
		self.content.pack(expand=True)

		self.detail_content = tk.Frame(self.content, width=self.config.side, height=self.config.side // 6 * 5, bg="white")
		self.detail_content.grid(row=0, column=0, sticky="nsew")

		self.content.grid_columnconfigure(0, weight=1)
		self.content.grid_rowconfigure(0, weight=1)

		for info in self.stats.score_:
			player_info = info

		#print(self.stats.score_)

		number = 0

		while number < 10:
			
			number += 1

			number_label = tk.Label(self.detail_content, text = number , font = ("Arial", 20, "bold"), bg = 'white')
			number_label.grid(row = number -1, sticky = 'w')

		for i in range(10):

			tkinter.ttk.Separator(self.detail_content, orient = "vertical").grid(column = 1, row = 0, rowspan = 10, sticky = "ns")

			self.name1 = tk.Label(self.detail_content, text = f'  {self.stats.score_[i][1]}  ', font = ("Arial", 20, "bold"), bg = 'white')
			self.name1.grid(row = i, column = 2)

			tkinter.ttk.Separator(self.detail_content, orient = "vertical").grid(column = 3, row = 0, rowspan = 10, sticky = "ns")

			self.score1 = tk.Label(self.detail_content, text = f'  {self.stats.score_[i][0][0]}  ', font = ("Arial", 20, "bold"), bg = 'white')
			self.score1.grid(row = i, column = 4)

			tkinter.ttk.Separator(self.detail_content, orient = "vertical").grid(column = 5, row = 0, rowspan = 10, sticky = "ns")

			self.time1 = tk.Label(self.detail_content, text = f"  {self.stats.score_[i][0][1]} second(s)  ", font = ("Arial", 20, "bold"), bg = 'white')
			self.time1.grid(row = i, column = 6)
