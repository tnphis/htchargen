import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'htchargen.settings'
django.setup()

from chargenapp.models import *

#genders
Gender.objects.all().delete()

current_obj = Gender(value='Male')
current_obj.save()

current_obj = Gender(value='Female')
current_obj.save()

#races
Race.objects.all().delete()

current_obj = Race(name='Remian')
current_obj.save()

current_obj = Race(name='Atlantean')
current_obj.save()

current_obj = Race(name='Tianean')
current_obj.save()

current_obj = Race(name='Ineit')
current_obj.save()

current_obj = Race(name='Shargran')
current_obj.save()

#attributes
Attribute.objects.all().delete()

current_obj = Attribute(code='str', name='Strength')
current_obj.save()

current_obj = Attribute(code='con', name='Constitution')
current_obj.save()

current_obj = Attribute(code='bdy', name='Body')
current_obj.save()

current_obj = Attribute(code='dex', name='Dexterity')
current_obj.save()

current_obj = Attribute(code='spd', name='Speed')
current_obj.save()

current_obj = Attribute(code='per', name='Perception')
current_obj.save()

current_obj = Attribute(code='int', name='Intellect')
current_obj.save()

current_obj = Attribute(code='cha', name='Charisma')
current_obj.save()

current_obj = Attribute(code='wil', name='Willpower')
current_obj.save()

#social backgrounds
SocialBackground.objects.all().delete()

current_obj = SocialBackground(value='Homeless', starting_wealth=200, point_cost=-5)
current_obj.save()

current_obj = SocialBackground(value='Working class', starting_wealth=1000, point_cost=0)
current_obj.save()

current_obj = SocialBackground(value='Middle class', starting_wealth=5000, point_cost=5)
current_obj.save()

current_obj = SocialBackground(value='Aristocrat', starting_wealth=25000, point_cost=10)
current_obj.save()

#skill groups
SkillGroup.objects.all().delete()

current_obj = SkillGroup(name='Combat')
current_obj.save()

current_obj = SkillGroup(name='General')
current_obj.save()

current_obj = SkillGroup(name='Infiltration')
current_obj.save()

current_obj = SkillGroup(name='Technological')
current_obj.save()

#skills
Skill.objects.all().delete()

##combat
current_obj = Skill(
	name='Fencing', 
	group=SkillGroup.objects.get(name='Combat'),
	primary_attribute=Attribute.objects.get(code='dex'),
	secondary_attribute=Attribute.objects.get(code='str')
)
current_obj.save()

current_obj = Skill(
	name='Martial Arts', 
	group=SkillGroup.objects.get(name='Combat'),
	primary_attribute=Attribute.objects.get(code='dex'),
	secondary_attribute=Attribute.objects.get(code='str')
)
current_obj.save()

current_obj = Skill(
	name='Throwing', 
	group=SkillGroup.objects.get(name='Combat'),
	primary_attribute=Attribute.objects.get(code='dex'),
	secondary_attribute=Attribute.objects.get(code='str')
)
current_obj.save()

current_obj = Skill(
	name='Archery', 
	group=SkillGroup.objects.get(name='Combat'),
	primary_attribute=Attribute.objects.get(code='per'),
	secondary_attribute=Attribute.objects.get(code='str')
)
current_obj.save()

current_obj = Skill(
	name='Evasion', 
	group=SkillGroup.objects.get(name='Combat'),
	primary_attribute=Attribute.objects.get(code='spd'),
	secondary_attribute=Attribute.objects.get(code='dex')
)
current_obj.save()

current_obj = Skill(
	name='Leadership', 
	group=SkillGroup.objects.get(name='Combat'),
	primary_attribute=Attribute.objects.get(code='int'),
	secondary_attribute=Attribute.objects.get(code='wil')
)
current_obj.save()

current_obj = Skill(
	name='Tactical analysis', 
	group=SkillGroup.objects.get(name='Combat'),
	primary_attribute=Attribute.objects.get(code='per'),
	secondary_attribute=Attribute.objects.get(code='int')
)
current_obj.save()

##general
current_obj = Skill(
	name='Athletics', 
	group=SkillGroup.objects.get(name='General'),
	primary_attribute=Attribute.objects.get(code='con'),
	secondary_attribute=Attribute.objects.get(code='str')
)
current_obj.save()

current_obj = Skill(
	name='Bodybuilding', 
	group=SkillGroup.objects.get(name='General'),
	primary_attribute=Attribute.objects.get(code='bdy'),
	secondary_attribute=Attribute.objects.get(code='str')
)
current_obj.save()

current_obj = Skill(
	name='Diplomacy', 
	group=SkillGroup.objects.get(name='General'),
	primary_attribute=Attribute.objects.get(code='cha'),
	secondary_attribute=Attribute.objects.get(code='int')
)
current_obj.save()

current_obj = Skill(
	name='Mercantile', 
	group=SkillGroup.objects.get(name='General'),
	primary_attribute=Attribute.objects.get(code='wil'),
	secondary_attribute=Attribute.objects.get(code='cha')
)
current_obj.save()

current_obj = Skill(
	name='Medicine', 
	group=SkillGroup.objects.get(name='General'),
	primary_attribute=Attribute.objects.get(code='int'),
	secondary_attribute=Attribute.objects.get(code='per')
)
current_obj.save()

current_obj = Skill(
	name='Survival', 
	group=SkillGroup.objects.get(name='General'),
	primary_attribute=Attribute.objects.get(code='wil'),
	secondary_attribute=Attribute.objects.get(code='con')
)
current_obj.save()

current_obj = Skill(
	name='Animal taming', 
	group=SkillGroup.objects.get(name='General'),
	primary_attribute=Attribute.objects.get(code='wil'),
	secondary_attribute=Attribute.objects.get(code='int')
)
current_obj.save()

##infiltration
current_obj = Skill(
	name='Stealth', 
	group=SkillGroup.objects.get(name='Infiltration'),
	primary_attribute=Attribute.objects.get(code='per'),
	secondary_attribute=Attribute.objects.get(code='dex')
)
current_obj.save()

current_obj = Skill(
	name='Lockpicking', 
	group=SkillGroup.objects.get(name='Infiltration'),
	primary_attribute=Attribute.objects.get(code='dex'),
	secondary_attribute=Attribute.objects.get(code='per')
)
current_obj.save()

current_obj = Skill(
	name='Pickpocket', 
	group=SkillGroup.objects.get(name='Infiltration'),
	primary_attribute=Attribute.objects.get(code='dex'),
	secondary_attribute=Attribute.objects.get(code='per')
)
current_obj.save()

current_obj = Skill(
	name='Backstabbing', 
	group=SkillGroup.objects.get(name='Infiltration'),
	primary_attribute=Attribute.objects.get(code='per'),
	secondary_attribute=Attribute.objects.get(code='int')
)
current_obj.save()

current_obj = Skill(
	name='Traps', 
	group=SkillGroup.objects.get(name='Infiltration'),
	primary_attribute=Attribute.objects.get(code='dex'),
	secondary_attribute=Attribute.objects.get(code='int')
) #spotting those will be aided by perception
current_obj.save()

##technological
current_obj = Skill(
	name='Chemistry', 
	group=SkillGroup.objects.get(name='Technological'),
	primary_attribute=Attribute.objects.get(code='int'),
	secondary_attribute=Attribute.objects.get(code='per')
)
current_obj.save()

current_obj = Skill(
	name='Explosives', 
	group=SkillGroup.objects.get(name='Technological'),
	primary_attribute=Attribute.objects.get(code='int'),
	secondary_attribute=Attribute.objects.get(code='per')
)
current_obj.save()

current_obj = Skill(
	name='Electromagnetism', 
	group=SkillGroup.objects.get(name='Technological'),
	primary_attribute=Attribute.objects.get(code='int'),
	secondary_attribute=Attribute.objects.get(code='per')
)
current_obj.save()

current_obj = Skill(
	name='Mechanics', 
	group=SkillGroup.objects.get(name='Technological'),
	primary_attribute=Attribute.objects.get(code='int'),
	secondary_attribute=Attribute.objects.get(code='dex')
)
current_obj.save()

current_obj = Skill(
	name='Therapeutics', 
	group=SkillGroup.objects.get(name='Technological'),
	primary_attribute=Attribute.objects.get(code='int'),
	secondary_attribute=Attribute.objects.get(code='per')
)
current_obj.save()

current_obj = Skill(
	name='Metallurgy', 
	group=SkillGroup.objects.get(name='Technological'),
	primary_attribute=Attribute.objects.get(code='int'),
	secondary_attribute=Attribute.objects.get(code='str')
)
current_obj.save()

current_obj = Skill(
	name='Ballistics', 
	group=SkillGroup.objects.get(name='Technological'),
	primary_attribute=Attribute.objects.get(code='int'),
	secondary_attribute=Attribute.objects.get(code='dex')
)
current_obj.save()

#skill training levels
SkillTrainingLevel.objects.all().delete()

current_obj = SkillTrainingLevel(value='Expert')
current_obj.save()

current_obj = SkillTrainingLevel(value='Master')
current_obj.save()

#default feat types
FeatType.objects.all().delete()

current_obj = FeatType(value='Trait')
current_obj.save()

current_obj = FeatType(value='Racial')
current_obj.save()

current_obj = FeatType(value='Acquired')
current_obj.save()

#feats

#settings
Setting.objects.all().delete()

current_obj = Setting(name='level_cap', value=35)
current_obj.save()

current_obj = Setting(name='points_per_level', value=6)
current_obj.save()

current_obj = Setting(name='attribute_cost', value=1)
current_obj.save()

current_obj = Setting(name='skill_cost', value=3)
current_obj.save()

current_obj = Setting(name='skill_attr_cap_primary', value=15)
current_obj.save()

current_obj = Setting(name='skill_attr_cap_secondary', value=12)
current_obj.save()

current_obj = Setting(name='skill_attr_cap_theshold_primary', value=1)
current_obj.save()

current_obj = Setting(name='skill_attr_cap_threshold_secondary', value=2)
current_obj.save()

current_obj = Setting(name='skill_attr_cap_per_lvl_primary', value=7)
current_obj.save()

current_obj = Setting(name='skill_attr_cap_per_lvl_secondary', value=5)
current_obj.save()

current_obj = Setting(name='base_attribute_value', value=15)
current_obj.save()

current_obj = Setting(name='base_character_points', value=30)
current_obj.save()