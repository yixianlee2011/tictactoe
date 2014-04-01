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
from google.appengine.ext import ndb

class Bot(ndb.Model):
  name = ndb.StringProperty()
  language = ndb.StringProperty()
  code = ndb.StringProperty()

class GameResult(ndb.Model):
  bot1 =  ndb.KeyProperty(kind=Bot)
  bot2 =  ndb.KeyProperty(kind=Bot)
  created = ndb.DateTimeProperty(auto_now_add=True)
  result = ndb.IntegerProperty()
  
def add_result(bot1,bot2,result):
  gr = GameResult(bot1=bot1, bot2=bot2, result=result)
  gr.put()

def list_results():
  results = []
  score = {}
  for gr in GameResult.all():
    results.append({"bot1":gr.bot1.name, "bot2":gr.bot2.name,"result":gr.result})
    if score.has_key(gr.bot1.key().id()):
      score[gr.bot1.key().id()] += gr.result
    else:
      score[gr.bot1.key().id()] = gr.result
      
    if score.has_key(gr.bot2.key().id()):
      score[gr.bot2.key().id()] -=gr.result
    else:
      score[gr.bot2.key().id()] = -gr.result
    
    return (results, score)

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

@bottle.route('/api/post_bot')
def use_verify_service():
  name = request.params.get('name')
  language = request.params.get('language')
  code = request.params.get('code')
  new_bot = Bot(name = name,
                language = language,
                code = code)
  new_bot.put()
  # result = json.dumps({"name":name,"language":langauge,"code":code})
  return 'true'

@bottle.route('/api/use_verify_service')
def use_verify_service():
  url = "http://ec2-54-251-204-6.ap-southeast-1.compute.amazonaws.com/python"
  problem = request.params.get('problem')
  tests = request.params.get('tests')
  result = verify(problem, tests, url)
  return result 

@bottle.route('/api/get_bots')
def use_verify_service():
  bots = Bot.query().fetch(100)
  result = []
  for bot in bots:
    result.append(bot.to_dict())
  return json.dumps(result) 

@bottle.error(404)
def error_404(error):
  """Return a custom 404 error."""
  return 'Sorry, Nothing at this URL.'