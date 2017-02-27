from flask import session, g, request
import odb, json, u, hashlib

@u.handle_all_generic_errors
class AuthHandler(odb.DatabaseConnector):
	def register_user(self):
		self.cur.execute('select count(*) from users where user_name = %s', (request.args['user_name'],))
		if self.cur.fetchone()[0] > 0:
			self.res['success'] = False
			self.res['error_desc'] = 'A user with this name already exists'
		else:
			self.cur.execute('select count(*) from users where email = %s', (request.args['user_email'],))
			if self.cur.fetchone()[0] > 0:
				self.res['success'] = False
				self.res['error_desc'] = 'A user with this email already exists'
			else:
				new_passwd = u.randomword(10)
				new_passwd_hash = hashlib.sha256(new_passwd).hexdigest()

				self.cur.execute('insert into users (user_name, email, password_hash) values (%s, %s, %s)', (request.args['user_name'], request.args['user_email'], new_passwd_hash))
				self.dbh.commit()
				res['success'] = True
				res['passwd'] = new_passwd

		return json.dumps(self.res)

	def login_user(self):
		self.cur.execute('select user_id from users where user_name = %s and password_hash = %s', (request.args['user_name'], hashlib.sha256(request.args['user_passwd']).hexdigest()))
		if self.cur.rowcount == 0:
			self.res['success'] = False
			self.res['error_desc'] = 'Incorrect user name or password'
		else:
			session['user_logged_in'] = True
			session['user_id'] = self.cur.fetchone()[0]
			self.res['success'] = True

		return json.dumps(self.res)

	def logout_user():
		session['user_id'] = None
		session['user_logged_in'] = False
		return '{"success": true}'

	def get_user_id(self):
		self.res = {}
		self.res['user_id'] = session.get('user_id')
		if self.res['user_id']:
			self.cur.execute('select user_name from users where user_id = %s', (session.get('user_id'),))
			self.res['user_name'] = self.cur.fetchone()[0]
			self.res['success'] = True
		else:
			self.res['success'] = False

		return json.dumps(self.res)

	def change_passwd(self):
		self.cur.execute('select password_hash from users where user_id = %s', (session['user_id'],))
		if hashlib.sha256(request.args['old_passwd']).hexdigest() != self.cur.fetchone()[0]:
			self.res['success'] = False
			self.res['error_desc'] = 'Old password is incorrect'
		else:
			self.cur.execute('update users set password_hash = %s where user_id = %s', (hashlib.sha256(request.args['new_passwd']).hexdigest(), session['user_id']))
			self.dbh.commit()
			self.res['success'] = True

		return json.dumps(self.res)
