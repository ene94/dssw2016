#!/usr/bin/env python

import myUtils
import webapp2
from google.appengine.ext.webapp \
    import template
from webapp2_extras import sessions
import session_module

class MainHandler(session_module.BaseSessionHandler):
    def get(self):
        sessionMessage = ""
        counterMessage = ""
        if self.session.get('counter'):
            sessionMessage = 'Existe una sesion activa '
            counter = self.session.get('counter')
            self.session['counter'] = counter + 1
            counterMessage = str(self.session.get('counter'))
        else:
            sessionMessage = 'Sesion nueva'
            self.session['counter'] = 1
            counterMessage = str(self.session.get('counter'))
        values = {
            'sessionMessage': sessionMessage,
            'counterMessage': counterMessage
        }

        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/main-' + lang + '.html', values))

class InitHandler(webapp2.RequestHandler):
    def get(self):
        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/initial-' + lang + '.html', {}))

class LogoutHandler(session_module.BaseSessionHandler):
    def get(self):
        if(self.session['counter']):
            del self.session['counter']
        self.redirect('/')

#This is needed to configure the session secret key
#Runs first in the whole application
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication(
[
    ('/logoutSession/', LogoutHandler),
    ('/', InitHandler),
    ('/main/', MainHandler),
], config = config, debug=True)
