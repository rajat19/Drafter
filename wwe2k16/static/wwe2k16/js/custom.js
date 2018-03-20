function capitalize(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}

function getWrestlersData(ids) {
	$.ajax({
		type: 'GET',
		url: '/wwe2k16/api/wrestlers/',
		success: function(response) {
			var customData = {};
			response.forEach(el => {
				customData[el] = null;
			});
			if (!Array.isArray(ids)) {
				ids = [ids];
			}
			for(var id in ids) {
				$(`#id_${id}`).material_chip({
					autocompleteOptions: {
						data: customData,
						limit: Infinity,
						minLength: 1,
					}
				});
			}
		}
	});
}

function handleResponse(response) {
	if(response.result == 1) {
		Materialize.toast(response.message, 3000, 'rounded')
	}
	else {
		e = response.errors;
		$('#error-parent').css('display', 'block');
		var html = ''
		for(k in e) {
			var s = `${capitalize(k)}: ${e[k][0].message}`;
			var html = `${html}<strong>${s}</strong>`;
		}
		$('#error').html(html);
	}
}

function confirmDelete(type, slug) {
	const csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
	swal({
		title: "Confirm Deletion",
		text: `Are you sure about deleting ${slug} ?`,
		type: "warning",
		showCancelButton: true,
		showLoaderOnConfirm: true,
		confirmButtonText: 'Yes, delete it!',
	}).then((result) => {
		$.post(`/wwe2k16/${type}/delete/`, {
			csrfmiddlewaretoken,
			slug,
		},
		function(response, status) {
			if (response === 'deleted') {
				$(`#${type}-${slug}`).html('');
			}
		});
	});
}

function initializeClasses() {
	Materialize.updateTextFields();
	$(".button-collapse").off("click").sideNav();
	$('#sidenav-overlay').remove();
	$('select').material_select();
	$('.modal').modal({
		dismissible: true,
		opacity: .5,
	});
	$('.materialize-textarea').trigger('autoresize');
	$('.ul.tabs').tabs();
	$('.datepicker').pickadate({
		selectMonths: true,
		selectYears: 15,
		format: 'dddd, dd mmm, yyyy',
		formatSubmit: 'yyyy-mm-dd',
		hiddenName: true,
	});
	$('.chips').material_chip();
}

$(document).ready(() => {
	initializeClasses();
});
