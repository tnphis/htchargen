// Filename: App.js
"use strict";

define([
	'jquery',
	'underscore',
	'backbone',
	'bootstrap',
	'AppRouter',
], function($, _, Backbone, dummybs, AppRouter){
  var initialize = function() {

    AppRouter.initialize();
    // new HomeView;
    // console.log('ztot');
  };

  return {
    initialize: initialize
  };
});
