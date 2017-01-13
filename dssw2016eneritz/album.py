#!/usr/bin/env python

import webapp2
from google.appengine.ext.webapp \
    import template
from webapp2_extras import sessions
import session_module
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
import urllib

class Image(ndb.Model):
    user = ndb.StringProperty()
    public = ndb.BooleanProperty()
    blob_key = ndb.BlobKeyProperty()

class PhotoUploadHandler(session_module.BaseSessionHandler, blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        logedUser = self.session.get('logedUser')
        googleUser = self.session.get('googleUser')
        user = ""
        if logedUser:
            user = logedUser
        if googleUser:
            user = googleUser
        values = {'logedUser': user}
        if user:
            upload_url = blobstore.create_upload_url('/album/upload/')
            values = {'logedUser': user, 'upload_url': upload_url}

        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/uploadImage-' + lang + '.html', values))
    def post(self):
        logedUser = self.session.get('logedUser')
        googleUser = self.session.get('googleUser')
        user = ""
        if logedUser:
            user = logedUser
        if googleUser:
            user = googleUser
        values = {'logedUser': user}
        if user:
            upload_files = self.get_uploads('file')
            blob_info = upload_files[0] # guardo la imagen en el BlobStore
    	    img = Image(user=user, public=self.request.get("access")=="public", blob_key=blob_info.key())
            img.put() #guardo el objeto Image

        self.redirect('/album/')

class ViewHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        fotos = blobstore.BlobInfo.all()
        for foto in fotos:
            self.response.out.write('<img src="/album/serve/%s" width="75" height="75"></td>' % foto.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
 	 def get(self, resource):
		resource = str(urllib.unquote(resource))
		blob_info = blobstore.BlobInfo.get(resource)
		self.send_blob(blob_info)

class AlbumHandler(session_module.BaseSessionHandler, blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        permission = self.request.get('permission')
        logedUser = self.session.get('logedUser')
        googleUser = self.session.get('googleUser')
        user = ""
        if logedUser:
            user = logedUser
        if googleUser:
            user = googleUser
        if user:
            #get images
            s = ""
            i = 1
            #images = blobstore.BlobInfo.all()
            #FILTER IMAGES
            if permission == "public":
                images = Image.query().filter(Image.public == True)
            else:
                images = Image.query().filter(Image.public == False).filter(Image.user == logedUser)

            for img in images:
                s += '<img onmouseover="preview.src=img{0}.src" name="img{0}" src="/album/serve/{1}" alt="" />'.format(i,img.blob_key)
                i += 1

            values = {'logedUser': user}
            lang = self.request.get('lang')#check language from get params
            if lang == '': lang = "es"
            self.response.out.write(
                        template.render('static/elements/' + lang + '/album-' + lang + '.html', values))#html start
            self.response.out.write(s)#images
            self.response.out.write(#html end
                '''
                </div>
                <div class="preview" align="center">
                <img name="preview" src="/img/girl_computer_anime.png" alt=""/>
                </div>

                </div> <!-- Close the gallery div -->
                <br><br><br>
                </div></td></tr><tr><td colspan="6"><img src="/img/tail.jpg" class="backgroundImages" alt="tail"></td>
                </tr></table></body></html>
                '''
            )
        else:
            error = "Tienes que iniciar sesion"
            values = {'error': error}
            lang = self.request.get('lang')#check language from get params
            if lang == '': lang = "es"
            self.response.out.write(
                        template.render('static/elements/' + lang + '/album-' + lang + '.html', values))

app = webapp2.WSGIApplication(
[
    ('/album/', AlbumHandler),
    ('/album/upload/', PhotoUploadHandler),
    ('/album/download/', ViewHandler),
    ('/album/serve/([^/]+)?', ServeHandler),
], config = session_module.config, debug=True)
