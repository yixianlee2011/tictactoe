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

@bottle.route('/currentplayer')
def currentplayer():
  d = {"name":str(users.get_current_user())}
  return json.dumps(d)

def verify(problem, tests, url):
  d = {"tests":">>> b \n 2", "solution":"b=3"}
  requestJSON = json.dumps(d)
  result = verify_service(requestJSON,url)
  return result

@bottle.route('/use_verify_service')
def use_verify_service():
  url = "http://ec2-54-251-204-6.ap-southeast-1.compute.amazonaws.com/python"
  problem = request.params.get('problem')
  tests = request.params.get('tests')
  result = verify(problem, tests, url)
  return result 

@bottle.route('/')
def home():
  """ Return Hello World at application root URL"""
  continue_url = request.params.get('continue')
  #redirect(users.create_login_url(continue_url))
  result = "Hello"+"<br>"
  result += str(continue_url)+"<br>"
  result += str(users.get_current_user())+"<br>"
  result += "<a href='"+users.create_login_url('/')+"'>login</a><br>"
  result += "<a href='"+users.create_logout_url('/')+"'>logout</a><br>"
  result += "<a href='/currentplayer'>currentplayer api</a><br>"
  result += "<a href='/use_verify_service'>use_verify_service api</a><br>"
  result += "Enter your bot code:<br> <textarea></textarea><br>"
  result += "Enter your tests:<br> <textarea></textarea><br>"
  result += "<input type=submit value='Verify code with service'><br>"
  result += "Results returned from verfier service:<br> <pre>{}</pre>"
  return result


@bottle.error(404)
def error_404(error):
  """Return a custom 404 error."""
  return 'Sorry, Nothing at this URL.'


