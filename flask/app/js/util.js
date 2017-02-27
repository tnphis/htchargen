//a non-model view to login the users
define([], function() {
	"use strict";
	return {
		validate_email : function(p_str) {
			if (!(p_str)) {
				return false
			} else {
				if (
					p_str.indexOf('@') >= 0
					&& p_str.indexOf('.', p_str.indexOf('@')) >= 0
					&& p_str.indexOf('.', p_str.indexOf('@')) < p_str.length - 1
				) {
					return true
				} else {
					return false
				}
			}
		}
	}
})
