from google.appengine.ext import ndb
from ndb_definition import *
from authorize import *
import json
import webapp2

class StartPage(webapp2.RequestHandler):
    def get(self):
	    self.redirect(authorize.url)

		
class UserHandler(webapp2.RequestHandler):
    def get(self):

	
class GameHandler(webapp2.RequestHandler);
    def get(self):

	
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', StartPage),
	('/ot', authorize.OAuthHanlder) 
], debug=True)		