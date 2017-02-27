// Filename: routes/AppRouter.js

define([
	'jquery',
	'underscore',
	'backbone',
	'bootstrap',
	'views/views.comp.min'
], function($, _, Backbone, dummybs, Views) {
	var AppRouter = Backbone.Router.extend({
		routes: {
			'app/client/login': 'showLogin',
			'app/client/characters' : 'showCharactersList',
			'app/client/edit_character' : 'newCharacterObject',
			'app/client/edit_character/:id' : 'showCharacterObject', //ah, let's just do it the boring way...
			// Default route
			'*actions': 'default'
		}
	});

	var check_user_credentials = function(route, callback) {
		if (!Global.user.id && route != 'app/client/login') {
			$.ajax({
				url: '/app/auth?get_user_id=true',
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
						Backbone.history.navigate('app/client/login', {trigger : true})
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
						url: '/app/api?get_settings=true',
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
			var LoginView = Views.LoginView()
			var loginView = new LoginView()
			loginView.render()
			console.log(loginView)
			$('#viewcontainer').html(loginView.el)
		});

		appRouter.on('route:showCharactersList', function() {
			var CharactersListView = Views.CharactersListView()
			var characterslistview = new CharactersListView()
			characterslistview.render()
			$('#viewcontainer').html(characterslistview.el)

			var NavbarView = Views.NavbarView()
			var navbarview = new NavbarView({page_name : 'Characters list'})
			navbarview.render()
			$('#navbarcontainer').html(navbarview.el)
		})

		appRouter.on('route:showCharacterObject', function(id) {
			var CharacterView = Views.CharacterView()
			var characterview = new CharacterView({
				'character_id' : id
			})
			characterview.refresh()
			$('#viewcontainer').html(characterview.el)

			var NavbarView = Views.NavbarView()
			var navbarview = new NavbarView({page_name : 'Character view'})
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
					appRouter.navigate('app/client/characters', {trigger : true})
				} else {
					appRouter.navigate('app/client/login', {trigger : true})
				}
			})
		});

		Backbone.history.start({ pushState: true});
	};

	return {
		initialize: initialize
	};
});
