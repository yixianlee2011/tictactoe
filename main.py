"""`main` is the top level module for your Bottle application.

Loads the Bottle framework and adds a custom error
handler.
"""

# import the Bottle framework
from bottle import Bottle
from google.appengine.api import users
from bottle import route, request, run, redirect
import json
import urllib
from google.appengine.api import urlfetch

def verify_service(requestJSON, url):
      params = urllib.urlencode({'jsonrequest': requestJSON})

      deadline = 10
    
      result = urlfetch.fetch(url=url,
                                payload=params,
                                method=urlfetch.POST,
                                deadline=deadline,
                                headers={'Content-Type': 'application/x-www-form-urlencoded'})
      return result.content


# Run the Bottle wsgi application. We don't need to call run() since our
# application is embedded within an App Engine WSGI application server.
bottle = Bottle()

@bottle.route('/api/currentplayer')
def currentplayer():
  d = {"name":str(users.get_current_user())}
  return json.dumps(d)

def verify(problem, tests, url):
  d = {"tests":tests, "solution":problem}
  requestJSON = json.dumps(d)
  result = verify_service(requestJSON,url)
  return result

@bottle.route('/api/use_verify_service')
def use_verify_service():
  url = "http://ec2-54-251-204-6.ap-southeast-1.compute.amazonaws.com/python"
  problem = request.params.get('problem')
  tests = request.params.get('tests')
  result = verify(problem, tests, url)
  return result 

@bottle.error(404)
def error_404(error):
  """Return a custom 404 error."""
  return 'Sorry, Nothing at this URL.'


