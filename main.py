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
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import os
from google.appengine.api import images
import logging
import models
import logic
import google.appengine.ext.db

class MainPage(webapp2.RequestHandler):
	teacher1, teacher2 = (None, None)
	def get(self):
		global teacher1
		global teacher2
		teacher1, teacher2 = logic.fetch_teachers(49)
		template_values = {
			'teacher1picture': teacher1.picture,
			'teacher2picture': teacher2.picture,
			'teacher1name': teacher1.name,
			'teacher2name': teacher2.name
		}
		# q = models.Teacher.all()
		# q.filter("number >", -1)
		# results = q.fetch(49)
		# for result in results:
		# 	result.rating = 1400
		# 	result.put()

		template_file = os.path.join(os.path.dirname(__file__), 'templates/index.html')
		self.response.out.write(template.render(template_file, template_values))

	def post(self):
		global teacher1
		global teacher2
		if self.request.POST.getall('teacher1'):
			winner = teacher1
		else:
			winner = teacher2
		logic.adjust_ratings(teacher1, teacher2, winner)
		self.redirect('/')
		
class RankingsPage(webapp2.RequestHandler):
	def get(self):
		q = models.Teacher.all()
		q = db.GqlQuery("SELECT * FROM Teacher ORDER BY rating DESC")
		results = q.fetch(49)
		template_values = {
			"teachers": results
		}

		template_file = os.path.join(os.path.dirname(__file__), 'templates/rankings.html')
		self.response.out.write(template.render(template_file, template_values))

class Upload(webapp2.RequestHandler):
	def post(self):
		template_file = os.path.join(os.path.dirname(__file__), 'templates/upload.html')
		self.response.out.write(template.render(template_file, {}))
		i = 0
		for img in self.request.POST.getall('img[]'):
			teacher = models.Teacher()
			filename, ext = os.path.splitext(img.filename)
			teacher.name = filename.replace("_", " ")
			teacher.number = i
			teacher.picture = img.filename
			teacher.put()
			i += 1

	def get(self):
		template_file = os.path.join(os.path.dirname(__file__), 'templates/upload.html')
		self.response.out.write(template.render(template_file, {}))

app = webapp2.WSGIApplication([('/', MainPage),
							   ('/rankings', RankingsPage),
							   ('/upload', Upload)],
							  debug=True)