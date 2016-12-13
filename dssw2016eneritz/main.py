#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp \
    import template

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #check language from get params
        LANGUAGE = "es"
        lan = self.request.get('lang')
        if lan != '':
            LANGUAGE = lan
        #display selected language main page
        if LANGUAGE == "en":
            self.response.out.write(
                template.render('static/elements/en/main-en.html', {}))
        elif LANGUAGE == "eus":
            self.response.out.write(
                template.render('static/elements/eus/main-eus.html', {}))
        else:
            self.response.out.write(
                template.render('static/elements/es/main-es.html', {}))

app = webapp2.WSGIApplication([
    ('.*', MainHandler)
], debug=True)
