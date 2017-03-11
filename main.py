from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from ndb_definition import *
import json
import webapp2
import urllib



def get_steam_info (steam_id):
    player_summary = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='
    steam_key = 'E605A7E4E5549D4B289D5CA74D952E93'
    url_para = '&steamids=' + str(steam_id)
    url = player_summary + steam_key + url_para
    resp_r = urlfetch.fetch(url)
    data = resp_r['response']
    data = data['players'][0]
	player = []
	for player in players:
        	    
	
    
	
def decode_token(access_token):
     header = {'Authorization': 'Bearer {}'.format(access_token)}
     resp_r = urlfetch.fetch(
         url = 'https://www.googleapis.com/plus/v1/people/me',
         headers = header
     )
     data = resp_r.content
     data = json.loads(data)
     return data

class StartPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello, this is my steam tracker")
	
    def delete(self):
        ndb.delete_multi(Users.query().fetch(keys_only=True))
        ndb.delete_multi(Games.query().fetch(keys_only=True))
		
		
class UserHandler(webapp2.RequestHandler):
    def get(self):
        if 'access_token' in args:
            user_data = decode_token(args['access_token'])
            user_id = user_data['id']
            query_user = Users.query(Books.google_id == user_id)
            user_data = query_user.fetch()
            for item in user_data:
                single_user = item.to_dict()
                self.response.write(json.dumps(back_data))	
        else:
            user_list = Users.query().fetch()
            user_data = []
            for item in user_lisat:
                single_user = item.to_dict()
                user_data.append(single_user)
            self.response.write(json.dumps(back_data))
	
    def post(self):
        user_Info = json.loads(self.request.body)
        user_data = decode_token(user_Info['access_token'])
        user_id = user_data['id']
        steam_info = steam_info(user_Info['steam_id'])
        new_user = Users (
            google_id = user_id,
            steam_id = steam,
            active_state = active,
            owned_game = game			
        )
        new_user.put()
        self.response.write(json.dumps(new_user.to_dict()))

	
class GameHandler(webapp2.RequestHandler):
    def get(self):
        system.response.write("waiting")

	
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', StartPage),
    ('/newUser',UserHandler)
], debug=True)		
