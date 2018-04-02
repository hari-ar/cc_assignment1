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


class Edit(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        gpu_data = ''
        gpu_key = ''

        if user:
            main_header = 'GPU Information'
            login_logout = 'Logout'
            login_logout_url = users.create_logout_url(self.request.uri)
            gpu_name = self.request.get('gpu_id')
            gpu_key = ndb.Key('GPUModel', gpu_name)
            print(gpu_key)
            print(gpu_name)
            gpu_data = gpu_key.get()


            if self.request.get("button") == "Submit":

                if self.request.get("geometryShader"):
                    gpu_data.geometryShader = True
                else:
                    gpu_data.geometryShader = False

                if self.request.get("tesselationShader"):
                    gpu_data.tesselationShader = True
                else:
                    gpu_data.tesselationShader = False

                if self.request.get("shaderInt16"):
                    gpu_data.shaderInt16 = True
                else:
                    gpu_data.shaderInt16 = False

                if self.request.get("sparseBinding"):
                    gpu_data.sparseBinding = True
                else:
                    gpu_data.sparseBinding = False

                if self.request.get("textureCompressionETC2"):
                    gpu_data.textureCompressionETC2 = True
                else:
                    gpu_data.textureCompressionETC2 = False

                if self.request.get("vertexPipelineStoresAndAtomics"):
                    gpu_data.vertexPipelineStoresAndAtomics = True
                else:
                    gpu_data.vertexPipelineStoresAndAtomics = False

                gpu_data.put()
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
            'gpu_data': gpu_data,
            'gpu_name': gpu_name
        }

        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_values))
