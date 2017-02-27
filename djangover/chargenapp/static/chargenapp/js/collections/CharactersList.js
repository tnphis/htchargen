var CharactersList = Backbone.Collection.extend({
	model: models.CharactersListItem(),
	url: function() {
		return '/app/api?get_characters_list=true';
	},
	parse: function(resp, xhr) {
		return resp.data
	}
})

return CharactersList;
