#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp \
    import template
import urllib
import json

class MapHandler(webapp2.RequestHandler):
    def get(self):
        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/map-' + lang + '.html', {}))

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
        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/map-' + lang + '.html', values))

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/login-' + lang + '.html', {}))

app = webapp2.WSGIApplication([
    ('/webservices/map/', MapHandler),
    ('/webservices/login/', LoginHandler)
], debug=True)
