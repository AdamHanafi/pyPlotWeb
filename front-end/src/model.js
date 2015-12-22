/** This module updates the model on the server
 *  @module model
 * 
 */


grapher.model = grapher.model || function() {
	
	//target address of the server
	this._url = window.location.href;
        //#TODO: Replace with unique user ID
	this._username = localStorage.username;
	
	this._sendRequests = function(data, callBack, context) {
		console.log("_sendRequests");
		$.ajax({
			url: this._url,
			type: "POST",
			contentType: 'application/json',
			dataType: "json",
			data: JSON.stringify(data)
		}).success(function(response){
			if (callBack) {
				//We must preserve the context on the callback
				callBack.apply(context, arguments);
			}
		});
	};
	
	this.updateControl = function(type, options, callBack, context) {
		var request = {
			type: "updateControl",
			control: type,
			options: options,
			username: this._username
		};
		this._sendRequests(request, callBack, context);
	};
	
	this.deleteHistoryItem = function(index, callBack, context) {
		var request = {
			type: "deleteHistoryItem",
			index: index,
			username: this._username
		};
		this._sendRequests(request, callBack, context);
	};
	
	this.updateElement = function(element, callBack, context) {
		var request = {
			type: "updateElement",
			element: element,
			username: this._username
		};
	};
	
	//Submit a brand new query
	this.newQuery = function(q, callBack, context) {
		var request = {
			type: "newQuery",
			query: q,
			username: this._username
		};
		this._sendRequests(request, callBack, context);
	};
	
	//Register a new user
        this.registerUser = function(credentials, callBack, context) {
		var request = {
			type: "register",
			username: credentials.username,
			password: credentials.password,
			passwordConfirm: credentials.passwordConfirm
		};
		this._sendRequests(request, callBack, context);
	};
	
	//Log in an already created user
	this.login = function(credentials, callBack, context) {
		console.log("login");
		var request = {
			type: "login",
			username: credentials.username,
			password: credentials.password
		};
		this._sendRequests(request, callBack, context);
	};
	
	//Log in a user only with the session ID that is saved in the browser
	this.loginExistingUser = function(username, callBack, context) {
		console.log("loginExistingUser");
		var request = {
			type: "loginExistingUser",
			username: username
		};
		this._sendRequests(request, callBack, context);
		
	};
	
	this.updateUserName = function() {
		this._username = localStorage.username;
	};
	
	
};