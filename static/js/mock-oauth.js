/***
* This is a mock implementation of an oauth it is designed to allow the users to implement against a mock oauth 2.0 service
* This implementation goes with a flask based oauth-mock in case users don't have keys or an internet connection
*/
if (!mock){
	var mock = {}
}

mock.oauth = {}
/*
* This function implements an oauth login that should lead to an authorization page
*/
mock.oauth.login = function(){
	jx.dom.hide('authentication') ;
	jx.dom.show('authorization') ;
}
mock.oauth.cancel = function(){
	jx.dom.hide('authorization') ;
	jx.dom.show('authentication') ;
}
/**
* At this point the user have granted permission to the application to access their account
* This function will invoke the api to simulate a response from the service provider.
*/
mock.oauth.init = function(){
	httpclient = HttpClient.instance() ;
	var url = ([window.location.pathname,'authorize']).join('')
	httpclient.post(url,function(x){
		var url = ([window.location.pathname,x.responseText]).join('').replace(/\/\/static/,'/static')
		window.open(url,'_self','width=405') 
	})
}


