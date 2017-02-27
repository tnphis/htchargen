//utility skillbar view options: id, value, min, max, [cap]

var SkillBarView = Backbone.View.extend({
	//el: $("#viewcontainer"),
	initialize : function(options) {
		this.options = options || {} //why not??
		if (this.options.cap === undefined) {
			this.options.cap = this.options.max
		}
	},
	tagName: 'span',
	events: {
		'click #btn_increase' : 'increase_value', //using ids won't work, it's called before initialize!
		'click #btn_decrease' : 'decrease_value'
	},
	drawboxes: function() {
		var boxesel = this.$el.find('#' + this.options.id + '_boxes')
		var value_txt = ''
		for (var i = 0; i < this.options.value; i++) {
			value_txt += '&rtrif;'//'&FilledSmallSquare;'
		}
		for (var i = 0; i < this.options.cap - this.options.value; i++) {
			value_txt += '&rtri;'//'&EmptySmallSquare;'
		}
		
		for (var i = 0; i < this.options.max - this.options.cap; i++) {
			value_txt += '<span class="skillbar-grayed">&rtri;</span>'//'&EmptySmallSquare;'
		}		
		
		boxesel.html(value_txt)
		
		if (this.options.value >= this.options.cap) {
			this.$el.find('#btn_increase').attr('disabled', 'true')
		} else {
			this.$el.find('#btn_increase').removeAttr('disabled')
		}
		if (this.options.value <= this.options.min) {
			this.$el.find('#btn_decrease').attr('disabled', 'true')
		} else {
			this.$el.find('#btn_decrease').removeAttr('disabled')
		}		
	},
	render: function(){
		var that = this
		require([
			'text',
			'text!' + Global.config.staticdir + '/templates/skillbar.html'
		], function(text, skillbarTemplate) {
			if (!Global.templates['skillbar']) {
				Global.templates['skillbar'] = _.template(skillbarTemplate)
			}
			that.template = Global.templates['skillbar']			
			that.$el.html(that.template(that.options))
			
			that.inputel = that.$el.find('input')
			that.inputel.val(that.options.value)
			
			that.drawboxes()
			
			if (that.options.afterdraw) {
				//console.log(that)
				that.options.afterdraw(that)
			}
		});
	},
	increase_value : function() {
		if (this.options.value < this.options.cap) {
			this.options.value += 1
			this.drawboxes()
			this.inputel.val(this.options.value)
			this.inputel.trigger('change')			
		}
	},
	decrease_value : function() {
		if (this.options.value > this.options.min) {
			this.options.value -= 1
			this.drawboxes()
			//console.log(this.options.value)
			this.inputel.val(this.options.value)
			this.inputel.trigger('change')							
		}
	}/*,
	get_inputel : function() {
		if (!this.inputel) {
			alert('smth is wrong with inputel')
		} else {
			return this.inputel
		}
	}*/
});

return SkillBarView;