//utility datatable view

var CharacterView = Backbone.View.extend({
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
			'models/models.comp.min',
			'views/views.comp.min',
			'backbone_stickit',
			'jqform'
		], function(models, views) {
			var CharacterModel = models.Character()
			that.options.model = new CharacterModel({
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

			that.SkillBarView = views.SkillBarView()

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
			Backbone.history.navigate('app/client/characters', {trigger: true})
		},
		'click #btn_delete': function() {
			if (confirm('Confirm the utter and irreversible destruction of ' + this.options.model.get('name'))) {
				this.options.model.destroy({
					success: function(model, response) {
						if (response.success) {
							alert('Character destroyed. Redirecting the characters list.')
							Backbone.history.navigate('app/client/characters', {trigger: true})
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
							Backbone.history.navigate('app/client/edit_character/' + response.data.id, {trigger: true})
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
					Backbone.history.navigate('app/client/edit_character/-1', {trigger: true})
				}
			} else {
				Backbone.history.navigate('app/client/edit_character/-1', {trigger: true})
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
					$.ajax({
						url: '/app/api?levelup=true&character_id=' + this.options.model.id,
						method: 'post',
						dataType: 'json',
						success: function(data) {
							if (data.success) {
								this.options.model.fetch()
								console.log(this.options.model.get('level'))
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
				//this.$el.find('#portrait_file').val(null)
				this.portrait_form.reset()
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
			'models/models.comp.min',
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
				url : "/app/api?upload_portrait=true&character_id=" + that.options.character_id,
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
				var skillbarview = new that.SkillBarView({
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
});

return CharacterView;
