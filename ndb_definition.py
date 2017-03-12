from google.appengine.ext import ndb


class Users(ndb.Model):
    google_id = ndb.StringProperty()
    steam_id = ndb.IntegerProperty()
    active_state = ndb.BooleanProperty() 
    owned_game = ndb.StringProperty(repeated=True)


class Games(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    game_id = ndb.IntegerProperty()
    game_name = ndb.StringProperty()
    recent_played = ndb.BooleanProperty()
    play_time = ndb.IntegerProperty()        
