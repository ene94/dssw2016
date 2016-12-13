#!/usr/bin/env python

import webapp2
import re

from google.appengine.ext.webapp \
    import template

class Register(webapp2.RequestHandler):
    def get(self):
        #check language from get params
        LANGUAGE = self.request.get('lang')
        #display selected language registration page
        if LANGUAGE == "en":
            self.response.out.write(
                template.render('static/elements/en/register-en.html', {}))
        elif LANGUAGE == "eus":
            self.response.out.write(
                template.render('static/elements/eus/register-eus.html', {}))
        else:
            self.response.out.write(
                template.render('static/elements/es/register-es.html', {}))

    def post(self):
        #get parameters
        LANGUAGE = self.request.get('lang')
        username = self.request.get('username')
        password = self.request.get('password')
        password2 = self.request.get('password2')
        email = self.request.get('email')
        usernameError = ""
        passwordError = ""
        password2Error = ""
        emailError = ""
        error = False

        #validate form info
        if not valid_username(username):
            error = True
            usernameError = "El usuario debe contener solo letras"
        if not valid_password(password):
            error = True
            passwordError = "La contrasena debe ser alfanumerica y tener 6 caracteres"
        if not valid_password2(password2):
            error = True
            password2Error = "La contrasena repetida debe ser alfanumerica y tener 6 caracteres"
        if password != password2:
            error = True
            password2Error += "r\n Las contrasenas deben coincidir"
        if not valid_email(email):
            error = True
            emailError = "No es un email valido"

        #show apropiate response --> ERROR in en/eus/es
        if error == True:
            values = fill_values(username, password, password2, email, usernameError, passwordError, password2Error, emailError)
            if LANGUAGE == "en":
                self.response.out.write(
                    template.render('static/elements/en/register-en.html', values))
                self.response.write('<h1>ERROR</h1>')
            elif LANGUAGE == "eus":
                self.response.out.write(
                    template.render('static/elements/eus/register-eus.html', values))
                self.response.write('<h1>ARAZOAK</h1>')
            else:
                self.response.out.write(
                    template.render('static/elements/es/register-es.html', values))
                self.response.write('<h1>ERROR</h1>')
        else:
            if LANGUAGE == "en":
                self.response.out.write(
                    template.render('static/elements/en/register-en.html', {}))
                self.response.write('<h1>The form has been received successfuly</h1>')
                self.response.write('<p>Welcome: %s</p>' % username)
            elif LANGUAGE == "eus":
                self.response.out.write(
                    template.render('static/elements/eus/register-eus.html', {}))
                self.response.write('<h1>Formularioa ongi jaso da</h1>')
                self.response.write('<p>Ongi etorri: %s</p>' % username)
            else:
                self.response.out.write(
                    template.render('static/elements/es/register-es.html', {}))
                self.response.write('<h1>El formulario ha sido recibido correctamente</h1>')
                self.response.write('<p>Bienvenid@: %s</p>' % username)

#form parameter's restriction
USER_RE = re.compile('[a-zA-Z]{3,20}')
PASSWORD_RE = re.compile('[a-zA-Z0-9]{6,6}')
PASSWORD2_RE = re.compile('[a-zA-Z0-9]{6,6}')
EMAIL_RE = re.compile('(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)')

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_password2(password2):
    return PASSWORD2_RE.match(password2)

def valid_email(email):
    return EMAIL_RE.match(email)

#values to fill the html texts holders written as {{something}}
def fill_values(username, password, password2, email, usernameError, passwordError, password2Error, emailError):
    values = {
        'username': username,
        'password': password,
        'password2': password2,
        'email': email,
        'usernameError': usernameError,
        'passwordError': passwordError,
        'password2Error': password2Error,
        'emailError': emailError
    }
    return values

app = webapp2.WSGIApplication([
    ('/register.*', Register),
], debug=True)
