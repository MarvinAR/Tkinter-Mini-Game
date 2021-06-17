
class Config:

	def __init__(self):

		#GAME CONFIG

		self.title  = "Battleship War"
		self.row    = 5
		self.column = 5

		#WINDOW CONFIG

		base        = 100
		ratio       = 5
		self.side   = base * ratio
		self.screen = f"{self.side}x{self.side+10}+500+500"

		# IMG PATH

		self.init_img  = "img/click-me.jpeg"
		self.final_img = "img/nope.jfif"
		self.win_img   = "img/win.jfif"

		self.logo_path = "img/logo.jfif"

		# AUDIO PATH

		self.music     = "sfx/music.mp3"