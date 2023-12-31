import os

class Playlist:
	def reinit(self):
		pls = os.popen("mpc playlist").read()
		self.playlist = pls.splitlines
		self.playlist_length = len(self.playlist)

	def __init__(self):
		self.reinit()
		


