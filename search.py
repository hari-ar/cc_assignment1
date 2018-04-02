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


class Search(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        gpu_list = ''

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
            'user': user,
            'gpu_list': gpu_list
        }

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        gpu_list = ''

        if user:
            main_header = 'GPU Information'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            gpu_list = GPUModel.query()
            if self.request.get("geometryShader"):
                gpu_list = gpu_list.filter(GPUModel.geometryShader == True)
            if self.request.get("tesselationShader"):
                gpu_list = gpu_list.filter(GPUModel.tesselationShader == True)
            if self.request.get("shaderInt16"):
                gpu_list = gpu_list.filter(GPUModel.shaderInt16 == True)
            if self.request.get("sparseBinding"):
                gpu_list = gpu_list.filter(GPUModel.sparseBinding == True)
            if self.request.get("textureCompressionETC2"):
                gpu_list = gpu_list.filter(GPUModel.textureCompressionETC2 == True)
            if self.request.get("vertexPipelineStoresAndAtomics"):
                gpu_list = gpu_list.filter(GPUModel.vertexPipelineStoresAndAtomics == True)
            gpu_list = gpu_list.fetch()
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

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))
