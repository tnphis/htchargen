#Similarly to django version, most database ops happen here.
import json, simplejson, os
from flask import session, request, g
from functools import wraps
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import modules.odb as odb, modules.u as u

#Helper functions
def get_character_data(cur, character_id):
	cur.execute('''select
		name, level, gender_id, race_id, social_background_id, point_pool, wealth, portrait_url
		from characters where character_id = %s''', (character_id,))

	char_data = cur.fetchone()

	res_data = {
		'id' : character_id,
		'name' : char_data[0],
		'level' : char_data[1],
		'gender' : char_data[2],
		'race' : char_data[3],
		'social_background' : char_data[4],
		'points' : char_data[5],
		'wealth' : char_data[6],
		'portrait_url' : char_data[7]
	}

	res_data['attributes'] = []
	cur.execute('''select ca.attribute_code, a.attribute_name, ca.attribute_value
		from character_attributes ca left join attributes a on ca.attribute_code = a.attribute_code
		where ca.character_id = %s''', (character_id,))

	for a in cur:
		res_data['attributes'].append({
			'code' : a[0],
			'name' : a[1],
			'value' : a[2]
		})

	#all the info about the skills is sent with the character data
	res_data['skills'] = {}
	cur.execute('''select cs.skill_id, s.skill_name, cs.skill_value, s.primary_attribute, s.secondary_attribute, g.skill_group_name
		from character_skills cs left join skills s on cs.skill_id = s.skill_id left join skill_groups g on s.group_id = g.skill_group_id
		where cs.character_id = %s''', (character_id,))

	for row in cur:
		if res_data['skills'].has_key(row[5]):
			res_data['skills'][row[5]].append({
				'id' : row[0],
				'name' : row[1],
				'value' : row[2],
				'primary_attribute' : row[3],
				'secondary_attribute' : row[4]
			})
		else:
			res_data['skills'][row[5]] = [{
				'id' : row[0],
				'name' : row[1],
				'value' : row[2],
				'primary_attribute' : row[3],
				'secondary_attribute' : row[4]
			}]

	res_data['skill_training'] = []

	#ignore the feats for now or indefinitely
	res_data['feats'] = {}
	cur.execute('select feat_type_name from feat_types')
	for row in cur:
		res_data['feats'][row[0]] = []

	return res_data

def calculate_points(cur, starting_value, char_data):
	ret_value = int(starting_value)

	#social background
	cur.execute('select point_cost from social_backgrounds where background_id = %s', (char_data.get('social_background'),))
	current_social_bk_cost = int(cur.fetchone()[0])
	#don't forget that new characters should have a default previous value of 0
	if int(char_data.get('id')) == -1:
		ret_value -= current_social_bk_cost
	else:
		cur.execute('''select b.point_cost from social_backgrounds b where
			(select count(*) from characters c where c.character_id = %s and c.social_background_id = b.background_id) > 0''', (char_data.get('id'),))
		prev_social_bk_cost = int(cur.fetchone()[0])
		ret_value += prev_social_bk_cost - current_social_bk_cost

	#attributes
	cur.execute('select value from settings where name = \'attribute_cost\'')
	attr_cost = int(cur.fetchone()[0])
	for a in char_data.get('attributes'):
		if int(char_data.get('id')) == -1:
			cur.execute('select value from settings where name = \'base_attribute_value\'')
		else:
			cur.execute(
				'select attribute_value from character_attributes where attribute_code = %s and character_id = %s',
				(a.get('code'), char_data.get('id'))
			)

		prev_value = int(cur.fetchone()[0])

		if int(char_data.get('id')) != -1 and prev_value > a.get('value'):
			raise ValueError('Lower than previous attribute value detected')

		ret_value += (prev_value - int(a.get('value'))) * attr_cost

	#skills
	cur.execute('select value from settings where name = \'skill_cost\'')
	skill_cost = int(cur.fetchone()[0])
	for g in char_data.get('skills'):
		for s in char_data.get('skills').get(g):
			if int(char_data.get('id')) == -1:
				prev_value = 0
			else:
				cur.execute(
					'select skill_value from character_skills where skill_id = %s and character_id = %s',
					(s.get('id'), char_data.get('id'))
				)
				prev_value = int(cur.fetchone()[0])

			if int(char_data.get('id')) != -1 and prev_value > s.get('value'):
				raise ValueError('Lower than previous skill value detected')

			ret_value += (prev_value - s.get('value')) * skill_cost

	#ignoring feats as usual

	return ret_value

def char_exists(cur, char_id):
	cur.execute(
		'select count(*) from characters where character_id = %s and owner_id = %s',
		(char_id, session.get('user_id'))
	)
	return cur.fetchone()[0]

#a really unnecessary check_char_exists decorator.
#Turns out it will not accept any class or module request arguments
#but we will leave it like that for educationsl purposes.
def check_char_exists(char_id = None):
	def char_exists_decorator(func):
		def char_exists_wrapper(self, *args, **kwargs):
			if self.current_char_id is not None and int(self.current_char_id) == -1:
				return func(self, *args, **kwargs)
			else:
				if char_exists(self.cur, self.current_char_id) == 0:
					self.res['success'] = False
					self.res['error_desc'] = 'The character does not exist.'
					return json.dumps(self.res)
				else:
					return func(self, *args, **kwargs)

		return char_exists_wrapper
	return char_exists_decorator

#url handler
@u.handle_all_generic_errors
class APIHandler(odb.DatabaseConnector):
	def __init__(self, **args):
		odb.DatabaseConnector.__init__(self, **args)
		if args.get('set_character_id') is not None:
			self.current_char_id = args.get('set_character_id')
		else:
			self.current_char_id = request.args.get('character_id')

	def get_settings(self):
		self.res['data'] = {}

		self.cur.execute('select name, value from settings')
		for row in self.cur:
			self.res['data'][row[0]] = row[1]

		self.res['data']['objects'] = {}
		self.cur.execute('select race_id, race_name from races')
		self.res['data']['objects']['races'] = []
		for row in self.cur:
			self.res['data']['objects']['races'].append({'id' : row[0], 'name' : row[1]})

		self.cur.execute('select gender_id, gender_name from genders')
		self.res['data']['objects']['genders'] = []
		for row in self.cur:
			self.res['data']['objects']['genders'].append({'id' : row[0], 'value' : row[1]})

		self.cur.execute('select background_id, background_name, starting_wealth, point_cost from social_backgrounds')
		self.res['data']['objects']['social_backgrounds'] = []
		for row in self.cur:
			self.res['data']['objects']['social_backgrounds'].append({
				'id' : row[0],
				'value' : row[1],
				'starting_wealth' : row[2],
				'point_cost' : row[3]
			})

		self.cur.execute('''select f.feat_id, t.feat_type_name, f.feat_name, f.feat_description, f.point_cost
			from feats f left join feat_types t on f.type_id = t.feat_type_id''')
		self.res['data']['objects']['feats'] = {}
		for row in self.cur:
			if self.res['data']['objects']['feats'].has_key(row[1]):
				self.res['data']['objects']['feats'][row[1]].append({
					'id' : row[0],
					'name' : row[2],
					'description' : row[3],
					'point_cost' : row[4]
				})
			else:
				self.res['data']['objects']['feats'][row[1]] = [{
					'id' : row[0],
					'name' : row[2],
					'description' : row[3],
					'point_cost' : row[4]
				}]

		self.res['success'] = True

		return json.dumps(self.res)

	def get_characters_list(self):
		self.cur.execute('''select c.character_id, c.name, c.level, g.gender_name, r.race_name, b.background_name, c.wealth, c.point_pool
			from characters c left join genders g on c.gender_id = g.gender_id
			left join races r on c.race_id = r.race_id
			left join social_backgrounds b on c.social_background_id = b.background_id
			where c.owner_id = %s
		''', (session.get('user_id'),))

		self.res['data'] = []
		for row in self.cur:
			self.res['data'].append({
				'id' : row[0],
				'name' : row[1],
				'level' : row[2],
				'gender' : row[3],
				'race' : row[4],
				'social_background' : row[5],
				'wealth' : row[6],
				'point_pool' : row[7],
			})

		self.res['success'] = True

		return json.dumps(self.res)

	def get_character(self):
		#an id of -1 means it's a new character
		if request.args.get('character_id') != '-1' and request.args.get('character_id') != None and request.args.get('character_id') != '':
			if char_exists(self.cur, request.args.get('character_id')) == 0:
				self.res['success'] = False
				self.res['error_desc'] = 'The character does not exist.'
			else:
				self.res['data'] = get_character_data(self.cur, request.args.get('character_id'))
				self.res['success'] = True
		else:
			#we don't want to init a new one here. Just return everything by default, an actual model object will be generated in post/put.
			self.cur.execute('select value from settings where name = \'base_character_points\'')
			self.res['data'] = {
				'name' : '',
				'level' : 1,
				'gender' : None,
				'race' : None,
				'social_background' : None,
				'points' : self.cur.fetchone()[0],
				'wealth' : None, #generated after creation
				'portrait_url' : ''
			}

			self.res['data']['attributes'] = []
			self.cur.execute('select value from settings where name = \'base_attribute_value\'')
			base_attr_value = self.cur.fetchone()[0]
			self.cur.execute('select attribute_code, attribute_name from attributes')
			for a in self.cur:
				self.res['data']['attributes'].append({
					'code' : a[0],
					'name' : a[1],
					'value' : base_attr_value
				})

			#all the info about the skills is sent with the character data
			self.res['data']['skills'] = {}
			self.cur.execute('''select s.skill_id, s.skill_name, s.primary_attribute, s.secondary_attribute, g.skill_group_name
			from skills s left join skill_groups g on s.group_id = g.skill_group_id''')
			for s in self.cur:
				if self.res['data']['skills'].has_key(s[4]):
					self.res['data']['skills'][s[4]].append({
						'id' : s[0],
						'name' : s[1],
						'value' : 0,
						'primary_attribute' : s[2],
						'secondary_attribute' : s[3]
					})
				else:
					self.res['data']['skills'][s[4]] = [{
						'id' : s[0],
						'name' : s[1],
						'value' : 0,
						'primary_attribute' : s[2],
						'secondary_attribute' : s[3]
					}]

			self.res['data']['skill_training'] = []

			#feats are stored in the settings, so, we don't need any extra info or existing feats here
			#right, this is a new character, not an existing one! All sorts of crap for existing ones upcoming...
			self.res['data']['feats'] = {}
			self.cur.execute('select feat_type_name from feat_types')
			for row in self.cur:
				self.res['data']['feats'][row[0]] = []

		self.res['success'] = True

		return json.dumps(self.res)

	def save_character(self):
		char_data = simplejson.loads(request.data)

		if int(char_data.get('id')) == -1:
			self.cur.execute('select value from settings where name = \'base_character_points\'')
			base_value = int(self.cur.fetchone()[0])
			point_pool = calculate_points(self.cur, base_value, char_data)

			if point_pool < 0:
				res['success'] = False
				res['error_desc'] = 'Data manipulation detected! Not enough character points for the value changes.'
			else:
				self.cur.execute('select starting_wealth from social_backgrounds where background_id = %s', (char_data.get('social_background'),))
				char_wealth = self.cur.fetchone()[0]

				self.cur.execute('''insert into characters
					(owner_id, name, level, gender_id, race_id, social_background_id, wealth, point_pool)
					values (%s, %s, 1, %s, %s, %s, %s, %s)''', (
						session.get('user_id'),
						char_data.get('name'),
						char_data.get('gender'),
						char_data.get('race'),
						char_data.get('social_background'),
						char_wealth,
						point_pool
					)
				)

				new_char_id = self.cur.lastrowid

				for a in char_data.get('attributes'):
					self.cur.execute('''insert into character_attributes (character_id, attribute_code, attribute_value)
					values (%s, %s, %s)''', (new_char_id, a.get('code'), a.get('value')))

				for g in char_data.get('skills'):
					for s in char_data.get('skills').get(g):
						self.cur.execute('''insert into character_skills (character_id, skill_id, skill_value)
						values (%s, %s, %s)''', (new_char_id, s.get('id'), s.get('value')))

				self.dbh.commit()
				#no feats and trainings, as usual
				self.res['data'] = get_character_data(self.cur, new_char_id)
				self.res['success'] = True
		else:
			if char_exists(self.cur, char_data.get('id')) == 0:
				self.res['success'] = False
				self.res['error_desc'] = 'The character does not exist.'
			else:
				self.cur.execute('select point_pool from characters where character_id = %s', (char_data.get('id'),))
				new_points = calculate_points(self.cur, self.cur.fetchone()[0], char_data)

				self.cur.execute('update characters set name = %s, point_pool = %s where character_id = %s and owner_id = %s',
					(char_data.get('name'), new_points, char_data.get('id'), session.get('user_id')))

				for a in char_data.get('attributes'):
					self.cur.execute('update character_attributes set attribute_value = %s where character_id = %s and attribute_code = %s',
						(a.get('value'), char_data.get('id'), a.get('code')))

				for g in char_data.get('skills'):
					for s in char_data.get('skills').get(g):
						self.cur.execute('update character_skills set skill_value = %s where character_id = %s and skill_id = %s',
							(s.get('value'), char_data.get('id'), s.get('id')))

				self.dbh.commit()

				self.res['data'] = get_character_data(self.cur, char_data.get('id'))
				self.res['success'] = True

		return json.dumps(self.res)

	#the function call part is really important here! Otherwise, internal function parameters will be passed to our external decorator function!
	@check_char_exists()
	def levelup_character(self):
		self.cur.execute('select value from settings where name = \'level_cap\'')
		level_cap = self.cur.fetchone()[0]

		self.cur.execute('select level from characters where character_id = %s and owner_id = %s',
			(request.args.get('character_id'), session.get('user_id')))
		current_level = self.cur.fetchone()[0]

		if current_level >= level_cap:
			self.res['success'] = False
			self.res['error_desc'] = 'Level is already at maximum'
		else:
			#technically, don't need this query but subquery is a bit cumbersome
			self.cur.execute('select value from settings where name = \'points_per_level\'')
			points_per_level = self.cur.fetchone()[0]
			self.cur.execute('''update characters set level = level + 1, point_pool = point_pool + %s
				where character_id = %s and owner_id = %s''',
				(points_per_level, request.args.get('character_id'), session.get('user_id')))

			self.dbh.commit()
			self.res['success'] = True

		return json.dumps(self.res)

	@check_char_exists()
	def delete_character(self):
		#don't forget to delete from skills, attributes (and feats and trainings one of these days)
		#the current_char_id is handled in __init__ in a slightly fancy way because it can either be
		#a request arg or a part of the url (in case of removal from the list interface)
		print self.current_char_id
		self.cur.execute('delete from character_attributes where character_id = %s', (self.current_char_id,))
		self.cur.execute('delete from character_skills where character_id = %s', (self.current_char_id,))
		self.cur.execute('delete from character_feats where character_id = %s', (self.current_char_id,))
		self.cur.execute('delete from character_skill_training where character_id = %s', (self.current_char_id,))
		self.cur.execute('delete from characters where character_id = %s and owner_id = %s', (self.current_char_id, session.get('user_id')))
		self.dbh.commit()
		self.res['success'] = True
		return json.dumps(self.res)

	@check_char_exists()
	def upload_character_portrait(self):
		try:
			file_path = os.path.dirname(os.path.dirname(__file__))[:-3] + 'app/img/portraits/'
			uploaded_file = None
			file_data = None

			for f in request.files.values():
				file_data = f.read()
				if len(file_data) > 524288:
					self.res['success'] = False
					self.res['error_desc'] = 'The portrait file must be smaller than 512 kilobytes.'
					return json.dumps(self.res)

				uploaded_file = f

			self.cur.execute('select portrait_url from characters where character_id = %s and owner_id = %s',
				(request.args.get('character_id'), session.get('user_id')))

			current_portrait_url = self.cur.fetchone()[0]

			if current_portrait_url is not None and current_portrait_url != '':
				try:
					os.unlink(file_path + current_portrait_url)
				except:
					pass

				self.cur.execute('update characters set portrait_url = null where character_id = %s and owner_id = %s',
					(request.args.get('character_id'), session.get('user_id')))

			if uploaded_file:
				user_filename = secure_filename(uploaded_file.filename)
				#handle fakepath if necessary
				fakepath = user_filename.find('fakepath')
				if fakepath > 0:
					user_filename = user_filename[fakepath + 9 : ]

				real_filename = u.get_filename(user_filename)
				#primitive extension checking in get_filename. Technically, would be better to check image by data headers.
				if real_filename is None:
					self.res['success'] = False
					self.res['error_desc'] = 'Unsupported image format'
					#no point in rolling back as the old file has already been removed.
				else:
					#uploaded_file.save(file_path + real_filename)
					#we have already read the data, unfortunately. So, save like a man.
					portrait_file = open(file_path + real_filename, 'wb')
					portrait_file.write(file_data)
					portrait_file.close()

					self.cur.execute('update characters set portrait_url = %s where character_id = %s and owner_id = %s',
						(real_filename, request.args.get('character_id'), session.get('user_id')))
					self.res['success'] = True
			else:
				self.res['success'] = True

			self.dbh.commit()
			return json.dumps(self.res)
		#this doesn't seem to work but whatever.
		except RequestEntityTooLarge:
			return '{"success" : false, "error_desc" : "Maximum file size exceeded"}'
