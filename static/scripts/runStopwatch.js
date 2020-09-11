import Stopwatch from './classes/stopwatch.js'
import { createButton } from './utils/helpers.js'

// BUTTONS region
let buttons = {
	'startButton': document.getElementById('sw_start_btn'),
	'stopButton': createButton('stop'),
	'resetButton': createButton('reset'),
	'resumeButton': createButton('resume'),
	'lapButton': createButton('lap')
}
// end of BUTTONS region

// MAIN BOARD region
let elapsedTimeParagraph = document.getElementById('elapsedTime');
// end of MAIN BOARD region

// STOPWATCH object initialization
let stopwatch = new Stopwatch(buttons, elapsedTimeParagraph);

// EVENT LISTENERS region 
buttons.startButton.addEventListener('click', eventClickerStart);
buttons.stopButton.addEventListener('click', eventClickerStop);
buttons.resetButton.addEventListener('click', eventClickerReset);
buttons.resumeButton.addEventListener('click', eventClickerResume);
buttons.lapButton.addEventListener('click', eventClickerLap);

function eventClickerStart() { stopwatch.start(); }
function eventClickerStop() { stopwatch.stop(); }
function eventClickerReset() { stopwatch.reset(); }
function eventClickerResume() { stopwatch.resume(); }
function eventClickerLap() { stopwatch.lap(); }
// end of EVENT LISTENERS region
