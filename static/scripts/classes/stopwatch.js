export default class Stopwatch {

	constructor(startButton, stopButton, elapsedTimeParagraph) {
		this.totalElapsedTime = 0;
		this.totalElapsedLaps = 0;
		this.actualPerLapTime = 0;

		this.startButton = startButton;
		this.stopButton = stopButton;
		this.elapsedTimeParagraph = elapsedTimeParagraph;
	}

	get time() {
		return this.totalElapsedTime;
	}

	printToElement(element, content) {
		element.innerHTML = content;
	}

	get randomNumber() {
		return Math.floor(Math.random() * 100);
	}

	start() {
		let startTime = new Date().getTime();
		let actualTime;
		let i = 0
		while(i < 50) {
			actualTime = new Date().getTime();
			let timeDelta = Math.abs(startTime - actualTime);
			console.log(timeDelta)
			this.printToElement(this.elapsedTimeParagraph, timeDelta);
			i++;
		}
		console.log('End of start function')
	}
}
