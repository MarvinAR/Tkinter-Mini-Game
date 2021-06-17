import tkinter   as tk 
import sys
import time 	
import os
from   tkinter   import messagebox
import random

from   PIL         import Image, ImageTk
from   datetime    import datetime
import pygame

from   config      import Config
from   board       import Board
from   ship        import Ship
from   player      import Player
from   game_stats  import Game_Stats
from   leaderboard import Leaderboard

class Window(tk.Tk):

	def __init__(self, Game):
		self.game   = Game
		self.config = Game.config # ( langsung ke Battleship )

		super().__init__()
		self.title(self.config.title)
		self.geometry(self.config.screen)
		self.create_container()

		self.pages = {}
		self.create_htp()
		self.create_leaderboard()
		self.create_board()
		self.create_play()


	def create_container(self):
		self.container = tk.Frame(self, bg = "white")
		self.container.pack(fill = "both", expand = True)

	def create_board(self):
		self.pages["board"] = Board(self.container, self.game)

	def create_play(self):
		self.pages['Play'] = Play(self.container, self)

	def create_leaderboard(self):
		self.pages['lb'] = Leaderboard(self.container, self.game)

	def create_htp(self):
		self.pages['htp'] = HowToPlay(self.container, self)

	def change_to_play(self):
		self.pages['Play'].tkraise()

	def change_page(self):
		self.pages["board"].tkraise()
		
	def change_leader(self):
		self.pages['lb'].tkraise()

	def change_htp(self):
		self.pages['htp'].tkraise()



class Battleship:

	def __init__(self):
		self.config = Config()
		self.window = Window(self)

		self.ship   = Ship(self)
		self.player = Player()
		self.stats  = Game_Stats()

		self.win_lose = "You Win :)"
		self.stats.score_.sort(reverse = True)

		pygame.mixer.init()

	def is_button_board_clicked(self, pos_x, pos_y):
		#print(f"Location : ( {pos_x}, {pos_y} )")
		self.player.current_location(pos_x, pos_y)
		
		self.stats.step    += 1

		self.window.pages['board'].label_attempt['text'] = f"{15 - self.stats.step} attempt(s) left"
		
		if self.ship.location == self.player.location:
			self.window.pages['board'].button_board[pos_x][pos_y].configure(image = self.window.pages['board'].win_img_btn)
			print("WIN !!!")

			self.win_lose = "You Win :)"
			self.finish = datetime.now()

			#print((self.finish - self.window.pages['Play'].start).seconds)

			if len(self.window.pages['Play'].nameVar.get()) > 6:
				name = self.window.pages['Play'].nameVar.get()[0:5] + "..."
				temp_data = [[self.stats.score, (self.finish -self.window.pages['Play'].start).seconds], name]
				self.stats.players.append(name)
			else:
				name = self.window.pages['Play'].nameVar.get()
				temp_data = [[self.stats.score, (self.finish -self.window.pages['Play'].start).seconds], name]
				self.stats.players.append(name)
			self.stats.score_.append(temp_data)

			self.stats.saveData()

			winner_choise = messagebox.askyesno('YOU WIN !!!', f"Good Game !\n\nScore   : {self.stats.score} pts\nTime     : {(self.finish -self.window.pages['Play'].start).seconds} second(s)\nStep(s) : {self.stats.step}\n\n'Yes'      : New Game\n'No'      : Cancel")

			if winner_choise == True:
				python = sys.executable
				os.execl(python, python, *sys.argv)

			else:
				exit()

		else:
			self.window.pages['board'].button_board[pos_x][pos_y].configure(image = self.window.pages['board'].final_img_btn)
			self.window.pages['board'].button_board[pos_x][pos_y]["state"] = "disabled"
			self.stats.score -= 4
			#print(self.stats.score)
			#print(self.stats.step)

			name = self.window.pages['Play'].nameVar.get()

			current_score = f"Score : {self.stats.score}"

			self.window.pages['board'].tracking_score['text'] = current_score

			if self.stats.step == 15:
				print("You Lose")

				self.finish = datetime.now()

				if len(self.window.pages['Play'].nameVar.get()) > 6:
					name = self.window.pages['Play'].nameVar.get()[0:5] + "..."
					temp_data = [[self.stats.score, (self.finish -self.window.pages['Play'].start).seconds], name]
					self.stats.players.append(name)
				else:
					name = self.window.pages['Play'].nameVar.get()
					temp_data = [[self.stats.score, (self.finish -self.window.pages['Play'].start).seconds], name]
					self.stats.players.append(name)
				#print(temp_data)
				self.stats.score_.append(temp_data)

				self.stats.saveData()

				loser_choise = messagebox.askyesno('YOU LOSE !!!', f"NICE TRY !\n\nScore   : {self.stats.score} pts\nTime     : {(self.finish -self.window.pages['Play'].start).seconds} second(s)\nStep(s) : {self.stats.step}\n\n'Yes'      : New Game\n'No'      : Cancel")
				if loser_choise == True:
					python = sys.executable
					os.execl(python, python, *sys.argv)
				else:
					exit()

	def change_to_play(self):
		self.window.pages['Play'].tkraise()


	def run(self):
		pygame.mixer.music.load(self.config.music)
		pygame.mixer.music.play()
		self.window.mainloop()

class Play(tk.Frame):

	def __init__(self, parent,App):
		self.application = App
		self.settings    = App.config
		self.stats       = Game_Stats()

		super().__init__(parent)

		self.configure(bg = "grey")
		self.grid(row = 0, column= 0, sticky = 'nswe')

		parent.grid_columnconfigure(0, weight = 1)
		parent.grid_rowconfigure(0, weight = 1)

		self.main_frame = tk.Frame(self, height = self.settings.side, width = self.settings.side, bg = 'gray')
		self.main_frame.pack(expand = True)

		image = Image.open(self.settings.logo_path)
		image_w, image_h = image.size
		ratio = (image_w / self.settings.side)
		image = image.resize((int(image_w // ratio) // 2, int(image_h // ratio) // 2))

		self.logo  = ImageTk.PhotoImage(image)
		self.label_logo = tk.Label(self.main_frame, image = self.logo)
		self.label_logo.pack(pady = 5)

		self.label_username = tk.Label(self.main_frame, text = "Input your nickname", bg = 'gray', fg = "white", font = ("Arial", 18, "bold"))
		self.label_username.pack(pady = 5)

		self.nameVar = tk.StringVar()
		self.entry_username = tk.Entry(self.main_frame, font = ("Arial", 16, "bold"), textvariable = self.nameVar, justify = 'center')
		self.entry_username.pack(pady = 15)

		lists = ["Jono", "Ayam", "Luigi", "Marvel", "Aldo"]

		self.entry_username.insert(0, random.choices(lists))


		self.warning_label = tk.Label(self.main_frame, text = '*You can change the nickname, if you want', font = ("Trajan Pro", 8), bg = 'gray', fg = 'white')
		self.warning_label.pack()

		self.btn_login = tk.Button(self.main_frame, text='Enter', command=lambda:self.greeting())
		self.btn_login.pack(pady=5)

		self.btn_how_to_play = tk.Button(self.main_frame, text='How To Play',command=self.application.change_htp)
		self.btn_how_to_play.pack(pady=5)

		self.button_leaderboard = tk.Button(self.main_frame, text='Leaderboard',command=self.application.change_leader)
		self.button_leaderboard.pack(pady=5)


	def start_timer(self):
		self.start  = datetime.now()

	def greeting(self):

		if self.application.pages['Play'].nameVar.get() in self.stats.players:
			self.warning_label.config(text = "*Your nickname is already exist, please choose another*", fg = 'maroon', font = ("Arial", 10, 'bold'))

		else:
			if len(self.nameVar.get()) > 6:
				name = self.nameVar.get()[0:5] + "..."
				self.label_username.config(text="Hello" + " " + name + "," + " " + "Guess The Correct Button To Win", font = ("Arial", 15, "bold"))
			else:
				self.label_username.config(text="Hello" + " " + self.nameVar.get()+ "," + " " + "Guess The Correct Button To Win", font = ("Arial", 15, "bold"))
			self.entry_username.destroy()
			self.button_leaderboard.destroy()
			self.warning_label.destroy()
			self.btn_how_to_play.destroy()
			self.btn_login.config(text="Play Now", command=lambda:[self.application.change_page(), self.start_timer()])

class HowToPlay(tk.Frame):

	def __init__(self, parent,App):
		self.application = App
		self.settings    = App.config
		self.stats       = Game_Stats()

		super().__init__(parent)

		self.configure(bg = "grey")
		self.grid(row = 0, column= 0, sticky = 'nswe')

		parent.grid_columnconfigure(0, weight = 1)
		parent.grid_rowconfigure(0, weight = 1)

		self.main_frame = tk.Frame(self, height = self.settings.side, width = self.settings.side, bg = 'gray')
		self.main_frame.pack(expand = True)

		self.how_to_play()


	def how_to_play(self):

		self.text = """
RULES :
[1] There are 25 boxes, Only one box is true and the other is false.
[2] Find the correct box to win this game
[3] If you clicked on incorrect box, your score will -4.
[4] Remember, you just have 15 attempts to guess where the correct box is.
[5] If you already understand, please click exit button below or play game.
[6] I dare you
"""
		htp_txt = tk.Label(self.main_frame, text=self.text, font=('Trajan Pro', 8), bg='gray', fg='white')
		htp_txt.pack()

		self.back = tk.Button(self.main_frame, text='BACK', command=self.application.change_to_play)
		self.back.pack(pady=5)


if __name__ == "__main__":
	my_battleship = Battleship()
	my_battleship.run()