## Introduction
This is a simple utility that graphs either two dimensional or three dimensional functions.

Raphael is used to provide the needed SVG functionality. [(http://raphaeljs.com/)](http://raphaeljs.com/)

Three.js is used to provide the needed WebGL functionality. [(https://http://threejs.org/)](http://threejs.org/)

The needed dependecies for building the client-side project are brought in through node.js.


## Building the back-end 

#### Linux 

**Note: You will likely need root privileges to install the following software. **

###### Python


The back-end is built on python 3.4. It is best if you were to use pip3 to bring in the needed dependecies.

All examples will be shown for the Ubuntu distribution, other distributions should also provide these packages.

First, you need to install pip3:
	
	$ sudo apt-get install python3-pip
	
Then use pip to install sympy:

	$ sudo pip3 install sympy
	
Install pymongo, the mongodb driver:
	
	$ sudo pip3 install pymongo

###### Mongodb

You need to install MongoDB 2.6 You can find instructions on how to do so [here](https://docs.mongodb.org/v2.6/tutorial/install-mongodb-on-ubuntu/).

Another very useful utility for MongoDB is [Robomongo](http://robomongo.org/)


## Building the front-end project


#### Linux and Mac
**You will likely need root privileges to install the following software. **

-Note that your distribution will likely provide node.js and git through its package manager.

You first need to install node.js on you machine. [(https://nodejs.org/)](https://nodejs.org/).

Followed by git [(http://git-scm.com/)](http://git-scm.com/).

Next, you need to install grunt:

	$ npm install -g grunt-cli
	
Change directory to /front-end, which is the root of the project.

Simply run:

	$ npm install
This will install the needed plugins. 

Type:

	$ grunt
	
This will run JSHint and then concatenate the Javascript and css sources to the dist/(js or css)/readable folders.

That's all! You now have the unminified sources in the dist folder!

#### Windows
First install the nodejs installer [(https://nodejs.org/)](https://nodejs.org/download/).

Followed by git [(http://git-scm.com/)](http://git-scm.com/).

Open up your command prompt.

Next, you need to install grunt:

	$ npm install -g grunt-cli

Change directory to development, which is the root of the project.

Simply run:

	$ npm install

Then you might need to run:

	$ npm install grunt

Finally, type:

	$ grunt
	
This will run JSHint and then concatenate the Javascript and css sources to the dist/(js or css)/readable folders.

That's all! You now have the unminified sources in the dist folder!



## Other grunt options
As previously stated, the default grunt task runs JSHint, and a concatenation of JS and CSS.
However, you may chose to run other tasks, or individual tasks.


#### Debug build
The debug build is the default choice when the user simply runs "grunt". The difference between production and debug besides
minification is that debug allows debugger statements in the code while production does not.

	$ grunt 
	
or

	$ grunt debug

#### Production build
The production build runs JSHint and minifies grapher.js into grapher-min.js which is then placed in dist/js/min.
It depends on /dist/js/readable/grapher.js existing (created by debug build), and it does not allow debugger statements.

	$ grunt build
	
#### JSHint
If you simply wish to run JSHint on the source files:

	$ grunt jshint
	
#### Minification
You may chose to only run minification, but it does depend on the debug build

	$ grunt uglify
	
#### Documentation
To run the automatic documentation creator:

	$ grunt doc
	
Simply use your favorite web browser to view doc/index.html


## Note to developers
* Do not submit anything from the /dist or /doc folders into the repo. These items should only exist on your local machine.
* Always build using grunt, or at least run JSHint over the code before making a submission.
* Use tabs in your text editor.