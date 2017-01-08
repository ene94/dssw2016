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

class ChatHandler(webapp2.RequestHandler):
    def get(self):
        shouts = db.GqlQuery(
            'SELECT * FROM Shout '
            'ORDER BY when DESC')
        values = {
            'shouts': shouts
        }
        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/chat-' + lang + '.html', values))
    def post(self):
        shout = Shout(
            message=self.request.get('message'),
            who=self.request.get('who'))
        shout.put()
        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.redirect('/chat/?lang=' + lang)

app = webapp2.WSGIApplication([
    ('/chat/', ChatHandler)
], debug=True)
