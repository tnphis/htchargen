//a non-model view to represent a user control panel navbar
var NavbarView = Backbone.View.extend({
	//el: $("#navbarcontainer"),
	tagName: 'div',
	initialize: function(options) {
		this.options = options || {}
	},
	events: {
		'click #MenuLogout': function() {
			if (confirm('Confirm user logout')) {
				$.ajax({
					url: '/app/auth?logout=true',
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
					url: '/app/auth?change_passwd=true&old_passwd=' + old_passwd + '&new_passwd=' + new_passwd,
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
});

return NavbarView;
