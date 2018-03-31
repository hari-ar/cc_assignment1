import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Add(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        login_logout = ''
        main_header = ''
        login_logout_url = ''
        user = users.get_current_user()

        if user:
            main_header = 'GPU Information'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)

        else:
            main_header = 'Please Login to Access This Page..!!'
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)

        template_values = {
            'main_header': main_header,
            'login_logout': login_logout,
            'login_logout_url': login_logout_url,
            'user': user
        }
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(template_values))
