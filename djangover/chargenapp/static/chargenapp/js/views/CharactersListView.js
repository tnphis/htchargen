//utility datatable view

var CharactersListView = Backbone.View.extend({
	//el: $("#viewcontainer"),
	initialize : function(options) {
		this.options = options || {} //why not??
		var that = this

		require([
			'views/views.comp.min',
			'collections/collections.comp.min',
		], function(views, collections) {
			var CharactersList = collections.CharactersList()
			var charactersList = new CharactersList()

			var DatatableView = views.DataTableView()
			that.characters_table = new DatatableView({
				collection: charactersList,
				datatableparams : {
					aoColumns : [
						//{'sTitle': '', 'collection_id' : 'id', 'sWidth': '30px'}, //id
						{'sTitle': 'Name', 'sWidth' : '150px', 'collection_id' : 'name'},
						{'sTitle': 'Level', 'sWidth' : '50px', 'collection_id' : 'level'},
						{'sTitle': 'Gender', 'sWidth' : '75px', 'collection_id' : 'gender'},
						{'sTitle': 'Race', 'sWidth' : '75px', 'collection_id' : 'race'},
						{'sTitle': 'Background', 'sWidth' : '75px', 'collection_id' : 'social_background'},
						{'sTitle': 'Wealth', 'sWidth' : '75px', 'collection_id' : 'wealth'},
						{'sTitle': 'Points', 'sWidth' : '50px', 'collection_id' : 'point_pool'},
						{'sTitle': '', 'collection_id' : 'id', 'sWidth': '30px'} //put delete button here
					],
					fnRowCallback : function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
						$(nRow).click(function() {
							Backbone.history.navigate('app/client/edit_character/' + aData[7], {trigger: true})
						}).css({'cursor' : 'pointer'}).addClass('chargenapp-list-row')
						
						$(nRow).find('td:eq(7)').html('').append($('<button>')						
							.addClass('chargenapp-btn')
							.html('-')
							.attr('title', 'Delete this character')
							.click(function(e) {
								e.stopPropagation()
								if (confirm('Confirm the utter and irreversible destruction of ' + aData[0])) {
									//hmm.
									that.characters_table.options.collection.get(aData[7]).destroy({
										success: function(model, response) {
											if (response.success) {
												alert('Character destroyed')
											} else {
												alert('Error: ' + response.error_desc)
											}
											that.characters_table.refresh()
										},
										error: function(model, response) {
											alert('Unhandled server error!')
											that.characters_table.refresh()
										}
									})
								}
							})
						)
					}
				},
				additional_buttons: [
					{
						'id': 'add',
						'html': '<i class="glyphicon glyphicon-plus"></i>',
						'class': 'btn btn-primary',
						'title': 'Add',
						'click': function(e, that) {
							Backbone.history.navigate('app/client/edit_character/-1', {trigger: true})
						}
					}
				]
			})
		})
	},
	tagName: 'div',
	events: {
	},
	render: function(){
		var that = this
		require([
			'text',
			'text!' + Global.config.staticdir + '/templates/characters_list.html'
		], function(text, characterslistTemplate) {
			that.$el.html(characterslistTemplate)
			console.log(that)
			that.characters_table.render()
			that.characters_table.refresh()
			that.$el.find('#char_view_datatable').html(that.characters_table.el)
		});
	}
});

return CharactersListView;
