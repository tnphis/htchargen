import random, string, datetime as dt, inspect
from functools import wraps

def randomword(length):
   return u''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

def get_filename(user_filename):
	starting_point = dt.datetime(2016,1,17)
	now = dt.datetime.now()
	dot_index = user_filename.rfind('.')
	if user_filename[dot_index:] not in ('.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.tif', '.tiff'):
		return None

	file_name = user_filename[:dot_index] + str(int((now - starting_point).total_seconds() * 1000 + now.microsecond/1000)) + str(random.randrange(0, 9999999)) + randomword(4) + user_filename[dot_index:]
	return file_name

def return_generic_error():
	return '{"success" : false, "error_desc" : "Unhandled error"}'

#a decorator to handle errors
def handle_generic_errors(func):
	@wraps(func)
	def func_wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except:
			#if it's a DatabaseConnector method, rollback.
			if len(args) > 0 and hasattr(args[0], 'dbh') and hasattr(args[0].dbh, 'rollback'):
				args[0].dbh.rollback()

			import traceback
			print traceback.format_exc()
			return return_generic_error()

	return func_wrapper

#a class decorator to apply the error handler to all methods
def handle_all_generic_errors(cls):
	for name, m in inspect.getmembers(cls, inspect.ismethod):
		setattr(cls, name, handle_generic_errors(m))

	return cls
