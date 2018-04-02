from google.appengine.ext import blobstore, ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
import jinja2
import os

from GPUModel import GPUModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):
        upload = self.get_uploads()[0]
        blob_info = blobstore.BlobReader(upload.key())
        file_object = blob_info.read()
        lines = file_object.split("\n")
        not_added = 0
        added_count = 0
        for line in lines:
            if line != "":
                each_line = line.split(",")
                new_model_key = ndb.Key(GPUModel, each_line[0])
                new_model = new_model_key.get()
                if new_model:
                    not_added += 1
                    print(not_added)
                else:
                    new_model = GPUModel(id=each_line[0])
                    if each_line[1].lower() == "true" or each_line[1].lower() == "t":
                        new_model.geometryShader = True
                    if each_line[2].lower() == "true" or each_line[2].lower() == "t":
                        new_model.tesselationShader = True
                    if each_line[3].lower() == "true" or each_line[3].lower() == "t":
                        new_model.shaderInt16 = True
                    if each_line[4].lower() == "true" or each_line[4].lower() == "t":
                        new_model.sparseBinding = True
                    if each_line[5].lower() == "true" or each_line[5].lower() == "t":
                        new_model.textureCompressionETC2 = True
                    if each_line[6].lower() == "true" or each_line[6].lower() == "t":
                        new_model.vertexPipelineStoresAndAtomics = True
                    new_model.put()
                    added_count += 1
                    print(added_count)
        template_values = {
            'not_added': not_added,
            'added': added_count
        }

        template = JINJA_ENVIRONMENT.get_template('file_upload_results.html')
        self.response.write(template.render(template_values))
