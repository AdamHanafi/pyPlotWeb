
module.exports = function(grunt) {

	grunt.initConfig({
		pkg: grunt.file.readJSON("package.json"),
		
		js: {
			//build destination
			dest: "dist/js/readable/grapher.js",
			//root of source folder
			src: "src",
			//libraries
			lib: [
				"lib/raphael-min.js",
				"lib/jquery.js",
				"src/utils.js"
			]
		},
		
		jshint: {
			options:{
				laxcomma: true,
				smarttabs: true,
				debug: true
			},
			all: [
				"src/*.js",
				"src/controllers/*.js"
			]
		},
		//JSHint for minification
		minjshint: {
			options:{
				laxcomma: true,
				smarttabs: true
			},
			all: [
				"src/*.js"
			]
		},
		
		jsdoc : {
			dist : {
				src: ["src/*.js", "../README.md"],
				options: {
					destination: "doc"
				}
			}
		},
		
		uglify: {
			compress: {
				hoist_funs: false,
				join_vars: false,
				loops: false,
				unused: false
			},
			beautify: {
				ascii_only: true
			},
			min: {
				files: {
					"dist/js/min/grapher-min.js": ["dist/js/readable/grapher.js"]
				}
			}
		},
		concat: {
			options: {
				separator: "\n;"
			},
			dist: {
				src: [
					"lib/raphael.js", 
					"lib/jquery.js",
					"lib/jquery-ui.js",
					"lib/three/three.js",
					"lib/three/OrbitControls.js",
					"lib/mathjax/MathJax.js",
					"lib/mathjax/TeX-AMS-MML_HTMLorMML-full.js",
					"lib/markdown/markdown.js",
					"lib/wijmo-wijgrid.js",
					"src/grapher.js",
					"src/model.js",
					"src/controllers/textArea.js",
					"src/controllers/plot2D.js",
					"src/controllers/plot3D.js",
					"src/controllers/listSelection.js",
					"src/controllers/table.js"
				],
				dest: "dist/js/readable/grapher.js"
			}
		},
		concatcss: {
			options: {
				separator: "\n;"
			},
			dist: {
				src: [
					"css/*.css"
				],
				dest: "dist/css/readable/style.css"
			}
		},
		copy: {
			main: {
				files: [
					{
						expand: true,
						flatten: true,
						src: ["css/images/*.png"],
						dest: "dist/css/readable/images"
					}
				]
			}
		}
	});
	
	//Load taks from plugins
	grunt.loadNpmTasks("grunt-contrib-uglify");
	grunt.loadNpmTasks("grunt-contrib-clean");
	grunt.loadNpmTasks("grunt-contrib-jshint");
	grunt.loadNpmTasks("grunt-contrib-concat");
	grunt.loadNpmTasks("grunt-contrib-jst");
	grunt.loadNpmTasks("grunt-contrib-copy");
	grunt.loadNpmTasks("grunt-jsdoc");
	
	//This is the default option for when you simply enter "grunt"
	grunt.registerTask("default", ["debug"]);
	
	grunt.registerTask("build", ["concat", "concatcss", "copy", "minjshint", "uglify"]);
	grunt.registerTask("debug", ["concat", "concatcss", "copy", "jshint"]); //TODO: make js the first task in the future
	grunt.registerTask('doc', ['jsdoc']);
	
	//This task just changes the arguments for the concat task and then runs it.
	grunt.registerTask("concatcss", function() {
		var task = grunt.config("concatcss");
		var src = task.dist.src;
		var dist = task.dist;
		var options = task.options;
		
		grunt.config.set("concat", {
			options: options,
			dist: dist
		})
		grunt.task.run("concat");
	});
	
	grunt.registerTask("minjshint", function() {
		var task = grunt.config("minjshint");
		var all = task.all;
		var options = task.options;
		
		grunt.config.set("jshint", {
			options: options,
			all: all
		})
		grunt.task.run("jshint");
	});
	
};