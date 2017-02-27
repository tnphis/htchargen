//a non-model view to login the users
var validate_email = function(p_str) {
	if (!(p_str)) {
		return false
	} else {
		if (
			p_str.indexOf('@') >= 0
			&& p_str.indexOf('.', p_str.indexOf('@')) >= 0
			&& p_str.indexOf('.', p_str.indexOf('@')) < p_str.length - 1
		) {
			return true
		} else {
			return false
		}
	}
}

var LoginView = Backbone.View.extend({
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
		var login = this.$el.find('#login').val()
		var passwd = this.$el.find('#passwd').val()
		var reglogin = this.$el.find('#reglogin').val()
		var regemail = this.$el.find('#regemail').val()
		var login_btn = this.$el.find('#btn_login')
		var register_btn = this.$el.find('#btn_register')

		if (!(login) || !(passwd)) {
			login_btn.attr('disabled', 'true')
		} else {
			login_btn.removeAttr('disabled')

			//enter submission handling
			if (e.which == 13) {
				this.login_user()
			}
		}

		if (!(reglogin) || !(validate_email(regemail))) {
			register_btn.attr('disabled', 'true')
		} else {
			register_btn.removeAttr('disabled')

			//enter submission handling
			if (e.which == 13) {
				this.register_user()
			}
		}
	},
	login_user: function() {
		var login = this.$el.find('#login').val()
		var passwd = this.$el.find('#passwd').val()
		$.ajax({
			url: '/app/auth?login=true&user_name=' + login + '&user_passwd=' + passwd,
			method: 'get',
			dataType: 'json',
			success: function(data) {
				if (data.success) {
					Global.user.id = data.user_id
					Backbone.history.navigate('app/client/characters', {trigger: true})
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
			url: '/app/auth?register=true&user_name=' + login + '&user_email=' + email,
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
});

return LoginView;
