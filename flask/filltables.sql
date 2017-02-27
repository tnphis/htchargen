set autocommit=0;

insert into genders (gender_name) values ('Male'), ('Female');

insert into races (race_name) values ('Remian'), ('Atlantean'), ('Tianean'), ('Ineit'), ('Shagran');

insert into attributes (attribute_code, attribute_name) values ('str', 'Strength'),
('con', 'Constitution'), ('bdy', 'Body'), ('dex', 'Dexterity'), ('spd', 'Speed'),
('per', 'Perception'), ('int', 'Intellect'), ('cha', 'Charisma'), ('wil', 'Willpower');

insert into social_backgrounds (background_name, starting_wealth, point_cost) values
('Homeless', 200, -5), ('Working class', 1000, 0), ('Middle class', 5000, 5), ('Aristocrat', 25000, 10);

insert into skill_groups (skill_group_name) values ('Combat skills'), ('General skills'), ('Infiltration skills'), ('Technological skills');

--now we actually need to know the group ids! They would be variable!
--we may also set the ids explicitly but that would be boring.
/*| 1                   | Combat skills         |
  | 2                   | General skills        |
  | 3                   | Infiltration skills   |
  | 4                   | Technological skills  |*/
  /*ditching bodibuilding for skills... - GUNS!!*/
insert into skills (skill_name, group_id, primary_attribute, secondary_attribute) values
('Fencing', 1, 'dex', 'str'),
('Martial Arts', 1, 'dex', 'str'),
('Throwing', 1, 'dex', 'str'),
('Archery', 1, 'per', 'str'),
('Evasion', 1, 'spd', 'dex'),
('Leadership', 1, 'int', 'wil'),
('Tactical Analysis', 1, 'per', 'int'),
('Athletics', 2, 'con', 'str'),
('Diplomacy', 2, 'cha', 'int'),
('Mercantile', 2, 'wil', 'cha'),
('Medicine', 2, 'int', 'per'),
('Survival', 2, 'con', 'wil'),
('Animal taming', 2, 'wil', 'int'),
('Stealth', 3, 'per', 'dex'),
('Lockpicking', 3, 'dex', 'per'),
('Pickpocketing', 3, 'dex', 'per'),
('Backstabbing', 3, 'per', 'int'),
('Traps', 3, 'dex', 'int'),
('Chemistry', 4, 'int', 'per'),
('Explosives', 4, 'int', 'per'),
('Electromagnetism', 4, 'int', 'per'),
('Mechanics', 4, 'int', 'dex'),
('Therapeutics', 4, 'int', 'per'),
('Metallurgy', 4, 'int', 'str')
('Firearms', 1, 'per', 'dex'),;

insert into skill_training_levels (training_level_name) values ('Expert'), ('Master');

insert into feat_types (feat_type_name) values ('Trait'), ('Racial'), ('Acquired');

insert into settings (name, value) values ('level_cap', 35), ('points_per_level', 6),
('attribute_cost', 1), ('skill_cost', 3), ('skill_attr_cap_primary', 15),
('skill_attr_cap_secondary', 12), ('skill_attr_cap_threshold_primary', 1),
('skill_attr_cap_threshold_secondary', 2), ('skill_attr_cap_per_lvl_primary', 7),
('skill_attr_cap_per_level_secondary', 5), ('base_attribute_value', 15), ('base_character_points', 30);
