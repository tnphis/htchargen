define(['jquery', 'underscore', 'backbone', 'models.min', 'collections.min'], function($, _, Backbone, models, collections) {
	"use strict";
	//self-referencing requires a slight modification of the syntax
	var views = {
		//utility datatable view
		DataTableView : Backbone.View.extend({
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
		}),
		//utility skillbar view options: id, value, min, max, [cap]
		SkillBarView : Backbone.View.extend({
			//el: $("#viewcontainer"),
			initialize : function(options) {
				this.options = options || {} //why not??
				if (this.options.cap === undefined) {
					this.options.cap = this.options.max
				}
			},
			tagName: 'span',
			events: {
				'click #btn_increase' : 'increase_value', //using ids won't work, it's called before initialize!
				'click #btn_decrease' : 'decrease_value'
			},
			drawboxes: function() {
				var boxesel = this.$el.find('#' + this.options.id + '_boxes')
				var value_txt = ''
				for (var i = 0; i < this.options.value; i++) {
					value_txt += '&rtrif;'//'&FilledSmallSquare;'
				}
				for (var i = 0; i < this.options.cap - this.options.value; i++) {
					value_txt += '&rtri;'//'&EmptySmallSquare;'
				}

				for (var i = 0; i < this.options.max - this.options.cap; i++) {
					value_txt += '<span class="skillbar-grayed">&rtri;</span>'//'&EmptySmallSquare;'
				}

				boxesel.html(value_txt)

				if (this.options.value >= this.options.cap) {
					this.$el.find('#btn_increase').attr('disabled', 'true')
				} else {
					this.$el.find('#btn_increase').removeAttr('disabled')
				}
				if (this.options.value <= this.options.min) {
					this.$el.find('#btn_decrease').attr('disabled', 'true')
				} else {
					this.$el.find('#btn_decrease').removeAttr('disabled')
				}
			},
			render: function(){
				var that = this
				require([
					'text',
					'text!' + Global.config.staticdir + '/templates/skillbar.html'
				], function(text, skillbarTemplate) {
					if (!Global.templates['skillbar']) {
						Global.templates['skillbar'] = _.template(skillbarTemplate)
					}
					that.template = Global.templates['skillbar']
					that.$el.html(that.template(that.options))

					that.inputel = that.$el.find('input')
					that.inputel.val(that.options.value)

					that.drawboxes()

					if (that.options.afterdraw) {
						//console.log(that)
						that.options.afterdraw(that)
					}
				});
			},
			increase_value : function() {
				if (this.options.value < this.options.cap) {
					this.options.value += 1
					this.drawboxes()
					this.inputel.val(this.options.value)
					this.inputel.trigger('change')
				}
			},
			decrease_value : function() {
				if (this.options.value > this.options.min) {
					this.options.value -= 1
					this.drawboxes()
					//console.log(this.options.value)
					this.inputel.val(this.options.value)
					this.inputel.trigger('change')
				}
			}/*,
			get_inputel : function() {
				if (!this.inputel) {
					alert('smth is wrong with inputel')
				} else {
					return this.inputel
				}
			}*/
		}),
		//a non-model view to represent a user control panel navbar
		NavbarView : Backbone.View.extend({
			//el: $("#navbarcontainer"),
			tagName: 'div',
			initialize: function(options) {
				this.options = options || {}
			},
			events: {
				'click #MenuLogout': function() {
					if (confirm('Confirm user logout')) {
						$.ajax({
							url: '/auth?logout=true',
							method: 'get',
							dataType: 'json',
							success: function(data) {
								if (data.success) {
									Global.user = {}
									Backbone.history.navigate('app/client/login', {trigger : true})
								} else {
									alert('Something happened...')
								}
							},
							error: function() {
								alert('Something happened...')
							}
						})
					}
				},
				'click #MenuChangepasswd': function() {
					this.$el.find('#PasswdChangeModalForm').modal('show')
				},
				'keyup #old_passwd': 'validate_form',
				'keyup #new_passwd': 'validate_form',
				'keyup #confirm_passwd': 'validate_form',
				'click #BtnChangePasswdRequest': function() {
					var old_passwd = this.$el.find('#old_passwd').val()
					var new_passwd = this.$el.find('#new_passwd').val()
					var confirm_passwd = this.$el.find('#confirm_passwd').val()

					if (new_passwd == confirm_passwd) {
						$.ajax({
							url: '/auth?change_passwd=true&old_passwd=' + old_passwd + '&new_passwd=' + new_passwd,
							method: 'get',
							dataType: 'json',
							success: function(data) {
								if (data.success) {
									alert('Password changed successfully')
									this.$el.find('#BtnChangePasswdRequest').modal('hide')
								} else {
									alert('Error: ' + data.error_desc)
								}
							},
							error: function() {
								alert('Unhandled server error')
							}
						})
					} else {
						alert('The new password doesn\'t match its confirmation value.')
					}
				}
			},
			validate_form: function() {
				//don't want to use a basic form submit, do a simple manual validation
				if (!this.$el.find('#old_passwd').val() || !this.$el.find('#new_passwd').val() || !this.$el.find('#confirm_passwd').val()) {
					this.$el.find('BtnChangePasswdRequest').attr('disabled', 'true')
				} else {
					this.$el.find('#BtnChangePasswdRequest').removeAttr('disabled')
				}
			},
			render: function(){
				var that = this
				require([
					'text',
					'text!' + Global.config.staticdir + '/templates/navbar.html'
				], function(text, navbarTemplate) {
					that.$el.html(navbarTemplate)
					if (that.options.page_name) {
						that.$el.find('#CurrentPageName').html(that.options.page_name)
					} else {
						that.$el.find('#CurrentPageName').html('Random unnamed page')
					}
					that.$el.find('#CurrentUserName').html(Global.user.name)
					console.log(Global.user.name)

					return that
				});
			}
		}),
		LoginView : Backbone.View.extend({
			//el: $("#viewcontainer"),
			tagName: 'div',
			events: {
				'click #btn_login' : 'login_user',
				'click #btn_register' : 'register_user',
				'keyup input' : 'check_button_status',
			},
			render: function(){
				var that = this
				require([
					'text',
					'text!' + Global.config.staticdir + '/templates/login.html'
				], function(text, loginTemplate) {
					that.$el.html(loginTemplate);
					that.check_button_status()

					//var apps = new models();
					// var appListView = new AppListView({ collection: apps});
					// appListView.render();
				});
			},
			check_button_status: function(e) {
				var that = this
				require(['utils'], function(utils) {
					var login = that.$el.find('#login').val()
					var passwd = that.$el.find('#passwd').val()
					var reglogin = that.$el.find('#reglogin').val()
					var regemail = that.$el.find('#regemail').val()
					var login_btn = that.$el.find('#btn_login')
					var register_btn = that.$el.find('#btn_register')

					if (!(login) || !(passwd)) {
						login_btn.attr('disabled', 'true')
					} else {
						login_btn.removeAttr('disabled')

						//enter submission handling
						if (e.which == 13) {
							that.login_user()
						}
					}

					if (!(reglogin) || !(utils.validate_email(regemail))) {
						register_btn.attr('disabled', 'true')
					} else {
						register_btn.removeAttr('disabled')

						//enter submission handling
						if (e.which == 13) {
							that.register_user()
						}
					}
				})
			},
			login_user: function() {
				var login = this.$el.find('#login').val()
				var passwd = this.$el.find('#passwd').val()
				$.ajax({
					url: '/auth?login=true&user_name=' + login + '&user_passwd=' + passwd,
					method: 'get',
					dataType: 'json',
					success: function(data) {
						if (data.success) {
							Global.user.id = data.user_id
							Backbone.history.navigate('client/characters', {trigger: true})
						} else {
							alert('Login unsuccessful...')
						}
					}
				})
			},
			register_user: function() {
				var login = this.$el.find('#reglogin').val()
				var email = this.$el.find('#regemail').val()
				$.ajax({
					url: '/auth?register=true&user_name=' + login + '&user_email=' + email,
					method: 'get',
					dataType: 'json',
					success: function(data) {
						if (data.success) {
							$('#RegistrationFormTitle').html('Registration successful')
							$('#RegistrationFormContent').html('Your new password is <b>' + data.passwd + '</b>')
							$('#RegistrationModalForm').modal('show')
						} else {
							$('#RegistrationFormTitle').html('Registration unsuccessful')
							if (data.error_desc) {
								$('#RegistrationFormContent').html(data.error_desc)
							} else {
								$('#RegistrationFormContent').html('Unknown error')
							}
							$('#RegistrationModalForm').modal('show')
						}
					}
				})
			}
		}),
		CharactersListView : Backbone.View.extend({
			//el: $("#viewcontainer"),
			initialize : function(options) {
				this.options = options || {} //why not??
				var that = this

				require([
					'collections.min'
				], function(collections) {
					var charactersList = new collections.CharactersList()

					that.characters_table = new views.DataTableView({
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
									Backbone.history.navigate('client/edit_character/' + aData[7], {trigger: true})
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
									Backbone.history.navigate('client/edit_character/-1', {trigger: true})
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
		}),
		CharacterView : Backbone.View.extend({
			//el: $("#viewcontainer"),
			initialize : function(options) {
				this.options = options || {} //why not??

				console.log('prolly true', Global.settings.objects)
				if ((!Global.settings.objects) && !Global.char_settings_event_set) {
					var that = this
					$(window).on('settings_loaded', function() {
						that.options.select_options = Global.settings.objects
						console.log('wtf is wrong with the settings', Global.settings)
						that.options.skill_groups = Global.settings.client.skill_groups //duh!
						that.options.feat_types = Global.settings.client.feat_types //duh!
					})

					Global.char_settings_event_set = true
				} else {
					this.options.select_options = Global.settings.objects
					this.options.skill_groups = Global.settings.client.skill_groups //duh redux!
					this.options.feat_types = Global.settings.client.feat_types //duh redux!
				}

				var that = this
				require([
					'backbone_stickit',
					'jqform'
				], function() {
					that.options.model = new models.Character({
						id : that.options.character_id
					}).on('sync', function(model) {
						that.model_just_synced = true
						that.options.model_backup = model.clone()
						console.log('sync', that.options.model_backup)
						that.render(function() {
							that.$el.find('#btn_cancel').attr('disabled', true)
							that.$el.find('#btn_save').attr('disabled', true)
							//Don't forget the character name placeholder!
							that.$el.find('#char_name_placeholder').removeClass('hidden').addClass(that.options.get_name_class('placeholder'))
							that.$el.find('#real_char_name').removeClass('hidden').addClass(that.options.get_name_class('real_name'))
							//Attribute min boundaries
							if (model.id != -1) {
								for (var i = 0, len = that.options.model_backup.get('attributes').length; i < len; i++) {
									var current_attr = that.options.model_backup.get('attributes')[i]
									that.$el.find('#attribute_' + i).attr('min', current_attr.value)
								}
							}
						})
					}).on('change', function(model) {
						if (that.model_just_synced) {
							console.log('removing disabled')
							that.$el.find('#btn_cancel').removeAttr('disabled')
							that.$el.find('#btn_save').removeAttr('disabled')

							if (that.options.model.get('level') == Global.settings.level_cap) {
								that.$el.find('#btn_levelup').attr('disabled', true)
							}

							that.model_just_synced = false
						}
					}).on('custom_error', function(msg) {
						that.render()
						if (msg)  {
							alert('Error: ' + msg)
						} else {
							alert('Unknown error')
						}
					})

					that.options.get_name_class = function(what) {
						if ((what == 'real_name' && !that.options.model.get('name')) || (what == 'placeholder' && that.options.model.get('name'))) {
							return 'hidden'
						} else {
							return ''
						}
					}

					console.log('model initialized')
				})
			},
			tagName: 'div',
			events: {
				'change .bound_attr': function(e) {
					var attr_index = Number($(e.target).attr('id').substr(10))
					var attrs = $.extend(true, [], this.options.model.get('attributes'))
					attrs[attr_index].value = $(e.target).val()
					this.options.model.set('attributes', attrs)
					//redraw the skills to identify new caps
					this.drawskills()
				},
				'click #char_name_placeholder': function(e) {
					$(e.target).addClass('hidden')
					this.$el.find('#char_name_input').removeClass('hidden').focus()
				},
				'click #real_char_name': function(e) { //repetitive but whatever
					$(e.target).addClass('hidden')
					this.$el.find('#char_name_input').removeClass('hidden').focus()
				},
				'click #btn_go_back': function() {
					Backbone.history.navigate('client/characters', {trigger: true})
				},
				'click #btn_delete': function() {
					if (confirm('Confirm the utter and irreversible destruction of ' + this.options.model.get('name'))) {
						this.options.model.destroy({
							success: function(model, response) {
								if (response.success) {
									alert('Character destroyed. Redirecting the characters list.')
									Backbone.history.navigate('client/characters', {trigger: true})
								} else {
									alert('Error: ' + response.error_desc)
								}
							},
							error: function(model, response) {
								alert('Unhandled server error!')
							}
						})
					}
				},
				'blur #char_name_input': function(e) {
					$(e.target).addClass('hidden')
					this.$el.find('#char_name_placeholder').removeClass('hidden').addClass(this.options.get_name_class('placeholder'))
					this.$el.find('#real_char_name').removeClass('hidden').addClass(this.options.get_name_class('real_name')).html(this.options.model.get('name'))
					console.log(this.options.get_name_class('placeholder'), this.options.get_name_class('real_name'))
				},
				'click #btn_refresh': function() {
					this.options.model.fetch()
				},
				'click #btn_cancel': function() {
					console.log('btn_cancel clicked')
					console.log('cancel', this.options.model_backup)
					if (this.options.model_backup) {
						this.options.model = this.options.model_backup.clone()
					}
					var that = this
					this.render(function() {
						that.$el.find('#btn_cancel').attr('disabled', true)
						that.$el.find('#btn_save').attr('disabled', true)
						that.model_just_synced = true
					})
				},
				'click #btn_save': function() {
					if (this.options.model.isValid()) {
						console.log('model is valid!')
						this.options.model.save(this.options.model.attributes, {
							success: function(model, response) {
								if (response.success) {
									Backbone.history.navigate('client/edit_character/' + response.data.id, {trigger: true})
								} else {
									alert('Error: ' + response.error_desc)
								}
							},
							error: function(model, response) {
								alert('Unhandled server error!')
							}
						})
					} else {
						alert('Required fields not filled: ' + this.options.model.validationError.join(', '))
					}
				},
				'click #btn_create': function() {
					if (!this.model_just_synced) {
						if (confirm('Confirm creating a new character. Any changes you have made will be lost')) {
							Backbone.history.navigate('client/edit_character/-1', {trigger: true})
						}
					} else {
						Backbone.history.navigate('client/edit_character/-1', {trigger: true})
					}
				},
				'click #btn_levelup': function() {
					if (this.options.model.id == -1) {
						alert('The character doesn\'t exist it! Save before leveling up.')
					} else {
						var confirmation_msg = 'Confirm level up. The procedure is irreversible.'
						if (!this.model_just_synced) {
							confirmation_msg += ' Any unsaved changes you have made will be lost.'
						}

						if (confirm(confirmation_msg)) {
							var that = this
							$.ajax({
								url: '/api?levelup=true&character_id=' + this.options.model.id,
								method: 'post',
								dataType: 'json',
								success: function(data) {
									if (data.success) {
										that.options.model.fetch()
										console.log(that.options.model.get('level'))
									} else {
										alert('Error: ' + data.error_desc)
									}
								},
								error: function() {
									alert('Unhandled server error')
								}
							})
						}
					}
				},
				'mouseover #PortraitPanel': function(e) {
					$(e.target).find('#PortraitForm').removeClass('hidden')
					$(e.target).find('#BtnDeletePortrait').removeClass('hidden')
					$(e.target).find('img').addClass('chargenapp-portrait-sm')
				},
				'mouseleave #PortraitPanel': function(e) {
					$(e.target).find('#PortraitForm').addClass('hidden')
					$(e.target).find('#BtnDeletePortrait').addClass('hidden')
					$(e.target).find('img').removeClass('chargenapp-portrait-sm')
				},
				'click #BtnSelectFile': function() {
					this.$el.find('#portrait_file').trigger('click')
				},
				'change #portrait_file': function(e) {
					this.$el.find('#portrait_file_placeholder').val($(e.target).val())
				},
				'click #BtnPortraitFormSubmit': function() {
					console.log(this.portrait_form)
					this.portrait_form.submit()
				},
				'click #BtnDeletePortrait': function() {
					if (confirm('Confirm removal of the character\'s portrait')) {
						console.log('lalalalala')
						//this.$el.find('#portrait_file').val(null)
						console.log(this.portrait_form)
						this.portrait_form.clearForm()
						this.portrait_form.submit()
					}
				}
			},
			bindings: {
				'#points': 'points',
				'#wealth': 'wealth',
				'#level': 'level',
				'#char_name_input': 'name',
				'#race': {
					observe: 'race',
					selectOptions: {
						collection: 'this.options.select_options.races',
						labelPath: 'name',
						valuePath: 'id',
						defaultOption: {
							label: '',
							value: null
						}
					}
				},
				'#gender': {
					observe: 'gender',
					selectOptions: {
						collection: 'this.options.select_options.genders',
						labelPath: 'value',
						valuePath: 'id',
						defaultOption: {
							label: '',
							value: null
						}
					}
				},
				'#social_background': {
					observe: 'social_background',
					selectOptions: {
						collection: 'this.options.select_options.social_backgrounds',
						labelPath: 'value',
						valuePath: 'id',
						defaultOption: {
							label: '',
							value: null
						}
					}
				}
			},
			refresh : function() {
				//require is needed to make sure the model is initialized before refreshing
				var that = this
				require([
					'models.min',
					'backbone_stickit', //not sure why at the moment...
					'jqform' //actually, both need to be loaded for the init to work!
				], function() {
					that.options.model.fetch()
					//that.render() //handled in onsync
				})
			},
			render: function(callback){
				var that = this
				require([
					'text',
					'text!' + Global.config.staticdir + '/templates/character_view.html'
				], function(text, characterviewTemplate) {
					if (!Global.templates['character_view']) {
						Global.templates['character_view'] = _.template(characterviewTemplate)
					}
					that.template = Global.templates['character_view']

					that.$el.html(that.template(that.options))
					that.stickit(that.options.model)
					that.drawskills()

					//technically, keeping it as a jquery var generated after init could be more efficient...
					that.portrait_form = that.$el.find('#PortraitForm').ajaxForm({
						iframe : true,
						dataType : 'json',
						type : "POST",
						url : "/api?upload_portrait=true&character_id=" + that.options.character_id,
						success : function (data) {
							if (data.success) {
								that.options.model.fetch()
							} else {
								alert('Error: ' + data.error_desc)
							}
						},
						error : function() {
							alert('Unhandled server error!')
						}
					})

					if (callback) {
						callback()
					}
					console.log('view rendered')
					return that
				});
			},
			drawskills: function() {
				//skillbar attachment - bindings handled separately
				var that = this
				_.each(_.keys(that.options.model.get('skills')), function(g) {
					_.each(that.options.model.get('skills')[g], function(s, index) {
						//console.log(s, that.options.model.get_skill_cap(s))
						var skillbarview = new views.SkillBarView({
							id : 'skill_' + s.id,
							min : 0,
							max : 6,
							cap : that.options.model.get_skill_cap(s),
							value : s.value,
							afterdraw : function(v) {
								//console.log(v)
								that.$el.find('#skill_bar_' + s.id).html(skillbarview.el)
								var reqs_txt = that.options.model.get_attr_requirements(s)
								if (reqs_txt && reqs_txt != '') {
									//see a nifty css trick in app.css
									that.$el.find('#skill_bar_' + s.id).attr('title', ' ')
									that.$el.find('#skill_bar_' + s.id).attr('data-title', reqs_txt)
								}
								var inputel = v.$el.find('input')
								inputel.on('change', function() {
									//horrible but wasting resources is fine, right?
									var skills = $.extend(true, {}, that.options.model.get('skills'))
									skills[g][index].value = Number(inputel.val())
									that.options.model.set('skills', skills)
								})
							}
						})
						skillbarview.render()
					})
				})
			}
		})
	}
	return views
});
