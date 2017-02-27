from flask import session, g
import mysql.connector

def getdbh():
	if not(g.app_config.get('PERSISTENT_DB')) or (g.app_config.get('PERSISTENT_DB') and session.get('dbh') is None):
		conn = mysql.connector.connect(
			user = g.app_config['DB_USERNAME'],
			password = g.app_config['DB_PASSWORD'],
			host = '127.0.0.1',
			database = g.app_config['DATABASE'],
			buffered = True
		)

		session['dbh'] = conn

	return session['dbh']

#it's possible to decorate every method with handle_generic_errors here
#but jic we want to implement a more customized error handling (such as passing arguments to the decorator),
#we'll stick with manual decoration for a while.
class DatabaseConnector(object):
	def __init__(self, **args):
		self.res = {}
		if args.get('skip_connection'):
			pass
		else:
			try:
				self.dbh = getdbh()
				self.cur = self.dbh.cursor()
			except:
				if hasattr(self, 'dbh') and hasattr(self.dbh, 'rollback'):
					self.dbh.rollback()
				import traceback
				print traceback.format_exc()
				return '{"success" : false, "error_desc" : "Database unavailable"}'
