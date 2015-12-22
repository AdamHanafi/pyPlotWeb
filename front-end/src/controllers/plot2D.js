grapher.plot2D = grapher.plot2D || function(target, grid, plots, updateHandler) {
	this._grid = grid;
	this._plots = plots;
	this._paper = undefined;
	this._target = target;
	this.updateHandler = updateHandler;
	this._parent = undefined;
	this._title = undefined;
	
	this._createGrid = function() {
		for (var k = 0, n = this._grid.length; k < n; k++) {
			this._paper.path(this._grid[k].path).attr(this._grid[k].attr);
		}
	};
	
	this._createPlots = function() {
		for (var k = 0, n = this._plots.length; k < n; k++) {
			this._paper.path(this._plots[k].path).attr(this._plots[k].attr);
		}
	};
	
	this.updateControl = function(arg) {
		this._plots = arg.plot2D.plots;
		this._grid = arg.plot2D.grid;
		this._destroyGraph();
		this.plot();
	};
	
	this._destroyGraph = function() {
		this._target.empty();
	};
	
	this._updateOptions = function(e) {
		var options = {
			rangeObj: {
				xMin: parseInt(this._xMinBox.val()),
				xMax: parseInt(this._xMaxBox.val()),
				yMin: parseInt(this._yMinBox.val()),
				yMax: parseInt(this._yMaxBox.val())
			}
		};
		this.updateHandler("2dplot", options, this.updateControl, this);
	};
	
	this._setupControls = function() {
		this._controlContainer = $("<div>",{
			width: 200,
			height: 550
		}).css({
			float: "right"
		});
		this._xMinBox = $("<input>", {
			type: "text",
			placeholder: "X Min"
		});
		this._xMaxBox = $("<input>", {
			type: "text",
			placeholder: "X Max"
		});
		this._yMinBox = $("<input>", {
			type: "text",
			placeholder: "Y Min"
		});
		this._yMaxBox = $("<input>", {
			type: "text",
			placeholder: "Y Max"
		});
		this._submitButton = $("<input>", {
			type: "button",
			value: "Update"
		});
		this._target.append(this._controlContainer);
		this._controlContainer.append(this._xMinBox);
		this._controlContainer.append(this._xMaxBox);
		this._controlContainer.append(this._yMinBox);
		this._controlContainer.append(this._yMaxBox);
		this._controlContainer.append(this._submitButton);
		this._submitButton.on("click", $.proxy(this._updateOptions, this));
	};
	
	
	this.plot = function() {
		//Add some props to the target element
		this._target.css({
			"border-style": "solid",
			"border-width": "1px"
		});
		
		//Set up the canvas and its container
		this._parent = $("<div>", {
			width: "500px",
			height: "500px"

		}).css({
			position: "absolute"
		});
		this._title = $("<div>", {
			width: "500px",
			height: "50px"
		}).html("2D Plot");
		
		this._target.append(this._title);
		this._target.append(this._parent);
		this._paper = Raphael(this._parent[0], 0, 0);
		this._paper.setSize(this._parent.width(), this._parent.height());
		//First create the grid
		this._createGrid();
		//Next, add the plots
		this._createPlots();
		//Create the controls
		this._setupControls();
	};
};