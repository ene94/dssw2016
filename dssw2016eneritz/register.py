#!/usr/bin/env python

import webapp2

from google.appengine.ext.webapp \
    import template

class MainHandler(webapp2.RequestHandler):
    def get(self):
		self.response.out.write(
            template.render('static/elements/register-es.html', {}))

    def post(self):
        self.response.out.write(
            template.render('static/elements/register-es.html', {}))
        self.response.write('<h1>Formulario recibido correctamente</h1>')
        self.response.write("Nombre: %s <br>" % self.request.get('username'))

class EnglishHandler(webapp2.RequestHandler):
    def get(self):
		self.response.out.write(
            template.render('static/elements/register-en.html', {}))

    def post(self):
        self.response.out.write(
            template.render('static/elements/register-en.html', {}))
        self.response.write('<h1>Form successfuly received</h1>')
        self.response.write("Name: %s <br>" % self.request.get('username'))

class EuskaraHandler(webapp2.RequestHandler):
    def get(self):
		self.response.out.write(
            template.render('static/elements/register-eus.html', {}))

    def post(self):
        #query_params = {'guestbook_name': guestbook_name}
        #self.redirect('/?' + urllib.urlencode(query_params))
        self.response.out.write(
            template.render('static/elements/register-eus.html', {}))
        self.response.write('<h1>Formularioa ondo jaso da</h1>')
        self.response.write("Izena: %s <br>" % self.request.get('username'))


app = webapp2.WSGIApplication([
    ('/register/', MainHandler),
    ('/register/es', MainHandler),
    ('/register/en', EnglishHandler),
    ('/register/eus', EuskaraHandler)
], debug=True)
