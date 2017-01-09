#!/usr/bin/env python

import webapp2
import re
from google.appengine.ext import ndb
from google.appengine.ext.webapp \
    import template
from webapp2_extras import sessions
import session_module

class Register(webapp2.RequestHandler):
    def get(self):
        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/register-' + lang + '.html', {}))

    def post(self):
        #get parameters
        username = self.request.get('username')
        password = self.request.get('password')
        password2 = self.request.get('password2')
        email = self.request.get('email')
        #photo = self.request.get('photo')
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

        # check if user exists: username & email
        userexist = User.query(User.username==username).count()
        if (userexist==1):
            error = True
            usernameError += "Ya existe un usuario con ese nombre"
        emailexist = User.query(User.email==email).count()
        if (emailexist==1):
            error = True
            emailError += "Ya existe un usuario con ese email"

        #show apropiate response --> ERROR in en/eus/es
        if error == True:
            values = fill_values(username, password, password2, email, usernameError, passwordError, password2Error, emailError)
            lang = self.request.get('lang')#check language from get params
            if lang == '': lang = "es"
            self.response.out.write(
                        template.render('static/elements/' + lang + '/register-' + lang + '.html', values))
        else:
            # save user in ddbb
            user = User(
                username = username,
                password = password,
                password2 = password2,
                email = email)
            user.put()
            lang = self.request.get('lang')#check language from get params
            if lang == '': lang = "es"
            values = {'welcome': username}
            self.response.out.write(
                        template.render('static/elements/' + lang + '/register-' + lang + '.html', values))

#server side validation
class AsyncValidation (webapp2.RequestHandler):
    def get(self):
        error = False
        emailError = ""
        email = self.request.get('email2')
        if not valid_email(email):
            error = True
            emailError = "Email NO valido... prueba otra vez"
        emailexist = User.query(User.email==email).count()
        if emailexist==1:
            error = True
            emailError += "Ya existe un usuario con ese email"
        if error == False:
            emailError = ""
        self.response.write(emailError)#returns this to the javascript

class ShowUsers(webapp2.RequestHandler):
    def get(self):
        users = ndb.gql(
            'SELECT * FROM User '
            'ORDER BY username ASC')
        values = {
            'users': users
        }
        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/users-' + lang + '.html', values))

class GoogleLoginHandler(session_module.BaseSessionHandler):
    def post(self):
        email = ""
        logedUser = ""
        if not self.session.get('logedUser'):
            self.session['googleUser'] = self.request.get('email')#SESSION PARAMETER

class LoginHandler(session_module.BaseSessionHandler):
    def get(self):
        logedUser = self.session.get('logedUser')#SESSION PARAMETER
        values = {'logedUser': logedUser}

        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/login-' + lang + '.html', values))
    def post(self):
        password = ""
        email = ""
        logedUser = ""
        messageError = ""
        error = False
        if self.session.get('logedUser'):
            messageError = 'Ya existe una sesion activa'
            logedUser = self.session.get('logedUser')
        elif self.session.get('googleUser'):
            messageError = 'Ya existe una sesion activa'
        else:
            #if app login
            #get parameters
            password = self.request.get('password')
            email = self.request.get('email')

            #validate form info
            if not valid_password(password):
                error = True
            if not valid_email(email):
                error = True
            usuarios = ndb.gql("SELECT * FROM User WHERE email=:1 AND password=:2", email, password)
            if usuarios.count()==0:
            	error = True

            #appropiate response
            if error:
                messageError = "El email o la contrasena son incorrectos"
            else:
                logedUser = email
                self.session['logedUser'] = logedUser#SESSION PARAMETER
                email = ""
                password = ""

        values = {'messageError': messageError, 'email': email, 'password': password, 'logedUser': logedUser}

        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/login-' + lang + '.html', values))

class LogoutHandler(session_module.BaseSessionHandler):
    def get(self):
        if(self.session.get('logedUser')):
            del self.session['logedUser']
        if(self.session.get('googleUser')):
            del self.session['googleUser']
        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.redirect('/register/login/?lang=' + lang)

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

#MODELO para la BBDD
class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    password2 = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    photo = ndb.BlobProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

app = webapp2.WSGIApplication([
    ('/register/', Register),
    ('/register/users/', ShowUsers),
    ('/register/asyncValidation/', AsyncValidation),
    ('/register/login/', LoginHandler),
    ('/register/googleLogin/', GoogleLoginHandler),
    ('/register/logout/', LogoutHandler)
], config=session_module.config, debug=True)
