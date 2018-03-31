#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import users
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainHandler(webapp2.RequestHandler):
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
            main_header = 'Please Login to see the GPU Information'
            login_logout = 'Login'
            login_logout_url = users.create_login_url(self.request.uri)

        template_values = {
            'main_header': main_header,
            'login_logout': login_logout,
            'login_logout_url': login_logout_url,
            'user': user
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
        ('/', MainHandler)
], debug=True)