function pollFunction() {
		
	if (document.getElementsByClassName('Am aO9 Al editable LW-avf tS-tW').item(0) != null) {
		
		var reply_div = document.getElementsByClassName('btC').item(0);
		var body_div = document.getElementsByClassName('Am aO9 Al editable LW-avf tS-tW').item(0);

		if (!document.getElementById("autocompletebutton")) {
			const td_elem = document.createElement("td");
			td_elem.id = "autocompletebutton";
			var clickable_button = document.createElement("button");
			td_elem.appendChild(clickable_button);
			clickable_button.innerHTML = "Auto Complete";
			var prev_msg = document.getElementsByClassName("a3s aiL")[0].innerText;

			reply_div.appendChild(td_elem, reply_div);

			clickable_button.addEventListener("click", e => {
				if (document.getElementsByClassName("a3s aiL")[0] != null) {
					
					//console.log(prev_msg);

					if (body_div.innerText.trim() !== "") {
						console.log("not empty");
						prev_msg = prev_msg + " " + body_div.innerText;
					} else {
						console.log("empty");
						prev_msg = prev_msg.replaceAll("\n", '');
						prev_msg = "Reply to this: " + prev_msg + "- ";
					}
					
					fetch('https://api.openai.com/v1/completions', {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
							'Authorization': 'Bearer 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'
						},
											
						body: JSON.stringify({
							model: 'text-davinci-003',
							prompt: prev_msg,
							max_tokens: 250,
							temperature: 0.7
						})
					})
					.then(response => response.json())
					.then(data => {

						// console.log(JSON.stringify(data));
						// console.log(data.choices[0].text);

						body_div.innerText += data.choices[0].text;
						
					}).catch(error => console.error(error));
					
				}
			});
		}
	}
}

// Poll the webpage every 0.5 seconds
setInterval(pollFunction, 500);

function pollFunctionForBigReplyWindow() {
	// Check the condition

	if (document.getElementsByClassName('Am Al editable LW-avf tS-tW').item(0) != null) {
		var reply_div = document.getElementsByClassName('btC').item(0);
		var body_div = document.getElementsByClassName('Am Al editable LW-avf tS-tW').item(0);
		//console.log("i can run");

		if (!document.getElementById("autocompletebutton")) {
			const td_elem = document.createElement("td");
			//button.innerHTML = "AutoComplete";
			td_elem.id = "autocompletebutton";

			var clickable_button = document.createElement("button");
			td_elem.appendChild(clickable_button);
			clickable_button.innerHTML = "Auto Complete";

			var prev_msg = document.getElementsByClassName("a3s aiL")[0].innerText;

			reply_div.appendChild(td_elem, reply_div);

			clickable_button.addEventListener("click", e => {
				
				if (document.getElementsByClassName("a3s aiL")[0] != null) {	
					fetch('https://api.openai.com/v1/completions', {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
							'Authorization': 'Bearer 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'
						},
											
						body: JSON.stringify({
							model: 'text-davinci-003',
							prompt: prev_msg,
							max_tokens: 250,
							temperature: 0.7
						})
					})
					.then(response => response.json())
					.then(data => {

						// console.log(JSON.stringify(data));
						// console.log(data.choices[0].text);

						body_div.innerText += data.choices[0].text;
						
					}).catch(error => console.error(error));
					
				}
			});

		}
	}
}

// Poll the webpage every 0.5 seconds
setInterval(pollFunctionForBigReplyWindow, 500);


/*
function pollFunctionForLinkedin() {
	// Check the condition
	if (document.getElementById('custom-message') != null) {

		var body_div = document.getElementById('custom-message');

		if (!document.getElementById("autocompletebutton")) {

			var clickable_button = document.createElement("button");
			clickable_button.id = "autocompletebutton";
			clickable_button.innerHTML = "Auto Complete";

			body_div.parentNode.insertBefore(clickable_button, body_div);

			clickable_button.addEventListener("click", e => {

				var prof = JSON.stringify(extract());
				var temp = JSON.parse(prof);
				temp["message"] = "profile-info";
				prof = JSON.stringify(temp);
				//var prof = getInfo();

				chrome.runtime.sendMessage(temp);

				chrome.runtime.onMessage.addListener(
					function(request, sender, sendResponse) {
						
						body_div.value = request.message;
					});
			});
		}
	}
}
// Poll the webpage every 0.5 seconds
setInterval(pollFunctionForLinkedin, 500);
*/