import logging
from pymongo import MongoClient
from bson.objectid import ObjectId
from googleapiclient import discovery
from oauth2client.contrib.appengine import OAuth2Decorator
from oauth2client.client import AccessTokenRefreshError
from bson import Binary
import os
import webapp2
import jinja2

GOOGLE_LOGIN_CLIENT_ID = '4826155823-o675k2ap3eq4trhlahaa565fv80l92ab.apps.googleusercontent.com'
GOOGLE_LOGIN_CLIENT_SECRET = 'npLKFVPp_pHfm1cRL9l68go0'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
extensions=['jinja2.ext.autoescape'])

decorator = OAuth2Decorator(
    client_id=GOOGLE_LOGIN_CLIENT_ID,
    client_secret=GOOGLE_LOGIN_CLIENT_SECRET,
    scope='https://www.googleapis.com/auth/gmail.readonly')

client = MongoClient()
mongo = client.db

def get_logged_user_email():
    service = discovery.build('gmail', 'v1', http=decorator.http())
    print service
    results = service.users().getProfile(userId='me').execute()
    return results.get('emailAddress')

class ListTasks(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        alltasks = mongo.tasks.find()
        variables = {
            'logged_user': get_logged_user_email(),
            'alltasks': alltasks,
        }
        template = JINJA_ENVIRONMENT.get_template('templates/alltasks.html')
        self.response.write(template.render(variables))

class CreateTask(webapp2.RequestHandler):
    def post(self):
        task_title = self.request.get('task_title')
        task_description = self.request.get('task_description')
        task_priority = self.request.get('task_priority')
        task_author = self.request.get('author')
        mongo.tasks.insert_one({'title': task_title, 
                                'description': task_description, 
                                'priority': task_priority,
                                'status': 0,
                                'author': task_author})
        self.redirect('/alltasks')

class DeleteTask(webapp2.RequestHandler):
    def get(self, task_id):
        mongo.tasks.delete_one({'_id': ObjectId(task_id)})
        self.redirect('/alltasks')


class UpdateTask(webapp2.RequestHandler):
    def get(self, task_id, task_title):
        mongo.tasks.update({'_id': ObjectId(task_id)}, {'$set': {'title': task_title}})
        self.response.write({'new_id': task_id})


class AddAttachment(webapp2.RequestHandler):
    def post(self, task_id):
        file = self.request.get('file')
        filename = self.request.params["file"].filename
        mongo.tasks.update({'_id': ObjectId(task_id)}, 
            {'$addToSet': { 
                'attachments': 
                {'filename': filename, 
                'data': Binary(file)}}})
        self.redirect('/alltasks')
        
class UpdateStatus(webapp2.RequestHandler):
    def get(self, task_id, new_status):
        mongo.tasks.update({'_id': ObjectId(task_id)}, {'$set': {'status': int(new_status)}})
        self.redirect('/alltasks')


app = webapp2.WSGIApplication([
    (decorator.callback_path, decorator.callback_handler()),
    ('/alltasks', ListTasks),
    ('/new_task', CreateTask),
    webapp2.Route('/delete/<task_id>', handler=DeleteTask),
    webapp2.Route('/update/<task_id>/<task_title>', handler=UpdateTask),
    webapp2.Route('/attachment/<task_id>', handler=AddAttachment),
    webapp2.Route('/updatestatus/<task_id>/<new_status>', handler=UpdateStatus),
], debug=False)