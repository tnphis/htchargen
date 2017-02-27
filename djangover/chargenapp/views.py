from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, hashers
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import htchargen
import json, u, models, simplejson, re, os, random
import datetime as dt

def index(request):
	context = RequestContext(request, {})
	return render(request, 'chargenapp/index.html', context)

def redir(request):
	return HttpResponseRedirect('app/client')

def register_user(user_name, user_email):
	new_passwd = u.randomword(10)
	user = User.objects.create_user(user_name, user_email, new_passwd)

	return new_passwd

def login_user(user_name, user_passwd, request):
	user = authenticate(username=user_name, password=user_passwd)
	if user is not None:
		# the password verified for the user
		if user.is_active:
			login(request, user)
			return user.id

	return -1

def change_passwd(user, old_passwd, new_passwd):
	if hashers.check_password(old_passwd, user.password):
		user.set_password(new_passwd)
		user.save()
		return {'success' : True}
	else:
		return {'success' : False, 'error_desc' : 'The old password is incorrect.'}

def get_filename(user_filename):
	starting_point = dt.datetime(2016,1,17)
	now = dt.datetime.now()
	dot_index = user_filename.rfind('.')
	if user_filename[dot_index:] not in ('.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.tif', '.tiff'):
		return None

	file_name = user_filename[:dot_index] + str(int((now - starting_point).total_seconds() * 1000 + now.microsecond/1000)) + str(random.randrange(0, 9999999)) + u.randomword(4) + user_filename[dot_index:]
	return file_name

def auth(request):
	res = {}

	if request.GET.get('register'):
		try:
			user_passwd = register_user(request.GET['user_name'], request.GET['user_email'])
			res['success'] = True
			res['passwd'] = user_passwd
		except IntegrityError as e:
			print e
			res['success'] = False
			res['error_desc'] = 'User with this username or email already exists'
	elif request.GET.get('login'):
		user_id = login_user(request.GET.get('user_name'), request.GET.get('user_passwd'), request)
		if user_id >= 0:
			res['success'] = True
			res['user_id'] = user_id
		else:
			res['success'] = False
	elif request.GET.get('logout'):
		logout(request)
		res['success'] = True
	elif request.GET.get('get_user_id'):
		if request.user.is_authenticated():
			res['success'] = True
			res['user_id'] = request.user.id
			res['user_name'] = str(request.user)
		else:
			res['success'] = False
	elif request.GET.get('logout'):
		logout(request)
		res['success'] = True
	elif request.GET.get('change_passwd'):
		res = change_passwd(request.user, request.GET.get('old_passwd'), request.GET.get('new_passwd'))
	else:
		res['success'] = False
		res['error_desc'] = 'Unsupported keyword'

	return HttpResponse(json.dumps(res))

def get_character_data(char_object):
	res_data = {
		'id' : char_object.id,
		'name' : char_object.name,
		'level' : char_object.level,
		'gender' : char_object.gender.id,
		'race' : char_object.race.id,
		'social_background' : char_object.social_background.id,
		'points' : char_object.point_pool,
		'wealth' : char_object.wealth,
		'portrait_url' : char_object.portrait_url
	}

	res_data['attributes'] = []
	for a in models.CharacterAttribute.objects.filter(character = char_object):
		res_data['attributes'].append({
			'code' : a.attribute.code,
			'name' : a.attribute.name,
			'value' : a.value
		})

	#all the info about the skills is sent with the character data
	res_data['skills'] = {}
	for g in models.SkillGroup.objects.all():
		res_data['skills'][g.name] = []
		for s in models.Skill.objects.filter(group = g):
			current_char_skill = models.CharacterSkill.objects.get(skill = s, character = char_object)
			res_data['skills'][g.name].append({
				'id' : s.id,
				'name' : s.name,
				'value' : current_char_skill.value,
				'primary_attribute' : s.primary_attribute.code,
				'secondary_attribute' : s.secondary_attribute.code
			})

	res_data['skill_training'] = []

	#ignore the feats for now or indefinitely
	res_data['feats'] = {}
	for g in models.FeatType.objects.all():
		res_data['feats'][g.value] = []

	return res_data

def calculate_points(starting_value, char_data, char_obj):
	ret_value = int(starting_value)

	#social background
	current_social_bk = models.SocialBackground.objects.get(id = char_data.get('social_background'))
	#don't forget that new characters should have a default previous value of 0
	if char_data.get('id') == -1:
		ret_value -= current_social_bk.point_cost
	else:
		ret_value += char_obj.social_background.point_cost - current_social_bk.point_cost

	#attributes
	attr_cost = int(models.Setting.objects.get(name = 'attribute_cost').value)
	for a in char_data.get('attributes'):
		current_attr = models.Attribute.objects.get(code = a.get('code'))
		if int(char_data.get('id')) == -1:
			prev_value = int(models.Setting.objects.get(name = 'base_attribute_value').value)
		else:
			#print 'id != -1 : ' + str(char_data.get('id')) + ' : ' + str(int(char_data.get('id'))) + ' : ' + str(type(int(char_data.get('id')))) + ' : ' + str(type(-1))
			prev_value = models.CharacterAttribute.objects.get(character = char_obj, attribute = current_attr).value

		if int(char_data.get('id')) != -1 and prev_value > a.get('value'):
			raise ValueError('Lower than previous attribute value detected')

		ret_value += (prev_value - int(a.get('value'))) * attr_cost

	#skills
	skill_cost = int(models.Setting.objects.get(name = 'skill_cost').value)
	for g in char_data.get('skills'):
		for s in char_data.get('skills').get(g):
			current_skill = models.Skill.objects.get(id = int(s.get('id')))
			if int(char_data.get('id')) == -1:
				prev_value = 0
			else:
				prev_value = models.CharacterSkill.objects.get(character = char_obj, skill = current_skill).value

			if int(char_data.get('id')) != -1 and prev_value > s.get('value'):
				raise ValueError('Lower than previous skill value detected')

			ret_value += (prev_value - s.get('value')) * skill_cost

	#ignoring feats as usual

	return ret_value

def api(request):
	res = {}

	if not request.user.is_authenticated():
		res['success'] = False
		res['error_desc'] = 'Unauthorized access'
		return HttpResponse(json.dumps(res))

	if request.method == 'GET':
		if request.GET.get('get_characters_list'):
			res['data'] = []
			chars_list = models.Character.objects.filter(owner = request.user.id)

			#standard django.core serialization is not that useful here.
			#Simpler to just make a custom serializer
			for char in chars_list:
				res['data'].append({
					'id' : char.id,
					'name' : char.name,
					'level' : char.level,
					'gender' : char.gender.value,
					'race' : char.race.name,
					'social_background' : char.social_background.value,
					'wealth' : char.wealth,
					'point_pool' : char.point_pool,
				})

			res['success'] = True
		elif request.GET.get('get_settings'):
			res['data'] = {}

			global_settings_list = models.Setting.objects.all()
			for itm in global_settings_list:
				res['data'][itm.name] = itm.value

			res['data']['objects'] = {}

			races_list = models.Race.objects.all()
			res['data']['objects']['races'] = []
			for itm in races_list:
				res['data']['objects']['races'].append({'id' : itm.id, 'name' : itm.name})

			res['data']['objects']['genders'] = []
			genders_list = models.Gender.objects.all()
			for itm in genders_list:
				res['data']['objects']['genders'].append({'id' : itm.id, 'value' : itm.value})

			res['data']['objects']['social_backgrounds'] = []
			bks_list = models.SocialBackground.objects.all()
			for itm in bks_list:
				#silly but actually quicker than any other serialization techniques
				res['data']['objects']['social_backgrounds'].append({
					'id' : itm.id,
					'value' : itm.value,
					'starting_wealth' : itm.starting_wealth,
					'point_cost' : itm.point_cost
				})

			res['data']['objects']['feats'] = {}
			fts_list = models.FeatType.objects.all()
			for itm in fts_list:
				#handle the sorting in here, draw on the client
				res['data']['objects']['feats'][itm.value] = []
				filtered_feats_list = models.Feat.objects.filter(feat_type = itm)

				for ft in filtered_feats_list:
					res['data']['objects']['feats'][itm.value].append({
						'id' : ft.id,
						'name' : ft.name,
						'description' : ft.description,
						'point_cost' : ft.point_cost
					})

			res['success'] = True
		elif request.GET.get('get_character'):

			#an id of -1 means it's a new character
			if request.GET.get('character_id') != '-1' and request.GET.get('character_id') != None and request.GET.get('character_id') != '':
				#security reasons
				current_char = None
				try:
					current_char = models.Character.objects.get(id = request.GET.get('character_id'), owner = request.user)
				except ObjectDoesNotExist:
					res['success'] = False
					res['error_desc'] = 'The character does not exist.'

				if current_char:
					res['data'] = get_character_data(current_char)
					res['success'] = True
			else:
				#we don't want to init a new one here. Just return everything by default, an actual model object will be generated in post/put.
				res['data'] = {
					'name' : '',
					'level' : 1,
					'gender' : None,
					'race' : None,
					'social_background' : None,
					'points' : models.Setting.objects.get(name = 'base_character_points').value,
					'wealth' : None, #generated after creation
					'portrait_url' : ''
				}

				res['data']['attributes'] = []
				for a in models.Attribute.objects.all():
					res['data']['attributes'].append({
						'code' : a.code,
						'name' : a.name,
						'value' : models.Setting.objects.get(name = 'base_attribute_value').value
					})

				#all the info about the skills is sent with the character data
				res['data']['skills'] = {}
				for g in models.SkillGroup.objects.all():
					res['data']['skills'][g.name] = []
					for s in models.Skill.objects.filter(group = g):
						res['data']['skills'][g.name].append({
							'id' : s.id,
							'name' : s.name,
							'value' : 0,
							'primary_attribute' : s.primary_attribute.code,
							'secondary_attribute' : s.secondary_attribute.code
						})

				res['data']['skill_training'] = []

				#feats are stored in the settings, so, we don't need any extra info or existing feats here
				#right, this is a new character, not an existing one! All sorts of crap for existing ones upcoming...
				res['data']['feats'] = {}
				for g in models.FeatType.objects.all():
					res['data']['feats'][g.value] = []
				#print 'inside!!'
				#print res['data']

			res['success'] = True
		else:
			res['success'] = False
			res['error_desc'] = 'Unsupported keyword'
	elif request.method == 'PUT':
		#print request.body
		char_data = simplejson.loads(request.body)
		#print char_data
		current_char_id = int(char_data.get('id'))

		if current_char_id == -1:
			new_char_obj = models.Character(
				owner = request.user,
				name = char_data.get('name'),
				level = 1,
				gender = models.Gender.objects.get(id = int(char_data.get('gender'))),
				race = models.Race.objects.get(id = int(char_data.get('race'))),
				social_background = models.SocialBackground.objects.get(id = int(char_data.get('social_background'))),
				wealth = models.SocialBackground.objects.get(id = int(char_data.get('social_background'))).starting_wealth
			)

			new_char_obj.point_pool = calculate_points(models.Setting.objects.get(name = 'base_character_points').value, char_data, new_char_obj)
			if new_char_obj.point_pool < 0:
				res['success'] = False
				res['error_desc'] = 'Data manipulation detected! Not enough character points for the value changes.'
				return HttpResponse(json.dumps(res))

			#let's actually deliberately avoid skill validation for whatever reason...
			new_char_obj.save()

			for a in char_data.get('attributes'):
				new_attr_obj = models.Attribute.objects.get(code = a.get('code'))
				new_char_attr_obj = models.CharacterAttribute(
					character = new_char_obj,
					attribute = new_attr_obj,
					value = int(a.get('value'))
				)
				new_char_attr_obj.save()

			for g in char_data.get('skills'):
				for s in char_data.get('skills').get(g):
					new_skill_obj = models.Skill.objects.get(id = s.get('id'))
					#print s
					new_char_skill_obj = models.CharacterSkill(
						character = new_char_obj,
						skill = new_skill_obj,
						value = int(s.get('value'))
					)
					new_char_skill_obj.save()
			#we do need that here since the character objects are different for new and old ones
			ret_data = get_character_data(new_char_obj)
			ret_data['success'] = True
			return HttpResponse(json.dumps(ret_data))
			#forget about feats and trainings for now or indefinitely, implementation is trivial
		else:
			current_char_obj = None
			try:
				current_char_obj = models.Character.objects.get(id = current_char_id, owner = request.user)
			except ObjectDoesNotExist:
				res['success'] = False
				res['error_desc'] = 'The character does not exist.'

			if current_char_obj:
				current_char_obj.name = char_data.get('name')

			#ValueErrors possible for existing characters if previous values are higher than the new ones.
			try:
				current_char_obj.point_pool = calculate_points(current_char_obj.point_pool, char_data, current_char_obj)
			except ValueError as e:
				res['success'] = False
				res['error_desc'] = 'Data manipulation detected! ' + e.args[0]
				return HttpResponse(json.dumps(res))

			if current_char_obj.point_pool < 0:
				res['success'] = False
				res['error_desc'] = 'Data manipulation detected! Not enough character points for the value changes.'
				return HttpResponse(json.dumps(res))

			current_char_obj.save()

			for a in char_data.get('attributes'):
				current_attr_obj = models.Attribute.objects.get(code = a.get('code'))
				current_char_attr_obj = models.CharacterAttribute.objects.get(
					character = current_char_obj,
					attribute = current_attr_obj,
				)
				current_char_attr_obj.value = int(a.get('value'))
				current_char_attr_obj.save()

			for g in char_data.get('skills'):
				for s in char_data.get('skills').get(g):
					current_skill_obj = models.Skill.objects.get(id = s.get('id'))
					current_char_skill_obj = models.CharacterSkill.objects.get(
						character = current_char_obj,
						skill = current_skill_obj,
					)
					current_char_skill_obj.value = int(s.get('value'))
					current_char_skill_obj.save()

			ret_data = get_character_data(current_char_obj)
			ret_data['success'] = True
			return HttpResponse(json.dumps(ret_data))

	elif request.method == 'DELETE':
		#print request.GET

		current_char = None
		current_char_id = None

		if request.GET.get('get_character'):
			#a character/model view call
			current_char_id = int(request.GET.get('character_id'))
		elif re.search(r'true/(\d+)', request.GET.get('get_characters_list')):
			#a collection/characters list call
			current_char_id = int(re.findall(r'true/(\d+)', request.GET.get('get_characters_list'))[0])

		try:
			current_char = models.Character.objects.get(id = current_char_id, owner = request.user)
		except ObjectDoesNotExist:
			res['success'] = False
			res['error_desc'] = 'The character does not exist.'

		if current_char:
			current_char.delete()
			res['success'] = True

		return HttpResponse(json.dumps(res))

	elif request.method == 'POST':
		#this is going to be a custom ajax, thus post.
		ret_data = {}

		if request.GET.get('levelup'):
			current_char = None
			try:
				current_char = models.Character.objects.get(id = int(request.GET.get('character_id')), owner = request.user)
			except ObjectDoesNotExist:
				ret_data['success'] = False
				ret_data['error_desc'] = 'The character does not exist.'

			if current_char:
				if current_char.level < int(models.Setting.objects.get(name = 'level_cap').value):
					current_char.level += 1
					current_char.point_pool += int(models.Setting.objects.get(name = 'points_per_level').value)
					current_char.save()
					ret_data['success'] = True
				else:
					ret_data['success'] = False
					ret_data['error_desc'] = 'Level is already at maximum'
		elif request.GET.get('upload_portrait'):
			for f in request.FILES:
				print request.FILES[f]
				if request.FILES[f].size > 524288:
					ret_data['success'] = False
					ret_data['error_desc'] = 'The portrait file must be smaller than 512 kilobytes.'

			current_char = None
			try:
				current_char = models.Character.objects.get(id = int(request.GET.get('character_id')), owner = request.user)
			except ObjectDoesNotExist:
				ret_data['success'] = False
				ret_data['error_desc'] = 'The character does not exist.'

			if current_char:
				file_path = htchargen.settings.STATICFILES_DIRS[0][:-7] + '/chargenapp/static/chargenapp/img/portraits/'
				#delete the old portrait in any case, even if no files are uploaded (assume cleanup)
				if current_char.portrait_url:
					#jic, if something gets screwed up
					try:
						os.unlink(file_path + current_char.portrait_url)
					except:
						pass

					current_char.portrait_url = None
					current_char.save()

				file_data = None
				user_filename = None
				#assume a single file, read the last one if multiple
				for f in request.FILES:
					file_data = request.FILES[f].read()
					user_filename = request.FILES[f].name

				if user_filename and file_data:
					#handle fakepath if necessary
					fakepath = user_filename.find('fakepath')
					if fakepath > 0:
						user_filename = user_filename[fakepath + 9 : ]

					real_filename = get_filename(user_filename)
					#primitive extension checking in get_filename. Technically, would be better to check image by data headers.
					if real_filename is None:
						ret_data['success'] = False
						ret_data['error_desc'] = 'Unsupported image format'
					else:
						#note: don't forget the os.path.join here.
						portrait_file = open(file_path + real_filename, 'wb')
						portrait_file.write(file_data)
						portrait_file.close()
						current_char.portrait_url = real_filename
						current_char.save()

						ret_data['success'] = True
				else:
					ret_data['success'] = True
		else:
			ret_data['success'] = False
			ret_data['error_desc'] = 'Unsupported keyword'

		return HttpResponse(json.dumps(ret_data))

	print res
	print json.dumps(res)
	return HttpResponse(json.dumps(res))
