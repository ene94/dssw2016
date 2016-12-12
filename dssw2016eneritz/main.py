#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp \
    import template

class MainHandler(webapp2.RequestHandler):
    def get(self):
		self.response.out.write(
            template.render('static/elements/main-es.html', {}))

class EnglishHandler(webapp2.RequestHandler):
    def get(self):
		self.response.out.write(
            template.render('static/elements/main-en.html', {}))

class EuskaraHandler(webapp2.RequestHandler):
    def get(self):
		self.response.out.write(
            template.render('static/elements/main-eus.html', {}))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/es', MainHandler),
    ('/en', EnglishHandler),
    ('/eus', EuskaraHandler),
], debug=True)
