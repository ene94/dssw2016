#!/usr/bin/env python

import webapp2

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp \
    import template

class Shout(db.Model):
    message = db.StringProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    who = db.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        shouts = db.GqlQuery(
            'SELECT * FROM Shout '
            'ORDER BY when DESC')
        values = {
            'shouts': shouts
        }
        self.response.out.write(
        template.render('static/elements/chat.html',
                        values))
    def post(self):
        shout = Shout(
            message=self.request.get('message'),
            who=self.request.get('who'))
        shout.put()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/chat', MainHandler)
], debug=True)
