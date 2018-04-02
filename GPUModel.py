from google.appengine.ext import ndb


class GPUModel(ndb.Model):
    geometryShader = ndb.BooleanProperty(default=False)
    tesselationShader = ndb.BooleanProperty(default=False)
    shaderInt16 = ndb.BooleanProperty(default=False)
    sparseBinding = ndb.BooleanProperty(default=False)
    textureCompressionETC2 = ndb.BooleanProperty(default=False)
    vertexPipelineStoresAndAtomics = ndb.BooleanProperty(default=False)
