import { createP, removeAllChildNodes } from '../utils/helpers.js'

export default class Stopwatch {
	// Create an instance of Stopwatch with basic functionality

	constructor(buttons, elapsedTimeParagraph) {
		// TIME region
		this.totalElapsedTime = 0;
		this.overallTime = 0;
		this.totalElapsedLaps = 0;
		this.perLapTime = 0;
		this.startTime;
		this.interval;
		// end of TIME region

		// CONTENT region
		this.buttonsDiv = document.getElementsByClassName('stopwatch_buttons')[0];
		this.lapsDiv = {
			'isSet': false,
			'laps': document.getElementById('_laps'),
			'lapTimes': document.getElementById('_lap_times'),
			'overallTime': document.getElementById('_overall_time'),
		}
		this.buttonsObj = buttons;
		this.elapsedTimeParagraph = elapsedTimeParagraph;
		// end of CONTENT region

		// FLAG region
		this.isActiveResumeBtn = false;
		// end if FLAG region
	}

	printToElement(element, content) {
		// Set content to desired element 
		element.innerHTML = content;
	}

	updateTime() {
		// Count time difference - `timeDelta` between `startTime`, which is variable
		// set when user presses START button and `actualTime`, which updates 
		// every iteration of `updateTime` function
		let actualTime = new Date().getTime();
		let timeDeltaReal = Math.abs(this.startTime - actualTime);
		let timeDeltaDisp = (timeDeltaReal / 1000).toFixed(1);
		this.totalElapsedTime = timeDeltaReal;

		// Update DOM element with actual `timeDelta`
		this.printToElement(this.elapsedTimeParagraph, timeDeltaDisp);
	}

	start() {
		// function is called after pressing `START` button
		// set actual timestamp to `this.startTime` var
		this.startTime = new Date().getTime() - this.totalElapsedTime;

		// if `RESUME` button was not clicked, set `STOP` and `LAP` buttons
		if (!this.isActiveResumeBtn) {
			this.buttonsDiv.removeChild(this.buttonsObj.startButton);
			this.buttonsDiv.appendChild(this.buttonsObj.stopButton);
			this.buttonsDiv.appendChild(this.buttonsObj.lapButton);
		}

		this.isActiveResumeBtn = false;

		// count `timeDelta` in infinite loop
		this.interval = setInterval(this.updateTime.bind(this), 100);
	}

	stop() {
		// function is called after pressing `STOP` button
		// break from an infinite loop
		clearInterval(this.interval);

		// set `RESUME` and `RESET` buttons
		this.buttonsDiv.removeChild(this.buttonsObj.stopButton);
		this.buttonsDiv.removeChild(this.buttonsObj.lapButton);
		this.buttonsDiv.appendChild(this.buttonsObj.resumeButton);
		this.buttonsDiv.appendChild(this.buttonsObj.resetButton);
	}

	reset() {
		// function is called after pressing `RESET` button
		// set vars of `Stopwatch` class to init values
		this.totalElapsedTime = 0.0;
		this.overallTime = 0.0;
		this.totalElapsedLaps = 0.0;
		this.perLapTime = 0.0;

		// set `0` as init value on main board
		this.printToElement(this.elapsedTimeParagraph, 0);

		// set `START` button
		this.buttonsDiv.removeChild(this.buttonsObj.resumeButton);
		this.buttonsDiv.removeChild(this.buttonsObj.resetButton);
		this.buttonsDiv.appendChild(this.buttonsObj.startButton);

		// reset board with laps
		removeAllChildNodes(this.lapsDiv.laps);
		removeAllChildNodes(this.lapsDiv.lapTimes);
		removeAllChildNodes(this.lapsDiv.overallTime);

		this.lapsDiv.isSet = false;
	}

	resume() {
		// function is called after pressing `RESET` button
		this.isActiveResumeBtn = true;

		// set `STOP` and `LAP` buttons
		this.buttonsDiv.removeChild(this.buttonsObj.resumeButton);
		this.buttonsDiv.removeChild(this.buttonsObj.resetButton);
		this.buttonsDiv.appendChild(this.buttonsObj.stopButton);
		this.buttonsDiv.appendChild(this.buttonsObj.lapButton);

		// continue with infinite loop which counts `timeDelta`
		this.start();
	}

	lap() {
		// function is called after pressing `LAP` button
		// count `perLapTime` and `overallTime` values and increment `totalElapsedLaps` var
		this.perLapTime = this.totalElapsedTime - this.overallTime;
		this.overallTime += this.perLapTime;
		this.totalElapsedLaps++;

		// create and initialize `p` tag elements 
		let pLeft = null;
		let pMiddle = null;
		let pRight = null;

		// if `LAP` button was not pressed yet, create a header of lap board
		if (!this.lapsDiv.isSet) {
			pLeft = createP('lap', 'Lap');
			pMiddle = createP('lap_times', 'Lap times');
			pRight = createP('overall_time', 'Overall time');

			this.lapsDiv.laps.appendChild(pLeft);
			this.lapsDiv.lapTimes.appendChild(pMiddle);
			this.lapsDiv.overallTime.appendChild(pRight);
			this.lapsDiv.isSet = true;
		}

		// if there are more than 4 laps on lap board, after next click on `LAP` button
		// remove the oldest counted lap
		if (this.lapsDiv.laps.childElementCount == 5) {
			this.lapsDiv.laps.removeChild(this.lapsDiv.laps.children[4]);
			this.lapsDiv.lapTimes.removeChild(this.lapsDiv.lapTimes.children[4]);
			this.lapsDiv.overallTime.removeChild(this.lapsDiv.overallTime.children[4]);
		}

		// update lap board with times
		pLeft = createP('lap', this.totalElapsedLaps);
		pMiddle = createP('lap_times', (this.perLapTime / 1000).toFixed(1));
		pRight = createP('overall_time', (this.overallTime / 1000).toFixed(1));

		this.lapsDiv.laps.insertBefore(pLeft, this.lapsDiv.laps.children[1]);
		this.lapsDiv.lapTimes.insertBefore(pMiddle, this.lapsDiv.lapTimes.children[1]);
		this.lapsDiv.overallTime.insertBefore(pRight, this.lapsDiv.overallTime.children[1]);
	}
}
