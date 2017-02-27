// Filename: routes/AppRouter.js

define([
	'jquery',
	'underscore',
	'backbone',
	'bootstrap',
	'views.min'
], function($, _, Backbone, dummybs, views) {
	var AppRouter = Backbone.Router.extend({
		routes: {
			'client/login': 'showLogin',
			'client/characters' : 'showCharactersList',
			'client/edit_character' : 'newCharacterObject',
			'client/edit_character/:id' : 'showCharacterObject', //ah, let's just do it the boring way...
			// Default route
			'*actions': 'default'
		}
	});

	var check_user_credentials = function(route, callback) {
		if (!Global.user.id && route != 'client/login') {
			$.ajax({
				url: '/auth?get_user_id=true',
				method: 'get',
				dataType: 'json',
				success: function(data) {
					console.log(data)
					if (data.success) {
						Global.user.id = data.user_id
						Global.user.name = data.user_name
						if (callback) {
							callback()
						}
					} else {
						Backbone.history.navigate('client/login', {trigger : true})
					}
				}
			})
		} else {
			//if user has alaready been logged in, we still need to trigger stuff like loading settings.
			if (callback) {
				callback()
			}
		}
	}


	var initialize = function(){
		console.log('Router initialized');

		var appRouter = new AppRouter;

		appRouter.on('route', function(route, params) {
			console.log('route triggered')
			console.log(route, params)
			check_user_credentials(route, function() {
				console.log(Global.settings, Global.user)
				if (Global.user.id && !Global.settings.objects) {
					$.ajax({
						url: '/api?get_settings=true',
						method: 'get',
						dataType: 'json',
						success: function(data) {
							console.log(data)
							if (data.success) {
								Global.settings = $.extend(Global.settings, data.data)
								$(window).trigger('settings_loaded')
							} else {
								console.log('shit happened when getting settings!', data)
							}
						}
					})
				}
			})
		})

		appRouter.on('route:showLogin', function(){
			var loginView = new views.LoginView()
			loginView.render()
			console.log(loginView)
			$('#viewcontainer').html(loginView.el)
		});

		appRouter.on('route:showCharactersList', function() {
			var characterslistview = new views.CharactersListView()
			characterslistview.render()
			$('#viewcontainer').html(characterslistview.el)

			var navbarview = new views.NavbarView({page_name : 'Characters list'})
			navbarview.render()
			$('#navbarcontainer').html(navbarview.el)
		})

		appRouter.on('route:showCharacterObject', function(id) {
			var characterview = new views.CharacterView({
				'character_id' : id
			})
			console.log(characterview)
			characterview.refresh()
			$('#viewcontainer').html(characterview.el)

			var navbarview = new views.NavbarView({page_name : 'Character view'})
			navbarview.render()
			$('#navbarcontainer').html(navbarview.el)
		})

		appRouter.on('route:newCharacterObject', function(id) {
			appRouter.navigate('app/client/edit_character/-1', {trigger: true, replace: true})
		})

		appRouter.on('route:default', function (actions) {
			console.log('route:default triggered')
			check_user_credentials('default', function() {
				if (Global.user.id) {
					appRouter.navigate('client/characters', {trigger : true})
				} else {
					appRouter.navigate('client/login', {trigger : true})
				}
			})
		});

		Backbone.history.start({ pushState: true});
	};

	return {
		initialize: initialize
	};
});
