grapher.table= grapher.table || function(target, data, updateHandler) {
	this._target = target;
	this._title = undefined;
	this._content = undefined;
	this._data = data;
	this.updateHandler = updateHandler;
	
	this.updateControl = function(arg) {
		this._destroyTable();
		this._data = arg.table;
		this.create();
	};
	
	this._destroyTable = function() {
		this._target.empty();
	};
	
	this._updateOptions = function(e) {
		var options = {
			start: parseInt(this._startBox.val()),
			delta: parseInt(this._deltaBox.val())
		};
		this.updateHandler("table", options, this.updateControl, this);
	};
	
	this._setupControls = function() {
		this._controlContainer = $("<div>",{
			width: 200,
			height: 550
		}).css({
			float: "right"
		});
		this._startBox = $("<input>", {
			type: "text",
			placeholder: "Start Value"
		});
		this._deltaBox = $("<input>", {
			type: "text",
			placeholder: "Delta"
		});
		this._submitButton = $("<input>", {
			type: "button",
			value: "Update"
		});
		this._target.append(this._controlContainer);
		this._controlContainer.append(this._startBox);
		this._controlContainer.append(this._deltaBox);
		this._controlContainer.append(this._submitButton);
		this._submitButton.on("click", $.proxy(this._updateOptions, this));
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
		}).append($("<span>").html("Table"));
		this._target.append(this._title);
		
		this._content = $("<table>", {
			width: 600,
			height: 550
		});
		this._target.append(this._content);
		
		var cols = this._data.column;
		var data = this._data.data;
		//Create the wijgrid
		
		this._content.wijgrid({
			columns: cols,
			data: data,
			selectionMode: "none",
			scrollMode: "none",
			allowSorting: false
		});
		this._setupControls();
	};
};
