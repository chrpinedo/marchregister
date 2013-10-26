function check_email(input) {
	if (input.value != document.getElementById('email').value) {
		input.setCustomValidity('Bi email helbideak berdinak izan behar dira. Las dos direcciones de email deben coincidir.');
	} else {
		input.setCustomValidity('');
	}
	validate_email(input)
}
function check_id_number(input) {
	if (input.value != document.getElementById('id_number').value) {
		input.setCustomValidity('Bi IZF-ak berdinak izan behar dira. Los dos NIF deben coincidir.');
	} else {
		input.setCustomValidity('');
	}
	validate_id_number(input)
}
function validate_email(input) {
	var re = /^[^ ]+@[^ ]+\.[^ ]+/
	if (re.test(input.value)) {
		input.setCustomValidity('');
	} else {
		input.setCustomValidity('Email helbidea ez da baliozkoa. La dirección de email no es válida.');
	}
}
function validate_id_number(input) {
	var re = /^[0-9]+[A-Z]/
	if (re.test(input.value)) {
		input.setCustomValidity('');
	} else {
		input.setCustomValidity('IZF ez da baliozkoa. El NIF no es válido.');
	}
}
function validate_born_date(input) {
	var re = /^[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}/
	if ( ! re.test(input.value)) {
		input.setCustomValidity('Data ez da baliozkoa. La fecha no es válida.');
		return;
	} 
	var items = input.value.split("-");
	if (parseInt(items[0], 10) > 31) {
		input.setCustomValidity('Data ez da baliozkoa. La fecha no es válida.');
	} else if (parseInt(items[1], 10) > 12) {
		input.setCustomValidity('Data ez da baliozkoa. La fecha no es válida.');
	} else {
		input.setCustomValidity('');
	}
}

