create table users (
	user_id int auto_increment primary key,
	user_name varchar(50) not null,
	email varchar(200) not null,
	password_hash varchar(256) not null,
	constraint user_name_uk unique (user_name),
	constraint user_email_uk unique (email)
);

create table races (
	race_id int auto_increment primary key,
	race_name varchar(50) not null,
	constraint race_name_uk unique (race_name)
);

create table genders (
	gender_id smallint auto_increment primary key,
	gender_name varchar(10) not null,
	constraint gender_name_uk unique (gender_name)
);

create table attributes (
	attribute_code varchar(3) not null primary key,
	attribute_name varchar(50) not null,
	constraint attribute_name_uk unique (attribute_name)
);

create table social_backgrounds (
	background_id int auto_increment primary key,
	background_name varchar(50) not null,
	starting_wealth int unsigned not null,
	point_cost int not null,
	constraint background_name_uk unique (background_name)
);

create table skill_groups (
	skill_group_id int auto_increment primary key,
	skill_group_name varchar(50) not null,
	constraint skill_group_name_uk unique (skill_group_name)
);

create table skills (
	skill_id int auto_increment primary key,
	group_id int not null,
	skill_name varchar(50) not null,
	primary_attribute varchar(3) not null,
	secondary_attribute varchar(3) not null,
	foreign key (group_id) references skill_groups(skill_group_id),
	foreign key (primary_attribute) references attributes(attribute_code),
	foreign key (secondary_attribute) references attributes(attribute_code),
	constraint skill_name_uk unique (skill_name)
);

create table skill_training_levels (
	training_level_id int auto_increment primary key,
	training_level_name varchar(50) not null,
	constraint training_level_name_uk unique (training_level_name)
);

create table feat_types (
	feat_type_id int auto_increment primary key,
	feat_type_name varchar(50) not null,
	constraint feat_type_name_uk unique (feat_type_name)
);

create table feats (
	feat_id int auto_increment primary key,
	type_id int not null,
	feat_name varchar(100) not null,
	feat_description varchar(4000) not null,
	point_cost int not null,
	foreign key (type_id) references feat_types(feat_type_id),
	constraint feat_uk unique (feat_name)
);

create table characters (
	character_id int auto_increment primary key,
	owner_id int not null,
	name varchar(200) not null,
	level int not null,
	gender_id smallint not null,
	race_id int not null,
	social_background_id int not null,
	point_pool int not null,
	wealth int not null,
	portrait_url varchar(1000), --this can be null!!
	foreign key (owner_id) references users(user_id),
	foreign key (gender_id) references genders(gender_id),
	foreign key (race_id) references races(race_id),
	foreign key (social_background_id) references social_backgrounds(background_id),
	constraint char_name_uk unique (name)
);

create table character_attributes (
	character_id int not null,
	attribute_code varchar(3) not null,
	attribute_value int not null,
	foreign key (character_id) references characters(character_id),
	foreign key (attribute_code) references attributes(attribute_code),
	constraint char_attrs_uk unique (character_id, attribute_code)
);

create table character_skills (
	character_id int not null,
	skill_id int not null,
	skill_value int not null,
	foreign key (character_id) references characters(character_id),
	foreign key (skill_id) references skills(skill_id),
	constraint char_skills_uk unique (character_id, skill_id)
);

create table character_skill_training (
	character_id int not null,
	skill_id int not null,
	skill_training_id int not null,
	foreign key (character_id) references characters(character_id),
	foreign key (skill_id) references skills(skill_id),
	foreign key (skill_training_id) references skill_training_levels(training_level_id),
	constraint char_skill_training_uk unique (character_id, skill_id)
);

create table character_feats (
	character_id int not null,
	feat_id int not null,
	foreign key (character_id) references characters(character_id),
	foreign key (feat_id) references feats(feat_id),
	constraint char_feats_uk unique (character_id, feat_id)
);

create table racial_attr_modifiers (
	race_id int not null,
	attribute varchar(3) not null,
	gender_id smallint not null,
	value int,
	foreign key (race_id) references races(race_id),
	foreign key (attribute) references attributes(attribute_code),
	foreign key (gender_id) references genders(gender_id),
	constraint racial_attrs_uk unique (race_id, attribute_code, gender_id)
);

create table racial_feats (
	race_id int not null,
	feat_id int not null,
	foreign key (race_id) references races(race_id),
	foreign key (feat_id) references feats(feat_id),
	constraint racial_feats_uk unique (race_id, feat_id)
);

create table settings (
	setting_id int auto_increment primary key,
	name varchar(100) not null,
	value varchar(100) not null,
	constraint settings_uk unique (name, value)
);
