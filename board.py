import tkinter as tk
from   PIL import Image, ImageTk
from   game_stats import Game_Stats
import sys

class Board(tk.Frame):

	def __init__(self, parent, Game):

		self.game   = Game
		self.config = Game.config # config yang ada di class Battleship ( bukan window )
		self.row    = self.config.row
		self.column = self.config.column

		self.stats  = Game_Stats()

		# CONFIG FRAME
		super().__init__(parent) # parent -=> container
		self.configure(bg = "gray")
		self.grid(row = 0, column = 0, sticky = "snew")

		parent.grid_rowconfigure   (0, weight = 1)
		parent.grid_columnconfigure(0, weight = 1)

		self.create_main_frame()
		self.update_board()

		self.tracking_score = tk.Label(self, text = f"Score : {self.stats.score}", font = ("Arial", 20, 'bold'), bg = "gray", fg = 'white', padx = 10)
		self.tracking_score.pack(side = 'left')

		self.label_attempt = tk.Label(self, text= '15 attempt(s) left', font=('Arial', 20, 'bold'), bg='gray', fg = 'white', padx=10)
		self.label_attempt.pack(side='right')




	def update_board(self):
		self.create_board()
		self.show_board()
		self.create_button_board()
		self.show_button_board()

	def create_main_frame(self):
		self.main_frame = tk.Frame(self, height = self.config.side, width = self.config.side, bg = 'black')
		self.main_frame.pack(expand = True)


	def create_board(self):
		self.frame_rows = [] #[0,1,2,3,4]
		colors          = ['yellow', 'green', 'cyan', 'orange', 'gray']

		nRow     , nColumn   = self.config.row        , self.config.column
		rowHeight, rowWidth = self.config.side // nRow, self.config.side

		for i in range(nRow):
			frame = tk.Frame(self.main_frame, height = rowHeight, width = rowWidth, bg = colors[i])
			self.frame_rows.append(frame)

	def show_board(self):
		for frame in self.frame_rows:
			frame.pack()

	def put_and_resize_photo(self, ori_img, scale):
		n_column     = self.config.column
		button_width = self.config.side // n_column - 10

		image = Image.open(ori_img)
		image_w, image_h = image.size
		ratio = image_w // button_width
		new_size = (int(image_w // ratio//scale), int(image_h // ratio//scale))
		image = image.resize(new_size)
		return ImageTk.PhotoImage(image)

	def create_button_board(self):
		self.button_board = []

		nRow         , nColumn      = self.config.row              , self.config.column
		button_height, button_width = self.config.side // nRow - 10, self.config.side // nColumn - 10 

		self.init_img_btn   = self.put_and_resize_photo(self.config.init_img  , 1)
		self.final_img_btn  = self.put_and_resize_photo(self.config.final_img , 1)
		self.win_img_btn    = self.put_and_resize_photo(self.config.win_img   , 1)

		for i in range(nRow):
			row = []
			for j in range(nColumn):
				button = tk.Button(self.frame_rows[i], bg = "white", image = self.init_img_btn, height = button_height, width = button_width, text = "O", font = ("Arial", 36, "bold"), command = lambda x=i, y=j:[self.game.is_button_board_clicked(x,y)])
				row.append(button)
			self.button_board.append(row)

	def show_button_board(self):
		nRow, nColumn = self.config.row, self.config.column
		for i in range(nRow):
			for j in range(nColumn):
				self.button_board[i][j].pack(side = 'left')
