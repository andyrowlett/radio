import os, glob

class Playlist:
	def reinit(self):
		pls = os.popen("mpc playlist").read()
		self.playlist = pls.splitlines()
		self.playlist_length = len(self.playlist)

	def __init__(self):
		os.chdir("/home/station/radio/")
		self.reinit()
		self.playlists = glob.glob("*.m3u")
		self.playlists_length = len(self.playlists)

	def get_track(self, number):
		name = self.playlist[number - 1]	
		if '-' in name:
			name = name.split("-")[1]	
		return name
	
	def get_playlist(self, number):
		name = self.playlists[number - 1]	
		return name.split(".")[0]

