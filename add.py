import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from GPUModel import GPUModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Add(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
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

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        error_message = ''

        if user:
            main_header = 'GPU Information'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            my_model_key = ndb.Key('GPUModel',self.request.get("gpuname"))
            my_model = my_model_key.get()
            if my_model:
                error_message = 'GPU Already exists ! Please retry'
            else:
                my_model = GPUModel(id=self.request.get("gpuname"))

                if self.request.get("geometryShader"):
                    my_model.geometryShader = True
                if self.request.get("tesselationShader"):
                    my_model.tesselationShader = True
                if self.request.get("shaderInt16"):
                    my_model.shaderInt16 = True
                if self.request.get("sparseBinding"):
                    my_model.sparseBinding = True
                if self.request.get("textureCompressionETC2"):
                    my_model.textureCompressionETC2 = True
                if self.request.get("vertexPipelineStoresAndAtomics"):
                    my_model.vertexPipelineStoresAndAtomics = True
                my_model.put()
                self.redirect('/')


        else:
            main_header = 'Please Login to Access This Page..!!'
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)
        template_values = {
            'main_header': main_header,
            'login_logout': login_logout,
            'login_logout_url': login_logout_url,
            'user': user,
            'error_message': error_message
        }
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(template_values))
