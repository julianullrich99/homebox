import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

scope = 'user-modify-playback-state,user-read-currently-playing,user-read-playback-state'

SPOTIPY_CLIENT_ID="49e4b4ca65ea409bb48295c0a2f3f5e7"
SPOTIPY_CLIENT_SECRET="ee5dc6e0676d42099c6e65ae9d4b276e"
SPOTIPY_REDIRECT_URI="http://localhost/"

token = util.prompt_for_user_token('j.ullrich',scope,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)

print SPOTIPY_CLIENT_ID

# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# print sp.pause_playback()

# if sp:
sp = spotipy.client.Spotify(auth=token)
# print dir(sp)

print sp.current_playback()

# prefix = "track"
# results = sp.search(q="reckless love", type=prefix)
# items = results[prefix + "s"]['items']
# if len(items) > 0:
#     play = items[0]
#     # print (play)
#     # uri = play["context_uri"]
#     sp.start_playback(context_uri="spotify:track:0BnRoiQbiSYb4K4y3aQWbg")


    # results = sp.current_user_saved_tracks()
    # for item in results['items']:
    #     track = item['track']
    #     print track['name'] + ' - ' + track['artists'][0]['name']
# else:
#     print "Can't get token for", username
