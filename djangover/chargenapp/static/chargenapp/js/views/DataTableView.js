//utility datatable view

var DataTableView = Backbone.View.extend({
	//el: $("#viewcontainer"),
	initialize : function(options) {
		this.options = options || {} //why not??
	},
	tagName: 'div',
	events: {
		'click #dt_btn_refresh' : 'refresh'
	},
	render: function(){
		var that = this
		require([
			'datatables',
			'text',
			'text!' + Global.config.staticdir + '/templates/datatable.html'
		], function(datatables, text, datatableTemplate) {
			if (!Global.templates['datatable']) {
				Global.templates['datatable'] = _.template(datatableTemplate)
			}
			that.template = Global.templates['datatable']

			//defaults
			that.options.dtsettings = {}
			that.options.per_page_options =[{'id' : 10, 'text' : 10},
				{'id' : 15, 'text' : 15},
				{'id' : 20, 'text' : 20},
				{'id' : 25, 'text' : 25},
				{'id' : 30, 'text' : 30},
				{'id' : 35, 'text' : 35},
				{'id' : 50, 'text' : 50},
				{'id' : 75, 'text' : 75},
				{'id' : 100, 'text' : 100},
				{'id' : 200, 'text' : 200}
			]

			that.options.sInfo = that.getsInfo()

			var datatableparams = {
				'sDom': 'Trt',
				'oTableTools': {
					'aButtons' : []
				},
				'bStateSave' : true,
				'oLanguage': {
					'sZeroRecords': "..."
				},
				'fnDrawCallback' : function(oSettings) {
					if (that.options.datatable) {
						that.options.dtsettings = that.options.datatable.fnSettings()
						if (that.data_was_loaded) {
							that.options.sInfo = that.getsInfo()
						}
						//scope.setButtonStates()
						if (that.options.customDrawCallback) {
							that.options.customDrawCallback(oSettings)
						}
					}
				}
			}

			that.$el.html(that.template(that.options))

			if (!that.options.datatable) {
				that.options.datatable = that.$el.find('#maintable').dataTable(
					$.extend(datatableparams, that.options.datatableparams)
				)
			}

			//additional button events
			if (that.options.additional_buttons) {
				for (var i=0, len=that.options.additional_buttons.length; i<len; i++) {
					var current_btn = that.options.additional_buttons[i]
					console.log(current_btn)
					if (current_btn.click) {
						that.$el.find('#dt_additional_btn_' + current_btn.id).unbind('click')
						that.$el.find('#dt_additional_btn_' + current_btn.id).bind('click', function(e) {
							current_btn.click(e, that)
						})
					}
				}
			}

			//synchronize possible refresh call
			return that
			//var apps = new models();
			// var appListView = new AppListView({ collection: apps});
			// appListView.render();
		});
	},
	getsInfo: function() {
		if (this.options.dtsettings && this.options.dtsettings._iDisplayEnd > 0) {
			return 'Displaying entries ' + (this.options.dtsettings._iDisplayStart + 1) + ' to ' + this.options.dtsettings._iDisplayEnd + ' out of ' + this.options.fnRecordsDisplay();
		} else {
			return 'No data to display'
		}
	},
	refresh: function() {
		if (this.options.beforerefresh) {
			this.options.beforerefresh()
		}

		this.options.sInfo = 'Loading data...'
		this.options.disablePrevPage = true
		this.options.disableNextPage = true

		var that = this
		this.options.collection.fetch({
			success: function(collection, response, options) {
				that.redraw()
				that.data_was_loaded = true
				that.options.sInfo = that.getsInfo()
				if (that.options.afterrefresh) {
					that.options.afterrefresh()
				}
			}
		})
	},
	redraw: function() {
		var that = this
		require(['datatables'], function() {
			var collection_data = that.options.collection.map(function(model) {
				var ordered_array = []
				for (var i=0, len = that.options.datatableparams.aoColumns.length; i<len; i++) {
					var thiscol = that.options.datatableparams.aoColumns[i]
					console.log(thiscol)
					console.log(model)
					ordered_array.push(model.get(thiscol.collection_id))
				}
				console.log(ordered_array)
				return ordered_array
			})
			that.options.datatable.fnClearTable()
			if (collection_data.length > 0) {
				that.options.datatable.fnAddData(collection_data)
			}
		})
	}
});

return DataTableView;
