from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from ndb_definition import *
import json
import webapp2
import urllib
import time


def get_steam_info (steam_id):
    player_summary = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='
    steam_key = 'E605A7E4E5549D4B289D5CA74D952E93'
    url_para = '&steamids=' + str(steam_id)
    url = player_summary + steam_key + url_para
    resp_r = json.loads(urlfetch.fetch(url).content)
    data = resp_r['response']['players']
    data = data[0]
    player = {}
    current_time = int(time.time())
    if (current_time - data['lastlogoff'] < 604800):
        player['active'] = True
    else:
        player['active'] = False
    owned_games = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
    appinfo = '&include_appinfo=1'
    format = '&format=json'
    url = owned_games + steam_key + '&steamid=' + str(steam_id) + appinfo + format
    resp_r = json.loads(urlfetch.fetch(url).content)
    data = resp_r['response']
    player['game_count'] = data['game_count']
    player['game'] = []
    for item in data['games']:
        game_info = []
        game_info.append(item['appid'])
        game_info.append(item['name'])
        if 'playtime_2weeks' in item.keys():
            game_info.append(item['playtime_2weeks'])
        else:
            game_info.append(0)
        game_info.append(item['playtime_forever'])
        player['game'].append(game_info)
    return player
         

def decode_token(access_token):
     header = {'Authorization': 'Bearer {}'.format(access_token)}
     resp_r = urlfetch.fetch(
         url = 'https://www.googleapis.com/plus/v1/people/me',
         headers = header
     )
     data = resp_r.content
     data = json.loads(data)
     return data
	 
def add_new_game(game_data, user):
    if game_data[2] == 0:
        rp = False
    else:
        rp = True
    new_game = Games (
        user_id = user,
        game_id = game_data[0],
        game_name = game_data[1],
        recent_played = rp,
        play_time = game_data[3]		
    )
    new_game.put()
    game_index = new_game.key.id()
    return ('/Game/'+str(game_index)) 	

class StartPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello, this is my steam tracker")
	
    def delete(self):
        ndb.delete_multi(Users.query().fetch(keys_only=True))
        ndb.delete_multi(Games.query().fetch(keys_only=True))
		
		
class UserHandler(webapp2.RequestHandler):
    def get(self):
        access_token = self.request.get('access_token') 
        if access_token:
            try:
                user_data = decode_token(access_token)
                user_id = user_data['id']
                query_user = Users.query(Users.google_id == user_id)
                user_data = query_user.fetch()
                if len(user_data)!=0:
                    for item in user_data:
                        single_user = item.to_dict()
                        self.response.write(json.dumps(single_user))
                else:
                    self.response.write('No user found')
            except:
                self.response.write('Invalid access token')   	
        else:
            self.response.write('Permission Deined')
	
    def post(self):
        user_Info = json.loads(self.request.body)
        try:
            user_data = decode_token(user_Info['access_token'])
            user_id = user_data['id']
            steam_info = get_steam_info(user_Info['steam_id'])
            game_owned = []
            for item in steam_info['game']:
                game_owned.append(add_new_game(item, user_id))
            if len(Users.query(Users.google_id == user_id).fetch()):
                self.response.write('Already Exist')
            else:				
                new_user = Users (
                    google_id = user_id,
                    steam_id = user_Info['steam_id'],
                    active_state = steam_info['active'],
                    owned_game = game_owned			
                )
                new_user.put()
                self.response.write(json.dumps(new_user.to_dict()))
        except:
            self.response.write('Invalid access token')
		
    def delete(self):
        access_token = self.request.get('access_token')
        if access_token:
            try:
                user_data = decode_token(access_token)
                user_id = user_data['id']
                query_user = Users.query(Users.google_id == user_id)
                user_data = query_user.fetch(keys_only=True)
                if len(user_data) !=0:
                    ndb.delete_multi(user_data)
                    ndb.delete_multi(Games.query(Games.user_id == user_id).fetch(keys_only=True))
                    self.response.write('User with id ' + str(user_id) + 'has been deleted')
                else:
                    self.response.write('No user found')
            except:
                self.response.write('Invalid access token')
        else:
            self.response.write('Permission Deined')

    def patch(self): 
        patch_info = json.loads(self.request.body)        		
        try:
            user_data = decode_token(patch_info['access_token'])
            user_id = user_data['id']
            try:                   
                quired_item = Users.query(Users.google_id == user_id).fetch()
                patched_key = None
                for item in quired_item:
                    patched_key = item.key
                patched_user = patched_key.get()
                if 'steam_id' in patch_info:
                    ndb.delete_multi(Games.query(Games.user_id == user_id).fetch(keys_only=True))
                    patched_user.steam_id = patch_info['steam_id']                     
                    steam_info = get_steam_info(patch_info['steam_id'])
                    game_owned = []
                    for item in steam_info['game']:
                        game_owned.append(add_new_game(item, user_id))
                    patched_user.owned_game = game_owned
                    patched_user.active_state = steam_info['active']
                if 'active_state' in patch_info:
                    patched_user.active_state = patch_info['active_state']
                patched_user.put()
                response_data = patched_user.to_dict()
                self.response.write(json.dumps(response_data))
            except:
                self.response.write(patch_info['access_token'])
        except:
            self.response.write('Invalid acces token')		

    def put(self):
        put_info = json.loads(self.request.body)
        try:
            replaced_key = ndb.Key(Users, put_info['id'])
            replaced_user = replaced_key.get()
            check = replaced_user.key.id()
            try:
                user_data = decode_token(put_info['access_token'])
                user_id = user_data['id'] 
                if len(Users.query(Users.google_id == user_id).fetch()):
                    self.response.write('Already exist')
                else:
                   replaced_user.google_id = user_id
                   replaced_user.steam_id = put_info['steam_id']
                   steam_info = get_steam_info(put_info['steam_id'])
                   replaced_user.active_state = steam_info['active']
                   game_owned = []
                   for item in steam_info['game']:
                       game_owned.append(add_new_game(item, user_id))
                   replaced_user.owned_game = game_owned
                   replaced_user.put()
                   self.response.write(json.dumps(replaced_user.to_dict()))
            except:
                self.response.write('Invalid access token')
        except:
            self.response.write('Invalid ID')
	
class GameHandler(webapp2.RequestHandler):
    def get(self, **args):
        if 'game_id' in args:
            queried_game = ndb.Key(Games, int(args['game_id']))      
            game = queried_game.get()
            return_data = game.to_dict()
            self.response.write(json.dumps(return_data))
        else:
            access_token = self.request.get('access_token')
            user_id = decode_token(access_token)['id']             
            quired_game = Games.query(Games.user_id == user_id)
            game_data = quired_game.fetch()
            return_data = []
            for item in game_data:
                single_game = item.to_dict()
                return_data.append(single_game)
            self.response.write(json.dumps(return_data)) 

 
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', StartPage),
    ('/User',UserHandler),
    ('/addUser', UserHandler),
    ('/deleteUser', UserHandler),
    ('/Game',GameHandler)
], debug=True)	
app.router.add(webapp2.Route('/Game/<game_id:\d+>', handler=GameHandler))
	
