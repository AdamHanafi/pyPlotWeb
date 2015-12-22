/** The entry pointgrunt
 * @module grapher
 * 
 */

var grapher = function(target, textInput) {
	this._textInput = $(textInput);
	this._functions = [];
	this._modules = {};
	this._modules.model = new grapher.model();
	this._initiated = false;
	this._query = undefined;
	this._plot2D = undefined;
	this._plot3D = undefined;
        this._isLoggedIn = false;
	this._loginpage = {
		element: undefined,
		type: "login"
	};
	this._loginPageCreated = false;
	
	this.setTarget = function(target) {
		var y = $(target);
		if (y.is("div")) {
			this._target = y;
		}
		else {
			throw new Error("Target element is not a div!");
		}
		
	};
	
	if (target) {
		this.setTarget(target);
	}
	else {
		this._target = undefined;
	}
	
	this.setQuery = function(query) {
		this._query = query;
	};
	
	this._setupProto = function() {
	};
	
	
	this._checkPrerequisites = function() {
		if (this._functions.length > 0) {
			if (this._target) {
				return true;
			}
			else {
				return false;
			}
		}
		else {
			return false;
		}
	};
	
	this.didClickHistoryMenu = function(e, ui) {
		var actionType = ui.item[0].innerHTML;
		var t = $(ui.item[0]);
		var parentID = t.parent().parent().attr("id");
		if (!parentID) {
			return;
		}
		index = t.parent().parent().attr("grapherItemID"); 
		var parentValue =t.parent().parent().attr("grapherValue");// t.parent().parent().text().replace("Append to searchDelete", "");
		
		//Append history item to query input
		if (actionType === "Append to search") {
			var currentVal = this._textInput.val();
			if (currentVal === "") {
				this._textInput.val(parentValue);
			}
			else {
				this._textInput.val(currentVal + ";" + parentValue);
			}
		}
		//Delete item from the list, a new list will then be sent by the server
		if (actionType === "Delete") {
			this._modules.model.deleteHistoryItem(index, this._createNewWorkspace, this);
		}
	};
	
	
	this._createNewWorkspace = function(args) {
		console.log(args);
		this._target.empty();
		
		if (args.formattedInput) {
			var originalInTarget = $("<div>", {
				width: 800
			});
			this._target.append(originalInTarget);
			originalArea = new grapher.textArea(originalInTarget, args.formattedInput, "Original input", "mathjax", true);
			originalArea.create();
			this._modules.integral = originalArea; 
		}
		
		if (args.plot2D) {
			var plotTarget = $("<div>", {
				width: 800,
				height: 600
			});
			this._target.append(plotTarget);
			this._plot2D = new grapher.plot2D(plotTarget, args.plot2D.grid, args.plot2D.plots, $.proxy(this._updateControl, this));
			this._plot2D.plot();
			this._modules.plot2D = this._plot2D;
			
		}
		if (args.plot3D) {
			var TDPlotTarget = $("<div>", {
				width: 800,
				height: 600
			});
			this._target.append(TDPlotTarget);
			this._plot3D = new grapher.plot3D(TDPlotTarget, args.plot3D.grid, args.plot3D.plots, args.plot3D.vertexColors);
			this._plot3D.plot();
			this._modules.plot3D = this._plot3D;
			
		}
		if (args.table) {
			var tableTarget = $("<div>", {
				width: 800,
				height: 600
			});
			this._target.append(tableTarget);
			this._table = new grapher.table(tableTarget, args.table, $.proxy(this._updateControl, this));
			this._table.create();
			this._modules.table = this._table;
			
		}
		if (args.integral) {
			var intTarget = $("<div>", {
				width: 800
			});
			this._target.append(intTarget);
			intArea = new grapher.textArea(intTarget, args.integral, "Integral", "mathjax");
			intArea.create();
			this._modules.integral = intArea; 
		}
		
		if (args.derivative) {
			var derTarget = $("<div>", {
				width: 800
			});
			this._target.append(derTarget);
			derArea = new grapher.textArea(derTarget, args.derivative, "Derivative", "mathjax");
			derArea.create();
			this._modules.derivative = derArea; 
		}
		
		if (args.helpPage) {
			var helpTarget = $("<div>", {
				width: 800
			});
			this._target.append(helpTarget);
			helpArea = new grapher.textArea(helpTarget, args.helpPage, "Help Page", "markdown");
			helpArea.create();
			this._modules.help = helpArea; 
		}
		
		if (args.historySelection) {
			var listTarget = $("<div>", {
				width: 800
			});
			this._target.append(listTarget);
			listArea = new grapher.listSelection(listTarget, args.historySelection, this.didClickHistoryMenu, this);
			listArea.create();
			this._modules.history = listArea;
			//Empty the query field
			this._textInput.val("");
		}
		
	};
	
	this._updateControl = function(type, options, callBack, context) {
		this._modules.model.updateControl(type, options, callBack, context);
	};
	
	this.generate = function() {
		if (!this._isLoggedIn) {
			return;
		}
		
		//Step1: Instantiate the needed modules
		if (this._initiated === false) {
			this._setupProto();
			this._initiated = true;
		}
		
		//Step 2: Inform the server of the query and create the workspace from the response
		this._modules.model.newQuery(this._query, this._createNewWorkspace, this);
	};
	
	this._loginManager = function(message) {
		console.log(message);
		if (message.success === "false" || message.success === false) {
			alert(message.message);
			if (!this._loginPageCreated) {
				this._setLoginPage();
			}
			return;
		}
		if (message.success === "true" || message.success === true) {
			this._tearDownLoginPage();
			if (message.username) {
				localStorage.setItem("username", message.username);
				this._isLoggedIn = true;
				this._modules.model.updateUserName();
			}
		}
		
	};
	
	this._signupManager = function(message) {
		console.log("message");
		if (message.success === "false" || message.success === false) {
			alert(message.message);
		}
		if (message.success === "true" || message.success === true) {
			alert(message.message);
			this._loginpage.type = "login";
			this._setLoginPage();
		}
	};
	
	this._didClickLoginBtn = function(e) {
		var username = e.data.username.val();
		var password = e.data.password.val();
		e.data.context._modules.model.login({username: username, password: password}, e.data.context._loginManager, e.data.context);
		this._isLoggedIn = true;
	};
	
	this._didClickSignUpBtn = function(e) {
		console.log("signup");
		var username = e.data.username.val();
		var password = e.data.password.val();
		var passwordConfirm = e.data.passwordConfirm.val();
		e.data.context._modules.model.registerUser({username: username, password: password, passwordConfirm: passwordConfirm}, e.data.context._signupManager, e.data.context);
	};
	
	this._tearDownLoginPage = function() {
		if (this._loginpage.element) {
			this._loginpage.element.remove();
		}
		
	};
	
	this._switchPageType = function(e) {
		if (e.data.type === "login") {
			e.data.context._loginpage.type = "login";
			e.data.context._setLoginPage();
		}
		else if (e.data.type === "signup") {
			e.data.context._loginpage.type = "signup";
			e.data.context._setLoginPage();
		}
		
	};
	
	this._setLoginPage = function() {
		//create a wrapper for the entire container
		
		if (!this._loginpage.element) {
			this._loginpage.element = $("<div>", {
				width: "400px",
				height: "300px"
			}).css({
				position: "absolute",
				"border-style": "solid",
				"border-width": "2px"
			});
			
			this._loginpage.signupBtn = $("<input>", {
				type: "button",
				value: "Sign-up"
			});
			
			this._loginpage.signupBtn.click( {context: this, type: "signup"}, this._switchPageType);
			
			this._loginpage.loginBtn = $("<input>", {
				type: "button",
				value: "Login"
			});
			
			this._loginpage.loginBtn.click( {context: this, type: "login"}, this._switchPageType);
			
			
			var titleContainer = $("<div>", {
				width: "100%",
				height: "20%",
				position: "relative"
			});
			titleContainer.append($("<span>").html("Python Grapher"));
			this._loginpage.element.append(titleContainer);
			this._loginpage.element.append(this._loginpage.signupBtn);
			this._loginpage.element.append(this._loginpage.loginBtn);
			this._target.append(this._loginpage.element);
		}
		//*******
		//login user
		//*******
		
		if (this._loginpage.type === "login") {
			if (this._loginpage.element.children()[3]) {
				this._loginpage.element.children()[3].remove();
			}
			var controlContainer = $("<div>", {
				width: "50%",
				height: "80%"
			}).css({
				position: "relative"
			});
			
			//create minor containers
			var inputContainer = $("<div>",{
			}).css({
				position: "relative"
			});
			
			var submitContainer = $("<div>",{
			}).css({
				position: "relative"
			});
			
			//create the controls
			var usernameField = $("<input>",{
				type: "text",
				placeholder: "username"
			}).css({
				left: "0px",
				top: "0px",
				position: "relative"
			});
			var passwordField = $("<input>",{
				type: "password",
				placeholder: "password"
			}).css({
				left: "0px",
				position: "relative"
			});
			
			var submitButton = $("<input>",{
				type: "button",
				value: "Login"
			});
			submitButton.click( {username: usernameField, password: passwordField, context: this}, this._didClickLoginBtn);
			
			//title
			
			//inputs
			inputContainer.append(usernameField);
			inputContainer.append(passwordField);
			controlContainer.append(inputContainer);
			
			//submit
			submitContainer.append(submitButton);
			controlContainer.append(submitContainer);
			
			this._loginpage.element.append(controlContainer);
		}
		//******
		//end login page
		//******
		
		//******
		//start sign-up page
		//******
		else if (this._loginpage.type === "signup") {
			if (this._loginpage.element.children()[3]) {
				this._loginpage.element.children()[3].remove();
			}
			var controlContainerS = $("<div>", {
				width: "50%",
				height: "80%"
			}).css({
				position: "relative"
			});
			
			//create minor containers
			var inputContainerS = $("<div>",{
			}).css({
				position: "relative"
			});
			
			var submitContainerS = $("<div>",{
			}).css({
				position: "relative"
			});
			
			
			//create the controls
			var usernameFieldS = $("<input>",{
				type: "text",
				placeholder: "username"
			}).css({
				left: "0px",
				top: "0px",
				position: "relative"
			});
			var passwordFieldS = $("<input>",{
				type: "password",
				placeholder: "password"
			}).css({
				left: "0px",
				position: "relative"
			});
			
			var passwordConfirmFieldS = $("<input>",{
				type: "password",
				placeholder: "Confirm Password"
			}).css({
				left: "0px",
				position: "relative"
			});
			
			var submitButtonS = $("<input>",{
				type: "button",
				value: "Signup"
			});
			submitButtonS.click( {username: usernameFieldS, password: passwordFieldS, passwordConfirm: passwordConfirmFieldS, context: this}, this._didClickSignUpBtn);
			
			
			//inputs
			inputContainerS.append(usernameFieldS);
			inputContainerS.append(passwordFieldS);
			inputContainerS.append(passwordConfirmFieldS);
			controlContainerS.append(inputContainerS);
			
			//submit
			submitContainerS.append(submitButtonS);
			controlContainerS.append(submitContainerS);
			
			this._loginpage.element.append(controlContainerS);
		}
		//******
		//end sign-up page
		//******
		
		this._loginPageCreated = true;
	};
	
	//Self-invoking function that checks initial login and sets up MathJax
	this._init = function() {
		
		MathJax.Hub.Config({
			SVG: {
				scale: 150
			}
		});
		
		var data = localStorage;
		if (!data.username) {
			this._setLoginPage();
			return;
		}
		
		//If a username already exists, try to log him in
		//If a timeout occured, then the user has to log in manually
		this._isLoggedIn = true;
		this._modules.model.loginExistingUser(data.username, this._loginManager, this);
		
	};
	this._init();
};