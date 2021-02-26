function updateSlider(sliderValue, numberElement){ 
			document.getElementById(numberElement).innerHTML = sliderValue;
			return;
		}
/*
// Create a request variable and assign a new XMLHttpRequest object to it.
function getLight(){
	var request = new XMLHttpRequest()

	// Open a new connection, using the GET request on the URL endpoint
	request.open('GET', 'https://diracweiler.github.io/dataFile.json', true)

	request.onload = function () {
  		// Begin accessing JSON data here
		var data = JSON.parse(this.responseText)

		if (request.status >= 200 && request.status < 400) {
			const cLight = document.getElementById('currentLight')
			cLight.textContent = data[1].value
			const dLight = document.getElementById('desiredLight')
			dLight.value = data[3].value

		} else {
  			console.log('error')
		}
	}
	// Send request
	request.send()
}
getLight();

function getTemp(){
	var request = new XMLHttpRequest()

	// Open a new connection, using the GET request on the URL endpoint
	request.open('GET', 'http://127.0.0.1:105/dorn/all', true)

	request.onload = function () {
  		// Begin accessing JSON data here
		var data = JSON.parse(this.responseText)

		if (request.status >= 200 && request.status < 400) {
			const cLight = document.getElementById('currentTemp')
			cLight.textContent = data[0].value
			const dLight = document.getElementById('desiredTemp')
			dLight.value = data[2].value

		} else {
  			console.log('error')
		}
	}
	request.send()
}
getTemp();

function postLight(dLight){
	var data = new FormData();
	data.append()

	var request = new XMLHttpRequest()
	request.open('PUT', 'https://diracweiler.github.io/dataFile.json', true)
}

function lightForm(){

	const isValidElement = (element) => {
  		return element.name && element.value;
	}; 

	const isValidValue = (element) => {
  		return !['checkbox', 'radio'].includes(element.type) || element.checked;
	};	

	const formToJSON = (elements) =>
  	  [].reduce.call(
    	elements,
    	(data, element) => {
       		if (isValidElement(element) && isValidValue(element)) {
        	data[element.name] = element.value;
      		}
      		return data;
    	},
    	{},
  	  );
	
	const handleFormSubmit = (event) => {
		event.preventDefault();
		// Call our function to get the form data.
  		const data = formToJSON(form.elements);
  		//This is where we use the JSON data 

	}

	const form = document.getElementById('desiredLightForm')[0];
	form.addEventListener('submit', handleFormSubmit);


}

*/