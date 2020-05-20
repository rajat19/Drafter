function capitalize(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}

function getWrestlersData(ids) {
	$.ajax({
		type: 'GET',
		url: '/wwe/api/wrestlers/',
		success: function(response) {
			var customData = {};
			response.forEach(el => {
				customData[el] = null;
			});
			if (!Array.isArray(ids)) {
				ids = [ids];
			}
			for(var id of ids) {
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

function handleFormResponse(response, param = '') {
	if(response.result == 1) {
		Materialize.toast(response.message, 3000, 'rounded');
	}
	else {
		e = response.errors;
		errorParentId = '#error-parent';
		errorId = '#error';
		if (param !== '') {
			errorParentId += `-${param}`;
			errorId += `-${param}`;
		}
		$(errorParentId).css('display', 'block');
		var html = ''
		for(k in e) {
			var s = `${capitalize(k)}: ${e[k][0].message}`;
			var html = `${html}<strong>${s}</strong>`;
		}
		// Materialize.toast(html, 3000, 'rounded');
		$(errorId).html(html);
	}
}

function deleteRequest(type, slug) {
	const csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
	$.post(`/wwe/${type}/${slug}/delete/`, {
		csrfmiddlewaretoken,
	},
	function(response, status) {
		if (response === 'deleted') {
			$(`#${type}-${slug}`).html('');
		}
	});
}

function confirmDelete(type, slug) {
	swal({
		title: "Confirm Deletion",
		text: `Are you sure about deleting ${slug} ?`,
		type: "warning",
		showCancelButton: true,
		showLoaderOnConfirm: true,
		confirmButtonText: 'Yes, delete it!',
	}).then((result) => {
		deleteRequest(type, slug);
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
	$('.sort-table').tablesorter({
		theme: 'materialize',
		widthFixed: true,
		// use the zebra stripe widget if you plan on hiding any rows (filter widget)
		widgets: ['filter', 'zebra'],
		widgetOptions: {
			zebra: ['even', 'odd'],
			filter_cssfilter: ['', '', 'browser-default'],
		},
	})
	.tablesorterPager({
		container: $('.ts-pager'),
		cssGoto: '.pagenum',
		removeRows: false,
		output: '{startRow} - {endRow} / {filteredRow} ({totalRows})'
	});
}

$(document).ready(() => {
	initializeClasses();
});
