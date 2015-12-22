//This module is really just creates a jQuery UI menu widget
grapher.listSelection = grapher.listSelection || function(target, list, eventCallback, context) {
	this._target = target;
	this._list = list;
	this._container = undefined;
	this._context = context;
	
	this.create = function() {
		this._container = $("<div>", {
			width: 500,
			height: "100%"
		});
		this._target.append(this._container);
		$(this._container).menu();
		//We have to add our own custom attributes to avoid a mess parsing the DOM looking for them later
		for (var k = 0, n = this._list.length; k < n; k++) {
			$("<li grapherValue = " + this._list[k] + " grapherItemID = " + k + "> " + this._list[k] + 
				"<ul><li>Append to search</li><li>Delete</li></ul></li>").appendTo(this._container);
		}
		$(this._container).menu("refresh");
		$(this._container).on("menuselect", function() {
			eventCallback.apply(context, arguments);
		});
		
	};
};