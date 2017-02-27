// Filename: main.js
"use strict";

var Global = {}

Global.user = {}
Global.settings = {
	//highly outrageous but convenient...
	client: {
		skill_groups: ['Combat skills', 'General skills', 'Infiltration skills', 'Technological skills'],
		feat_types: ['Acquired feats', 'Racial feats', 'Traits']
	}
}
Global.templates = {}
Global.config = {
	staticdir : '/app'
}

require.config({
	paths: {
		'jquery': '/app/lib/jquery-1.11.3.min',
		'underscore': '/app/lib/underscore-min',
		'backbone': '/app/lib/backbone-min',
		'text': '/app/lib/text',
		'datatables': '/app/lib/datatables/js/jquery.dataTables.min',
		'bootstrap': '/app/lib/bootstrap/js/bootstrap.min',
		'backbone_stickit': '/app/lib/backbone.stickit.min',
		'jqform': '/app/lib/jquery.form.min',
		'utils': '/app/js/util'
	},
	shim: {
		'underscore': {
			deps: ['jquery'],
		},
		'backbone': {
			deps: ['underscore']
		},
		'bootstrap': {
			deps: ['jquery']
		},
		'backbone_stickit': {
			deps: ['backbone']
		},
		'jqform': {
			deps: ['jquery']
		}
	},
	urlArgs: 'v=0.1'
});

require([
	'App'
	], function(App) {

		App.initialize();
	}
);
