from google.appengine.ext import ndb


class Users(ndb.Model):
    google_name = ndb.StringProperty()
    google_id = ndb.StringProperty()
    steam_id = ndb.IntegerProperty()
    active_state = ndb.BoolProperty() 
    owned_game = ndb,StringProperty(repeated=True)


class Games(ndb.Model):
    game_id = ndb.IntegerProperty()
    game_name = ndb.StringProperty()
    recent_played = ndb.BoolProperty()
    play_time = ndb.IntegerProperty()        
