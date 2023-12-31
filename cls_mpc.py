import os, glob

class Playlist:
	def reinit(self):
		pls = os.popen("mpc playlist").read()
		self.playlist = pls.splitlines()
		self.playlist_length = len(self.playlist)

	def __init__(self):
		self.reinit()
		self.playlists = glob.glob("*.m3u")
		self.playlists_length = len(self.playlists)
		


