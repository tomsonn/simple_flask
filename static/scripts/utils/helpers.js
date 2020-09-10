function BadButtonType(errorMessage, type) {
	const error = new Error(errorMessage);
	error.buttonType = type;

	return error;
}

function BadParagraphType(errorMessage, type) {
	const error = new Error(errorMessage);
	error.buttonType = type;

	return error;
}

export function createButton(buttonType) {
	// Create a DOM element based on type, which is passed as parameter to function
	// elements type is `input` with `type=button`);
	// If bad type is passed to function as parameter, an exceptions is thrown

	let button = document.createElement('input');
	button.setAttribute('type', 'button');
	button.setAttribute('class', 'stopwatch_button');

	if (buttonType == 'stop') {
		button.setAttribute('id', 'sw_stop_btn');
		button.setAttribute('value', 'STOP');
	} else if (buttonType == 'reset') {
		button.setAttribute('id', 'sw_reset_btn');
		button.setAttribute('value', 'RESET');
	} else if (buttonType == 'resume') {
		button.setAttribute('id', 'sw_resume_btn');
		button.setAttribute('value', 'RESUME');
	} else if (buttonType == 'lap') {
		button.setAttribute('id', 'sw_lap_btn');
		button.setAttribute('value', 'LAP');
	} else {
		throw new BadButtonType('Couldn\'t create desired button.');
	}

	return button;
}

export function createP(type, content) {
	let p = document.createElement('p');

	if (type == 'lap') {
		(content == 'Lap') ? p.setAttribute('class', 'left title') : p.setAttribute('class', 'left time');
		p.innerHTML = content;
	} else if (type == 'lap_times') {
		(content == 'Lap times') ? p.setAttribute('class', 'middle title') : p.setAttribute('class', 'middle time');
		p.innerHTML = content;
	} else if (type == 'overall_time') {
		(content == 'Overall time') ? p.setAttribute('class', 'right title') : p.setAttribute('class', 'right time');
		p.innerHTML = content;
	} else {
		throw new BadParagraphType('Couldn\'t create desired paragraph.');
	}

	return p;
}

export function removeAllChildNodes(parent) {
	while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}
