function check_email(input) {
	if (input.value != document.getElementById('email').value) {
		input.setCustomValidity('Las dos direcciones de email deben coincidir');
	} else {
		input.setCustomValidity('');
	}
	validate_email(input)
}
function check_id_number(input) {
	if (input.value != document.getElementById('id_number').value) {
		input.setCustomValidity('Las dos NIF deben coincidir');
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
		input.setCustomValidity('No se ha introducido una dirección de email válida');
	}
}
function validate_id_number(input) {
	var re = /^[0-9]+[A-Z]/
	if (re.test(input.value)) {
		input.setCustomValidity('');
	} else {
		input.setCustomValidity('No se ha introducido un DNI válido');
	}
}
function validate_born_date(input) {
	var re = /^[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}/
	if ( ! re.test(input.value)) {
		input.setCustomValidity('No se ha introducido una fecha válida');
		return;
	} 
	var items = input.value.split("-");
	if (parseInt(items[0], 10) > 31) {
		input.setCustomValidity('No se ha introducido una fecha válida');
	} else if (parseInt(items[1], 10) > 12) {
		input.setCustomValidity('No se ha introducido una fecha válida');
	} else {
		input.setCustomValidity('');
	}
}

