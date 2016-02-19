"""
	Cloud Broker Emulator 1.0
	The Phi Technology LLC
	Steve L. Nyemba <steve@the-phi.com>
	
	This API is a sketch for a cloud service broker. A cloud service broker
	features is articulated around authentication and proxy to the cloud.
	We have implemented:	
		1- Authentication/Authorization: OAuth 2.0 Emulation
		2- Proxy to Cloud to perform reads of files (for now)
	
	This API should be used as an emulator, it doesn't really access any
	cloud service but demonstrates how it could potentially be and allows
	developement against an interface.

	AUTHENTICTION & AUTHORIZATION : OAUTH 2.0 EMULATION:

	The OAuth 2.0 is standard https://pingidentity.com/OAuth. The emulator
	is supported by an HTML UI that is fully OAUTH 2.0 Compliant
	
	CLOUD BROKER EMULATION

	The cloud broker enables interacton with an arbitrary cloud service
	provider that supports OAuth 2.0:
		- user information
		- access to files
		- sharing
	
	USAGE:

	@TODO:
		- Implement sharing
	
	@LIMITATIONS:
	This emulation is designed to emulate basic interaction and does not
	implement domain specific policies (i.e how you choos to log data,...)

"""
from flask import Flask, request, session,Response
from flask import render_template
import uuid ;
import os
import json
from random import random

app = Flask(__name__,static_url_path='/static')
port = 8081
folder = os.path.expanduser('~') ;
myfiles = []
#
# Before the API is made available it will load a few files from disk and make
# them available to a client that interacts with it.
# 
list_items = os.listdir(folder)
for item in list_items:
	if item not in ['Documents','Pictures','Music','Movies']:
		continue;
	path = "".join([folder,os.sep,item])
	for root, dirs, files in os.walk(path, topdown=False):
		i = 0;
		for name in files:
			value =("".join([root,os.sep,name])) ;	
			if os.path.exists(value) and name.startswith('.') == False:
				i = i+ 1
				file = {}
				file['name'] = name
				file['path'] = value
				myfiles.append(file) 
			if i == 10:
				break;
		if i == 10:
			break;
"""
	This function launches the authorization & authentication page for a
	given service. The service can be given any identifier
	{dropbox,box,google-drive,one-drive}
"""
@app.route('/<id>/',methods=['GET'])
def get(id):
	session['uid'] = uuid.uuid4().urn[9:] ;
	#id = request.args.get('id') ;
	return render_template('authorization.html',id=id) ;


"""
	This function is part of the OAuth 2.0 specifications that	
"""
@app.route('/<id>/authorize',methods=['POST'])
def authorize(id) :
	key = session['uid'] ;	
	if key is not None:
		url  = '/static/success.html?code=' +  key ;
	else:
		url = 'error.html'
	print request.endpoint
	return url ;


"""
	This endpoint is called when the oauth server has responded. At this
	point we are sure to have connectivity with the cloud service provider.
	With the connectivity established we can now do whatever we need to do.
"""
@app.route('/<id>/set',methods=['POST']) 
def set(id):
	code = request.args.get('code')
	if code is not None:
		info = {}
		info['uid'] = 'support@the-phi.com' ;
		info['uii'] = 'Mock User' ;
		info['space'] = {}
		info['space']['used'] = random()*700
		info['space']['size'] = random()*1000
		session['uid'] = info
		return '1' ;
	else:
		del session['uid'] ;
		return '0' 
"""
	This function provides user information & high level cloud space usage
	for a given cloud service provider specified by the identifier
"""
@app.route('/<id>/isLoggedIn',methods=['GET'])
def user(id):
	info = session['uid']
	return json.dumps(info)
"""
	This function will return a list of files specified by a
	filter={mp3,m4a,mp4,doc,xlx,odt} the filters are the extensions.
	@TODO: We must wrap extensions by a label
"""
@app.route('/<id>/files',methods=['GET'])
def get_files(id):
	filter = request.args.get('filter') ;
	if filter is None:
		filter = 'mp3' ;
	rfiles = [] ;
	for file in myfiles:
		if file['name'].endswith(filter):
			rfiles.append(file) ;
	print filter,'get.files',len(rfiles)
	return json.dumps(rfiles)

"""
	This function returns the current user's information i.e just high level information nothing major
	The basic idea is uid: email, uii: full name
"""
@app.route("/<id>/info",methods=['GET','POST']) 
def get_uid(id):
	if 'uid' in session:
		info = session['uid'] 
		return json.dumps(info);
	else:
		return '0' 
#"""
#	This function sets the code from which the authentication token is requested
#
#"""
#@app.route('/<id>/set',methods=['POST'])
#def set_code():
#	code = request.args.get('code') ;
#	if 'uid' in session:
#		return '1';
#	else:
#		return '0';
#
"""
	This function will stream a given file from a cloud service provider.
	The streaming of the file is analogous to a download
"""
@app.route('/<id>/stream',methods=['GET'])
def stream(id):
	#id = request.args.get('id') ;
	file = ([file for file in myfiles if file['name'] == id])[0]
	print file 
	return Response((open(file['path'])).read())
	#[]
	#http://blog.miguelgrinberg.com/post/video-streaming-with-flask

if __name__ == '__main__':
	app.debug = True
	app.secret_key = '1.61803399-bkr3871v3&[v3n71v]-2@11h8r5:4qm!'
	app.run(port = port,threaded=True) 


