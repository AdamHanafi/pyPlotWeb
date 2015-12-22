//Type-"mathjax" or "markdown"
grapher.textArea = grapher.textArea || function(target, values, title, type) {
	this._target = target;
	this._values = values;
	this._titleString = title;
	this._type = type || "none";
	this._title = undefined;
	this._content = undefined;
	this._dropDownContainer = undefined;
	
	
	this._didSelectFromMenu = function(e, ui) {
		this._insertMathjax(parseInt(ui.item.value));
	};
	
	this._addDropDown = function() {
		var that = this;
		this._dropDownContainer = $("<select>", {
			width: 200,
			height: 20
		});
		this._title.append(this._dropDownContainer);
		$(this._dropDownContainer).selectmenu();
		$(this._dropDownContainer).selectmenu("option", "position", {
			my: "right top",
			at: "right top"
		});
		for (var k = 0, n = this._values.length; k < n; k++) {
			if (k === 0) {
				$("<option value =" + k + "selected> " + this._values[k].label + ": " + this._values[k].rawText + 
					"</option>").appendTo(this._dropDownContainer);
			}
			else {
				$("<option value =" + k + "> " + this._values[k].label + ": " + this._values[k].rawText + 
					"</option>").appendTo(this._dropDownContainer);
			}
		}
		$(this._dropDownContainer).selectmenu("refresh");
		$(this._dropDownContainer).on("selectmenuselect", $.proxy(this._didSelectFromMenu, this));
	};
	
	this._insertMathjax = function(index) {
		if (this._content) {
			this._content.empty();
		}
		var wrappers = "";
		//Add the wrapper if it is mathjax
		if (this._type === "mathjax") {
			wrappers = "$$";
		}
		
		this._content = $("<div>", {
			width: "100%",
			height: "calc(100% - 30px)"
		}).html(wrappers + this._values[index].formatted + wrappers); //Wrap the content in flags that MathJax can parse
		this._target.append(this._content);
		this._updateMathjax();
	};
	
	this._updateMathjax = function() {
		MathJax.Hub.Typeset(this._content[0]);
	};
	
	this.create = function() {
		//Add some props to the target element
		this._target.css({
			"border-style": "solid",
			"border-width": "1px"
		});
		//Create the title
		this._title = $("<div>", {
			width: "100%",
			height: "30px"
		}).append($("<span>").html(this._titleString));
		this._target.append(this._title);
		
		if (this._type === "mathjax" || this._type === "none") {
			this._insertMathjax(0);
			if (this._values.length > 1) {
				this._addDropDown();
			}
		}
		
		else if (this._type === "markdown") {
			//Get the HTML format of the md source
			HTMLContent = markdown.toHTML(this._values);
			
			//Add some props to the target element
			this._target.css({
				"border-style": "solid",
				"border-width": "1px"
			});
			this._title = $("<div>", {
				width: "100%",
				height: "30px"
			}).append($("<span>").html(this._titleString));
			
			this._content = $("<div>", {
				width: "100%"
			}).html(HTMLContent); 
			this._target.append(this._content);
		}
	};
};