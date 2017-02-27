from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Race(models.Model):
	name = models.CharField(max_length=50)

	class Meta():
		unique_together = ('name',)

	def __unicode__(self):
		return unicode(self.name)

class Gender(models.Model):
	value = models.CharField(max_length=10)

	class Meta():
		unique_together = ('value',)

	def __unicode__(self):
		return unicode(self.value)

class Attribute(models.Model):
	code = models.CharField(max_length=3)
	name = models.CharField(max_length=50)

	class Meta():
		unique_together = (('code',), ('name',))

	def __unicode__(self):
		return unicode(self.code)

class SocialBackground(models.Model):
	value = models.CharField(max_length=50)
	starting_wealth = models.PositiveIntegerField()
	point_cost = models.SmallIntegerField()

	class Meta():
		unique_together = ('value',)

	def __unicode__(self):
		return unicode(self.value)

class SkillGroup(models.Model):
	name = models.CharField(max_length=100)

	class Meta():
		unique_together = ('name',)

	def __unicode__(self):
		return unicode(self.name)

class Skill(models.Model):
	group = models.ForeignKey(SkillGroup)
	name = models.CharField(max_length=50)
	primary_attribute = models.ForeignKey(Attribute, related_name='primary_attr')
	secondary_attribute = models.ForeignKey(Attribute, related_name='secondary_attr')

	class Meta():
		unique_together = ('name',)

	def __unicode__(self):
		return unicode(self.name)

class SkillTrainingLevel(models.Model):
	value = models.CharField(max_length=20)

	class Meta():
		unique_together = ('value',)

	def __unicode__(self):
		return unicode(self.value)

class FeatType(models.Model):
	value = models.CharField(max_length=100)

	class Meta():
		unique_together = ('value',)

	def __unicode__(self):
		return unicode(self.value)

class Feat(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=4000)
	feat_type = models.ForeignKey(FeatType)
	point_cost = models.SmallIntegerField()

	class Meta():
		unique_together = ('name',)

	def __unicode__(self):
		return unicode(self.name)

class Character(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=200)
	level = models.PositiveSmallIntegerField()
	gender = models.ForeignKey(Gender)
	race = models.ForeignKey(Race)
	social_background = models.ForeignKey(SocialBackground)
	point_pool = models.PositiveSmallIntegerField()
	wealth = models.PositiveIntegerField()
	portrait_url = models.CharField(max_length=1000)

	def __unicode__(self):
		return unicode(self.name)

class CharacterAttribute(models.Model):
	character = models.ForeignKey(Character)
	attribute = models.ForeignKey(Attribute)
	value = models.SmallIntegerField()

	class Meta():
		unique_together = ('character', 'attribute')

	def __unicode__(self):
		return unicode(self.character) + '_' + unicode(self.attribute)

class CharacterSkill(models.Model):
	character = models.ForeignKey(Character)
	skill = models.ForeignKey(Skill)
	value = models.SmallIntegerField()

	class Meta():
		unique_together = ('character', 'skill')

	def __unicode__(self):
		return unicode(self.character) + '_' + unicode(self.skill)

class CharacterSkillTraining(models.Model):
	character = models.ForeignKey(Character)
	skill = models.ForeignKey(Skill)
	value = models.ForeignKey(SkillTrainingLevel)

	class Meta():
		unique_together = ('character', 'skill')

	def __unicode__(self):
		return unicode(self.character) + '_' + unicode(self.skill)

class CharacterFeat(models.Model):
	character = models.ForeignKey(Character)
	feat = models.ForeignKey(Feat)

	class Meta():
		unique_together = ('character', 'feat')

	def __unicode__(self):
		return unicode(self.character) + '_' + unicode(self.feat)

class Setting(models.Model):
	name = models.CharField(max_length=100)
	value = models.CharField(max_length=100)

	class Meta():
		unique_together = ('name',)

	def __unicode__(self):
		return unicode(self.name)

class RacialAttrModifier(models.Model):
	race = models.ForeignKey(Race)
	attribute = models.ForeignKey(Attribute)
	gender = models.ForeignKey(Gender)
	value = models.IntegerField()

	class Meta():
		unique_together = ('race', 'gender', 'attribute')

	def __unicode__(self):
		return unicode(self.race) + '_' + unicode(self.gender) + '_' + unicode(self.attribute)

class RacialFeat(models.Model):
	race = models.ForeignKey(Race)
	feat = models.ForeignKey(Feat)

	class Meta():
		unique_together = ('race', 'feat')

	def __unicode__(self):
		return unicode(self.race)
