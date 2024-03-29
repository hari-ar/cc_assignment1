import webapp2
from google.appengine.api import users
import jinja2
import os

from GPUModel import GPUModel
from UploadHandler import UploadHandler
from add import Add
from display import Display
from edit import Edit
from file import File
from search import Search

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        gpu_list = ''

        if user:
            main_header = 'GPU Information'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            gpu_list = GPUModel.query().fetch()

        else:
            main_header = 'Please Login to Access This Page..!!'
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)

        template_values = {
            'main_header': main_header,
            'login_logout': login_logout,
            'login_logout_url': login_logout_url,
            'user': user,
            'gpu_list': gpu_list
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add', Add),
    ('/search', Search),
    ('/edit', Edit),
    ('/display', Display),
    ('/file', File),
    ('/upload', UploadHandler)
], debug=True)
