from flask import Flask, g, request, session, redirect, abort
import datetime as dt, re, os
import modules.api as api, modules.auth as auth, modules.sessions

chargenapp = Flask('web', static_folder = '../app', static_url_path = '/app')
chargenapp.config.from_pyfile(os.path.abspath(os.path.dirname(__file__)) + '/config.py')
session_object = {}
chargenapp.session_interface = modules.sessions.ManagedSessionInterface(
	modules.sessions.CachingSessionManager(
		modules.sessions.ObjectSessionManager(
			chargenapp.config['SECRET_KEY'],
			session_object
		),
		10000
	),
	['/app'],
	dt.timedelta(days=14)
)

@chargenapp.before_request
def before_request():
	g.app_config = chargenapp.config

@chargenapp.errorhandler(413)
def request_entity_too_large(error):
    return '{"success" : false, "error_desc" : "Maximum file size exceeded"}'

#definitely not an accessible file! Still, should move the next compile a folder above.
@chargenapp.route('/app/compile.py')
def return_404():
	abort(404)

@chargenapp.route('/')
@chargenapp.route('/<path:path>')
def return_index(path = ''):
	#this needs to actually return index without redirecting!
	index_file = open('../app/index.html', 'r')
	index_file_contents = index_file.read()
	index_file.close()
	return index_file_contents

@chargenapp.route('/auth')
def url_auth():
	skip_db_connection = False
	if request.args.get('logout'):
		skip_db_connection = True

	current_request_handler = auth.AuthHandler(skip_connection = skip_db_connection)

	if request.args.get('get_user_id'):
		return current_request_handler.get_user_id()
	elif request.args.get('login'):
		return current_request_handler.login_user()
	elif request.args.get('logout'):
		return current_request_handler.logout_user()
	elif request.args.get('register'):
		return current_request_handler.register_user()
	elif request.args.get('change_passwd'):
		return current_request_handler.change_passwd()
	else:
		return '{"success" : false, "error_desc": "Unsupported keyword"}'

@chargenapp.route('/api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def url_api():
	if not(session.get('user_logged_in')):
		return '{"success" : false, "error_desc" : "Unauthorized access."}'

	#special handling for removal from the list
	if request.method == 'DELETE' and request.args.get('get_characters_list') and re.search(r'true/(\d+)', request.args.get('get_characters_list')):
		#a collection/characters list call
		current_char_id = int(re.findall(r'true/(\d+)', request.args.get('get_characters_list'))[0])
		current_request_handler = api.APIHandler(set_character_id = current_char_id)
	else:
		current_request_handler = api.APIHandler()

	if request.method == 'GET':
		if request.args.get('get_settings'):
			return current_request_handler.get_settings()
		elif request.args.get('get_characters_list'):
			return current_request_handler.get_characters_list()
		elif request.args.get('get_character'):
			return current_request_handler.get_character()
		else:
			return '{"success" : false, "error_desc": "Unsupported keyword"}'
	elif request.method == 'PUT':
		return current_request_handler.save_character()
	elif request.method == 'DELETE':
		return current_request_handler.delete_character()
	elif request.method == 'POST':
		if request.args.get('levelup'):
			return current_request_handler.levelup_character()
		elif request.args.get('upload_portrait'):
			return current_request_handler.upload_character_portrait()
		else:
			return '{"success" : false, "error_desc": "Unsupported keyword"}'

if __name__ == '__main__':
	chargenapp.run()
