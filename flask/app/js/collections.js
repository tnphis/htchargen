define(['jquery', 'underscore', 'backbone', 'models.min'], function($, _, Backbone, models) {
	"use strict";
	return {
		CharactersList : Backbone.Collection.extend({
			model: models.CharacterListItem,
			url: function() {
				return '/api?get_characters_list=true';
			},
			parse: function(resp, xhr) {
				return resp.data
			}
		})
	}
});
