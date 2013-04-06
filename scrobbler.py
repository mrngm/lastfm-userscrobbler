import api as LastFM
import sys
import signal
import time
import datetime

to_scrobble = True # or not to scrobble
sleeptime = 10

def sighandle(sig, frame):
	print "" # adds a line
	print "Closing down, scrobble you next time!"
	sys.exit(0)

if len(sys.argv) < 2:
	print """Usage: scrobbler.py [username]

username	Name of the Last.fm user to copy scrobbled tracks from

When username is omitted, this help is displayed.
"""
else:
	if isinstance(LastFM.network, LastFM.pylast.LastFMNetwork):
		print "Following " + sys.argv[1] + ", press Ctrl+C to stop."
		signal.signal(signal.SIGINT, sighandle)
		user = LastFM.network.get_user(sys.argv[1])
		lastKnownTrack = None
		if isinstance(user, LastFM.pylast.User):
			t = user.get_now_playing()
			lastKnownTrack = t
			d = datetime.datetime.utcnow()
			timestamp = time.mktime(d.timetuple())
			firstMsg = True
			while True:
				if isinstance(t, LastFM.pylast.Track):
					if to_scrobble == True:
						LastFM.network.update_now_playing(t.get_artist(), t.get_title(True))
					if firstMsg == True:
						print str(d) + " /",
						print "Now playing: " + str(t)
						firstMsg = False
					t = user.get_now_playing()
					if isinstance(t, LastFM.pylast.Track):
						if t == lastKnownTrack:
							time.sleep(sleeptime)
						else:
							if to_scrobble == True:
								LastFM.network.scrobble(lastKnownTrack.get_artist(), lastKnownTrack.get_title(True), int(timestamp))
								print str(datetime.datetime.utcnow()) + " /",
								print "Scrobbled: " + str(lastKnownTrack) + " from " + str(d)
							d = datetime.datetime.utcnow()
							timestamp = time.mktime(d.timetuple())
							lastKnownTrack = t
							firstMsg = True
					else:
						firstMsg = True
				else:
					if firstMsg == False:
						time.sleep(sleeptime)
					else:
						print "Not playing anything at the moment"
						firstMsg = False
		# Catch Ctrl-C
		signal.pause()
