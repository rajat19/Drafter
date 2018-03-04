// FIXME: call only on particular files
$(document).ready(function() {
	$(function() {
		$.ajax({
			type: 'GET',
			url: '/wwe2k16/api/wrestlers/',
			success: function(response) {
				// console.log(response);
				var customData = {};
				response.forEach(el => {
					customData[el] = null;
				});
				$('#id_champion').material_chip({
					autocompleteOptions: {
						data: customData,
						limit: Infinity,
						minLength: 1,
					}
				});
			}
		});
	});
});