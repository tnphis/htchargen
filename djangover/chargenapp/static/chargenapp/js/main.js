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
	staticdir : '/static/chargenapp/'
}

require.config({
	paths: {
		'jquery': '/static/lib/jquery-1.11.3.min',
		'underscore': '/static/lib/underscore-min',
		'backbone': '/static/lib/backbone-min',
		'text': '/static/lib/text',
		'datatables': '/static/lib/datatables/js/jquery.dataTables.min',
		'bootstrap': '/static/lib/bootstrap/js/bootstrap.min',
		'backbone_stickit': '/static/lib/backbone.stickit.min',
		'jqform': '/static/lib/jquery.form.min'
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
