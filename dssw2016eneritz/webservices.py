#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp \
    import template
import urllib
import json

class MapHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(
            template.render('static/elements/es/map-es.html', {}))

    def post(self):
        #ask for data
        serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'
        address = self.request.get('address')
        url = serviceurl + urllib.urlencode({'address': address})
        uh = urllib.urlopen(url)
        data = uh.read()
        #process the result
        js = json.loads(str(data))
        location = js['results'][0]['formatted_address']
        lat = js['results'][0]['geometry']['location']['lat']
        lng = js['results'][0]['geometry']['location']['lng']
        #coords = "latitud: " + str(lat) + " , longitud: " + str(lng)
        values = {'address': address , 'location': location , 'lat': lat, 'lng': lng}
        self.response.out.write(
            template.render('static/elements/es/map-es.html', values))

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(
            template.render('static/elements/es/login-es.html', {}))
        #clientID:606652852649-a4m0dlihj050t108ltlequa0cglsth09.apps.googleusercontent.com
        #clientSecret: nwlPpNAcaiK6hG32t6xTkpEQ

app = webapp2.WSGIApplication([
    ('/webservices/map/', MapHandler),
    ('/webservices/login/', LoginHandler)
], debug=True)
