from flask import Flask, request, session,Response
from flask import render_template
import uuid ;
import os
import json


app = Flask(__name__,static_url_path='/static')
port = 8081
folder = os.path.expanduser('~') ;
myfiles = []
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
@app.route('/',methods=['GET'])
def get():
	session['uid'] = uuid.uuid4().urn[9:] ;
	id = request.args.get('id') ;
	return render_template('authorization.html',id=id) ;


@app.route('/get',methods=['GET'])
def get_auth():
	pass	

@app.route('/set',methods=['POST']) 
def set():
	code = request.args.get('code')
	if code is not None:
		info = {}
		info['uid'] = 'support@the-phi.com' ;
		info['uii'] = 'Mock User' ;

		session['uid'] = info
		return '1' ;
	else:
		del session['uid'] ;
		return '0' 
	
@app.route('/authorize',methods=['POST'])
def authorize() :
	key = session['uid'] ;	
	if key is not None:
		url  = '/static/success.html?code=' +  key ;
	else:
		url = 'error.html'
	print request.endpoint
	return url ;


@app.route('/files',methods=['GET'])
def get_files():
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
@app.route("/info",methods=['GET','POST']) 
def get_uid():
	if 'uid' in session:
		info = session['uid'] 
		return json.dumps(info);
	else:
		return '0' 
"""
	This function sets the code from which the authentication token is requested

"""
@app.route('/set',methods=['POST'])
def set_code():
	code = request.args.get('code') ;
	if 'uid' in session:
		return '1';
	else:
		return '0';


@app.route('/stream',methods=['GET'])
def stream():
	id = request.args.get('id') ;
	file = ([file for file in myfiles if file['name'] == id])[0]
	print file 
	return Response((open(file['path'])).read())
	#[]
	#http://blog.miguelgrinberg.com/post/video-streaming-with-flask
if __name__ == '__main__':
	app.debug = True
	app.secret_key = '1.61803399-bkr3871v3&[v3n71v]-2@11h8r5:4qm!'
	app.run(port = port) 


