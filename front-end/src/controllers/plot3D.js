grapher.plot3D = grapher.plot3D || function(target, grid, plots, colors) {
	this._grid = grid;
	this._plots = plots;
	this._colors = colors;
	this._paper = undefined;
	this._renderer = undefined;
	this._camera = undefined;
	this._orthCamera = undefined;
	this._scene = undefined;
	this._light = undefined;
	this._light2 = undefined;
	
	this._gridObjs = [];
	
	this._target = target;
	this._parent = undefined;
	this._title = undefined;
	this._controls = undefined;
	
	this._requestID = undefined;
	this._controlContainer = undefined;
	this._cameraSwitch = undefined;
	this._activeCamera = "Perspective";
	this._currentActiveCam = undefined;
	
	this._createGrid = function() {
		var that = this;
		var lineMaterial = new THREE.LineDashedMaterial({
			color : this._grid.color,
			linewidth : this._grid.lineWidth
		});
		var currentVal, geometry, line;
		
		var createLine = function(val) {
			geometry = new THREE.Geometry();
			geometry.vertices.push(new THREE.Vector3(currentVal[0][0], currentVal[0][1], currentVal[0][2]));
			geometry.vertices.push(new THREE.Vector3(currentVal[1][0], currentVal[1][1], currentVal[1][2]));
			line = new THREE.Line(geometry, lineMaterial);
			that._gridObjs.push(line);
			that._scene.add(line);
			
		};
		//Create the X-Y grid.
		for (var k = 0, n = this._grid.xy.length; k < n; k++) {
			currentVal = this._grid.xy[k];
			createLine(currentVal);
		}
		//Create the Y-Z grid.
		for (k = 0, n = this._grid.yz.length; k < n; k++) {
			currentVal = this._grid.yz[k];
			createLine(currentVal);
		}
		//Create the X-Z grid.
		for (k = 0, n = this._grid.xz.length; k < n; k++) {
			currentVal = this._grid.xz[k];
			createLine(currentVal);
		}
	};
	
	this._createPlots = function() {
		var that = this, i = 0;
		
		var getMesh = function(x, y) {
			var z = 0;
			if (that._plots.vectors[0][i]) {
				z = that._plots.vectors[0][i][2];
			}
			i++;
			return new THREE.Vector3(x, y, z);
			
		};
		var normalize = function(val) {
			val = (val - that._plots.minMax[0][0].min) / (that._plots.minMax[0][0].max - that._plots.minMax[0][0].min);
			return val;
		};
		
		//Hard coded for red max, blue min
		var getColor = function(val) {
			var result = [];
			if (that._colors.max === "#FF0000") {
				//val = normalize(val);
				result.push(parseInt(val * 255));
			}
			result.push(0);
			if (that._colors.min === "#0000FF") {
				//val = normalize(val);
				result.push(parseInt( (1 - val) * 255));
			}
			return result;
		};
		
		var surface = new THREE.ParametricGeometry(getMesh, 100, 100);
		surface.computeBoundingBox();
		
		var material = new THREE.MeshPhongMaterial({shininess : 0, side : THREE.DoubleSide,  vertexColors: THREE.VertexColors})
		,	surfaceMesh = new THREE.Mesh(surface, material)
		,	faceIndices = ['a', 'b', 'c', 'd'];
		
		for (var k = 0; k < surface.faces.length; k++) 
		{
			var face = surface.faces[k];
			var numberOfSides = (face instanceof THREE.Face3) ? 3 : 4;
			for (var j = 0; j < numberOfSides; j++) 
			{
				var vertexIndex = face[faceIndices[j]];
				var vertexValue = surface.vertices[vertexIndex].z;
				var colorResult = getColor(vertexValue);
				var zMin = surface.boundingBox.min.z;
				var zMax = surface.boundingBox.max.z;
				var zRange = zMax - zMin;
				var val = (zMax - vertexValue) / zRange;
				face.vertexColors[j] = new THREE.Color(1 - val, 0, val);
			}
		}
		surfaceMesh.scale.x = 20;
		surfaceMesh.scale.y = 20;
		surfaceMesh.scale.z = 20;
		this._scene.add(surfaceMesh);
		
	};
	
	this._setupWebGL = function() {
		this._renderer = new THREE.WebGLRenderer({antialias : true});
		this._renderer.setSize(this._parent.width(), this._parent.height());
		this._parent.append(this._renderer.domElement);
		this._renderer.setClearColor( 0xffffff, 1);
		
		this._scene = new THREE.Scene();
		this._camera = new THREE.PerspectiveCamera(75, this._parent.width() / this._parent.height(), 0.01, 10000);
		
		this._light = new THREE.AmbientLight(0xFFFFFF);
		this._scene.add(this._light);
		this._light.position.set(0, 0, 30);
		
		this._controls = new THREE.OrbitControls(this._camera, this._parent[0]);
		this._camera.position.x = 10;
		this._camera.position.y = 10;
		this._camera.position.z = 50;
		this._camera.updateProjectionMatrix();
		this._currentActiveCam = this._camera;
		
		//Create the orthographic camera
		this._orthCamera = new THREE.OrthographicCamera(-15, 15, -15, 15, 1, 100000);
		this._orthCamera.position.x = 5;
		this._orthCamera.position.y = 5;
		this._orthCamera.position.z = 50000;
		this._orthCamera.up.y = 0;
		this._orthCamera.up.x = -1;
		this._orthCamera.up.z = 0;
		this._orthCamera.lookAt(new THREE.Vector3(5, 5, 0));
		
		this._render();
	};
	
	this._render = function(arg) {
		this._requestID = requestAnimationFrame(this._render.bind(this));
		this._renderer.render(this._scene, this._currentActiveCam);
	};
	
	this._switchCamera = function(e) {
		if (this._activeCamera === "Perspective") {
			this._cameraSwitch.attr("value" ,"Perspective Camera");
			this._activeCamera = "Orthographic";
			this._currentActiveCam = this._orthCamera;
		}
		else {
			this._cameraSwitch.attr("value" ,"Orthographic Camera");
			this._activeCamera = "Perspective";
			this._currentActiveCam = this._camera;
		}
	};
	
	this._setupControls = function() {
		this._controlContainer = $("<div>",{
			width: 200,
			height: 550
		}).css({
			float: "right"
		});
		
		this._target.append(this._controlContainer);
		this._cameraSwitch = $("<input>",{
			type: "button",
			value:  "Orthographic Camera"
		});
		this._controlContainer.append(this._cameraSwitch);
		this._cameraSwitch.on("click", $.proxy(this._switchCamera, this));
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
		}).html("3D Plot");
		
		this._target.append(this._title);
		this._target.append(this._parent);
		
		this._setupWebGL();
		//First create the grid
		this._createGrid();
		//Next, add the plots
		this._createPlots();
		//Finally, create the control container
		this._setupControls();
	};
	
	
};