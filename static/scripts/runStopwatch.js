import Stopwatch from './classes/stopwatch.js'

let startButton = document.getElementById('sw_start_btn');
let stopButton = document.getElementById('sw_stop_btn');
let elapsedTimeParagraph = document.getElementById('elapsedTime')

let stopwatch = new Stopwatch(startButton, stopButton, elapsedTimeParagraph);

function eventClicker() {
	stopwatch.start();
}

function removeEventClicker() {
	startButton.removeEventListener('click', eventClicker);
}

startButton.addEventListener('click', eventClicker);
stopButton.addEventListener('click', removeEventClicker);
