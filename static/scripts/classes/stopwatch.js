import { createP, removeAllChildNodes } from '../utils/helpers.js'

export default class Stopwatch {

	constructor(buttons, elapsedTimeParagraph) {
		this.totalElapsedTime = 0;
		this.overallTime = 0;
		this.totalElapsedLaps = 0;
		this.perLapTime = 0;
		this.startTime;
		this.interval;

		this.buttonsDiv = document.getElementsByClassName('stopwatch_buttons')[0];
		this.lapsDiv = {
			'isSet': false,
			'laps': document.getElementById('_laps'),
			'lapTimes': document.getElementById('_lap_times'),
			'overallTime': document.getElementById('_overall_time'),
		}
		this.buttonsObj = buttons;
		
		this.elapsedTimeParagraph = elapsedTimeParagraph;

		this.isActiveResumeBtn = false;
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
		let timeDeltaDisplayed = (timeDeltaReal / 1000).toFixed(1);
		this.totalElapsedTime = timeDeltaReal;
		this.perLapTime = this.totalElapsedTime - this.overallTime;

		// Update DOM element with actual `timeDelta`
		this.printToElement(this.elapsedTimeParagraph, timeDeltaDisplayed);
	}

	start() {
		this.startTime = new Date().getTime() - this.totalElapsedTime;

		if (!this.isActiveResumeBtn) {
			this.buttonsDiv.removeChild(this.buttonsObj.startButton);
			this.buttonsDiv.appendChild(this.buttonsObj.stopButton);
			this.buttonsDiv.appendChild(this.buttonsObj.lapButton);
		}

		this.isActiveResumeBtn = false;

		this.interval = setInterval(this.updateTime.bind(this), 100);
	}

	stop() {
		clearInterval(this.interval);

		this.buttonsDiv.removeChild(this.buttonsObj.stopButton);
		this.buttonsDiv.removeChild(this.buttonsObj.lapButton);
		this.buttonsDiv.appendChild(this.buttonsObj.resumeButton);
		this.buttonsDiv.appendChild(this.buttonsObj.resetButton);
	}

	reset() {
		this.totalElapsedTime = 0;
		this.overallTime = 0;
		this.totalElapsedLaps = 0;
		this.perLapTime = 0;

		this.printToElement(this.elapsedTimeParagraph, 0);

		this.buttonsDiv.removeChild(this.buttonsObj.resumeButton);
		this.buttonsDiv.removeChild(this.buttonsObj.resetButton);
		this.buttonsDiv.appendChild(this.buttonsObj.startButton);

		removeAllChildNodes(this.lapsDiv.laps);
		removeAllChildNodes(this.lapsDiv.lapTimes);
		removeAllChildNodes(this.lapsDiv.overallTime);

		this.lapsDiv.isSet = false;
	}

	resume() {
		this.isActiveResumeBtn = true;

		this.buttonsDiv.removeChild(this.buttonsObj.resumeButton);
		this.buttonsDiv.removeChild(this.buttonsObj.resetButton);
		this.buttonsDiv.appendChild(this.buttonsObj.stopButton);
		this.buttonsDiv.appendChild(this.buttonsObj.lapButton);

		this.start();
	}

	lap() {
		this.perLapTime = this.totalElapsedTime - this.overallTime;
		this.overallTime += this.perLapTime;
		this.totalElapsedLaps++;
		console.log(`Lap number: ${this.totalElapsedLaps}`);
		console.log(`Time per lap: ${this.perLapTime}\n`);

		let pLeft, pMiddle, pRight;

		if (!this.lapsDiv.isSet) {
			pLeft = createP('lap', 'Lap');
			pMiddle = createP('lap_times', 'Lap times');
			pRight = createP('overall_time', 'Overall time');

			this.lapsDiv.laps.appendChild(pLeft);
			this.lapsDiv.lapTimes.appendChild(pMiddle);
			this.lapsDiv.overallTime.appendChild(pRight);
			this.lapsDiv.isSet = true;
		}

		pLeft = createP('lap', this.totalElapsedLaps);
		pMiddle = createP('lap_times', this.perLapTime);
		pRight = createP('overall_time', this.overallTime);

		this.lapsDiv.laps.insertBefore(pLeft, this.lapsDiv.laps.children[1]);
		this.lapsDiv.lapTimes.insertBefore(pMiddle, this.lapsDiv.lapTimes.children[1]);
		this.lapsDiv.overallTime.insertBefore(pRight, this.lapsDiv.overallTime.children[1]);
	}
}
