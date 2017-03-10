from google.appengine.api import urlfetch
import json
import urllib
import random

def state_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

root = 'http://accounts.google.com/o/oauth2/v2/auth?'
rt = 'response_type=code&'
ci = '471620941351-e2dgn52bn4omiujl5i224jcqt76bb9m6.apps.googleusercontent.com'
ru = ''
sl = 'scope=email&state='
state = state_generator() 
url = root + rt + ci + ru + s1 + state

class OauthHandler(webapp2.RequestHandler):
    def get(self):
	    code = self.request.get("code")
        state_b = self.request.get("state")
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        parameters = {
           'code': code,
           'client_id': '471620941351-e2dgn52bn4omiujl5i224jcqt76bb9m6.apps.googleusercontent.com',
           'client_secret': 'WNRdXX-6Q76jzYlOeA0ShuBG', 
           'redirect_uri': 'https://oath-158021.appspot.com/demo1',
           'grant_type': 'authorization_code'}
        payload = urllib.urlencode(parameters)
        request = urlfetch.fetch (
           url = 'https://www.googleapis.com/oauth2/v4/token',
           payload = urllib.urlencode(parameters),
           method = urlfetch.POST,
           headers = headers)
        access_t = json.loads(request.content)
        access_t = access_t["access_token"]
        header = {'Authorization': 'Bearer {}'.format(access_t)}
        resp_r = urlfetch.fetch(
            url = 'https://www.googleapis.com/plus/v1/people/me',
            headers = header
        data = resp_r.content
        data = json.loads(data)
        names = data["name"] 
        url = data["url"]
        givenName = str(names[u'givenName'])
        familyName = str(names[u'familyName'])
        self.response.write("Given Name: " + givenName)
        self.response.write('<br />')
        self.response.write("Family Name: " + familyName)
        self.response.write('<br />')
        self.response.write("Google Plus Url: "+  url)
        self.response.write('<br />')
        self.response.write("State Send: " + state)
        self.response.write('<br />')
        self.response.write("State Back: " + state_b)
