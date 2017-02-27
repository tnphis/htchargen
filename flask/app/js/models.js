define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
	"use strict";
	return {
		Character : Backbone.Model.extend({
			initialize : function() {
				console.log('char model initialized', Global.settings, this.id)
				this.on('change:skills', function(model, newval) {
					var oldval = model.previous('skills')
					if (oldval) {
						var old_pts = Number(model.get('points'))
						var new_pts = Number(old_pts) //clone
						for (var i = 0, glen = Global.settings.client.skill_groups.length; i < glen; i++) {
							var g = Global.settings.client.skill_groups[i]
							for (var j = 0, slen = newval[g].length; j < slen; j++) {
								if (newval[g][j].value != oldval[g][j].value) {
									new_pts = new_pts - (newval[g][j].value - oldval[g][j].value) * Global.settings.skill_cost
								}
							}
						}
						if (new_pts >= 0) {
							model.set('points', new_pts)
						} else {
							model.set('skills', oldval)
							this.trigger('custom_error', ['Not enough points!'])
						}
					}
				})

				this.on('change:attributes', function(model, newval) {
					var oldval = model.previous('attributes')
					if (oldval) {
						var old_pts = Number(model.get('points'))
						var new_pts = Number(old_pts) //clone
						for (var i = 0, len = newval.length; i < len; i++) {
							if (newval[i].value != oldval[i].value) {
								new_pts = new_pts - (newval[i].value - oldval[i].value) * Global.settings.attribute_cost
							}
						}
						if (new_pts >= 0) {
							model.set('points', new_pts)
						} else {
							model.set('attributes', oldval)
							this.trigger('custom_error', ['Not enough points!'])
						}
					}
				})

				this.on('change:social_background', function(model, newval) {
					//no resetting
					if (model.previous('social_background') && !newval) {
						model.set('social_background', model.previous('social_background'))
					}

					var current_background = _.find(Global.settings.objects.social_backgrounds, function(a) {return a.id == newval})

					if (current_background) {
						var previous_background
						if (model.previous('social_background')) {
							previous_background = _.find(Global.settings.objects.social_backgrounds, function(a) {return a.id == model.previous('social_background')})
						} else {
							//it's undefined on syncing!
							if (model.get('id') == -1) {
								previous_background = _.find(Global.settings.objects.social_backgrounds, function(a) {return a.point_cost == 0})
							} else {
								previous_background = current_background
							}
						}

						console.log(Global.settings.objects.social_backgrounds, current_background, previous_background, newval)

						var new_pts = model.get('points') - current_background['point_cost'] + previous_background['point_cost']

						if (new_pts >= 0) {
							model.set('points', new_pts)
							model.set('wealth', current_background['starting_wealth'])
						} else {
							model.set('social_background', model.previous('social_background'))
							this.trigger('custom_error', ['Not enough points!'])
						}
					}
				})
			},
			url : function() {
				return '/api?get_character=true&character_id=' + this.id
			},
			parse : function(resp, xhr) {
				console.log('parsing', resp)
				if (!resp.success) {
					alert('Error: ' + resp.error_desc)
				}
				return resp.data
			},
			validate: function(attrs, options) {
				var errors = []
				if (!attrs.name.length) {
					errors.push('Name')
				}
				if (!attrs.race) {
					errors.push('Race')
				}
				if (!attrs.gender) {
					errors.push('Gender')
				}
				if (!attrs.social_background) {
					errors.push('Social background')
				}

				if (errors.length > 0) {
					return errors
				}
			},
			get_skill_cap_by_type: function(skill, type) {
				var thresh, attr, min_val, pl
				if (type == 'primary') {
					attr = _.find(this.get('attributes'), function(a) {return a.code == skill.primary_attribute})
					thresh = Global.settings.skill_attr_cap_threshold_primary
					pl = Global.settings.skill_attr_cap_per_lvl_primary
					min_val = Global.settings.skill_attr_cap_primary
				} else if (type == 'secondary') {
					attr = _.find(this.get('attributes'), function(a) {return a.code == skill.secondary_attribute})
					thresh = Global.settings.skill_attr_cap_threshold_secondary
					pl = Global.settings.skill_attr_cap_per_lvl_secondary
					min_val = Global.settings.skill_attr_cap_secondary
				}

				//console.log(thresh, attr, min_val, pl)
				return (thresh - 1) + Math.ceil((attr.value - min_val + 1) / pl)
			},
			get_skill_cap: function(skill) {
				var primary_cap = this.get_skill_cap_by_type(skill, 'primary')
				var secondary_cap = this.get_skill_cap_by_type(skill, 'secondary')

				return Math.min(primary_cap, secondary_cap)
			},
			get_attr_requirements: function(skill) {
				if (skill.value == 6) {
					return null
				} else {
					var return_txt = ''
					var primary_attr = _.find(this.get('attributes'), function(a) {return a.code == skill.primary_attribute})
					var secondary_attr = _.find(this.get('attributes'), function(a) {return a.code == skill.secondary_attribute})

					/*var next_value_primary = this.get_skill_cap_by_type(skill, 'primary') + 1
					var next_value_secondary = this.get_skill_cap_by_type(skill, 'secondary') + 1*/
					var next_value = this.get_skill_cap(skill) + 1

					var primary_req = 0
					if (next_value >= Global.settings.skill_attr_cap_threshold_primary) {
						primary_req = Number(Global.settings.skill_attr_cap_primary) + (next_value - Global.settings.skill_attr_cap_threshold_primary) * Global.settings.skill_attr_cap_per_lvl_primary
					}
					var secondary_req = 0
					if (next_value >= Global.settings.skill_attr_cap_threshold_secondary) {
						secondary_req = Number(Global.settings.skill_attr_cap_secondary) + (next_value - Global.settings.skill_attr_cap_threshold_secondary) * Global.settings.skill_attr_cap_per_lvl_secondary
					}

					if (primary_req > primary_attr.value) {
						return_txt += 'Minimum ' + skill.primary_attribute + ' required: ' + primary_req
					}
					if (secondary_req > secondary_attr.value) {
						if (primary_req > primary_attr.value) {
							return_txt += '\n'
						}
						return_txt += 'Minimum ' + skill.secondary_attribute + ' required: ' + secondary_req
					}
					if (skill.name == 'Leadership') {
						console.log(next_value, primary_req, secondary_req, skill, primary_attr, secondary_attr)
					}
					if (return_txt == '') {
						return null
					} else {
						return return_txt
					}
				}
			}
		}),
		CharacterListItem : Backbone.Model.extend({
			//not sure what to use here for now...
		})
	}
})
