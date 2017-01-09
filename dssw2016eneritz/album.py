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

class Image(ndb.Model):
    user = ndb.StringProperty()
    public = ndb.BooleanProperty()
    blob_key = ndb.BlobKeyProperty()

class AlbumHandler(session_module.BaseSessionHandler, blobstore_handlers.BlobstoreUploadHandler):
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
            upload_url = blobstore.create_upload_url('/album/upload')
            values = {'logedUser': user, 'upload_url': upload_url}

        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/album-' + lang + '.html', values))
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

        lang = self.request.get('lang')#check language from get params
        if lang == '': lang = "es"
        self.response.out.write(
                    template.render('static/elements/' + lang + '/album-' + lang + '.html', values))

class ViewHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self):
		fotos= blobstore.BlobInfo.all()
		for foto in fotos:
            self.response.out.write('<img src="/album/serve/%s"></image></td>' % foto.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
 	 def get(self, resource):
		resource = str(urllib.unquote(resource))
		blob_info = blobstore.BlobInfo.get(resource)
		self.send_blob(blob_info)


app = webapp2.WSGIApplication(
[
    ('/album/', AlbumHandler),
    ('/album/upload', AlbumHandler),
    ('/album/download', ViewHandler),
    ('/album/serve/([^/]+)?', ServeHandler)],
], config = session_module.config, debug=True)
