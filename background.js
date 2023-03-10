// ================ RESET FOR TESTING =====================
// function resetCount(){chrome.storage.local.set({'LatestMailCount': '0'});}
// resetCount();
chrome.storage.local.clear(function() {
    var error = chrome.runtime.lastError;
    if (error) {
        console.error(error);
    }
});
// ================ RESET FOR TESTING =====================

// ==================== RIGHT CLICK CONTEXT MENU ===========================
// TODO: USE BINGAI HERE

// chrome.contextMenus.create({
	// title: "AutoComplete", 
	// id: "new_id",
	// contexts:["editable"]
// });

// chrome.contextMenus.onClicked.addListener( (info, tab) => {

// });

// ==================== RIGHT CLICK CONTEXT MENU ===========================


// =============================== AUTOSYNC===============================================
// chrome.alarms.create("check-new-emails", {delayInMinutes: 0.1, periodInMinutes: 0.1});
// chrome.alarms.create("check-if-finetune-complete", {delayInMinutes: 0.1, periodInMinutes: 0.1});

// chrome.alarms.onAlarm.addListener(function(alarm) {
	
	// if (alarm.name === "check-if-finetune-complete"){
		// chrome.storage.local.get(['ID'], function(result) {

			// fetch('https://api.openai.com/v1/fine-tunes', {
				// headers: {
					// 'Authorization': 'Bearer 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'
				// }
			// }).then(response => response.json())
			  // .then(data => {
				  
				// var uu = JSON.stringify(data);
				// uu = data.data
				// var current_model = uu.pop();
				// console.log(current_model.status); 
				  
				// if (current_model.status === "pending"){
					// console.log("pending");		
				// }
				// else if (current_model.status === "succeeded"){
					
					// // TODO: Continuously saves. Can be fixed
					// chrome.storage.local.set({'ID': data.id}, function() {
						// //console.log("success, saving as the current model");
					// });
					
				// }
			// }).catch(error => console.error(error));
		// });
	// }

	// if (alarm.name === "check-new-emails") {
		
		// chrome.identity.getAuthToken({'interactive': false}, function(token, callback) {

		// //chrome.storage.local.get(['OauthSet'], function(result) {
			// if (token != null){
				// fetch("https://www.googleapis.com/gmail/v1/users/me/messages?q=from:me+-is:draft&maxResults=1", {
					// headers: {
						// "Authorization": "Bearer " + token
					// }
				// })		
				// .then(response => response.json())
				// .then(data => {
					// chrome.storage.local.get(['LatestMail'], function(result) {
						// if (data.messages[0].id === result.LatestMail){
							// console.log("same");
						// }else{
							// console.log("NEW MAIL!");
							// updateNewMailIdAndMailCount(data);					
						// }
					// });
				// });
			// }else{ console.log(token); }
		// }); 		
	// }

// });

// function updateNewMailIdAndMailCount(data){
	// //console.log("in updateNewMailIdAndMailCount" + JSON.stringify(data));
	// chrome.storage.local.get(['LatestMailCount'], function(result) {
		// var new_count = parseInt(result.LatestMailCount) + 1;
		
		// console.log(new_count);
		// //console.log(data.messages[0]);
		
		// if (new_count == 1){
			// console.log("New emails. Time to finetune");

			// const date = new Date();
			// const formattedDate = date.toLocaleString("en-us", { day: "numeric", month: "long", year: "numeric" });
			// console.log("ccc"+formattedDate);

			// chrome.tabs.sendMessage(0, {message: "change-date"});
				
			// //reset LatestMail and LatestMailCount
			// chrome.storage.local.set({'LatestMailCount': '0'});
			// chrome.storage.local.set({'LatestMail': data.messages[0].id});
			// autosync();
		// }
		// chrome.storage.local.set({'LatestMailCount': JSON.stringify(new_count)});
		// chrome.storage.local.set({'LatestMail': data.messages[0].id});
	// });
// }

// function autosync(){
	// chrome.identity.getAuthToken({'interactive': false}, function(token, callback) {
		// if (token == null) {
			// console.error("Expired token (autosync)");
		// } 
		// else {
			// fetch("https://www.googleapis.com/gmail/v1/users/me/messages?q=from:me&maxResults=200", {
				// headers: {
					// "Authorization": "Bearer " + token
				// }
			// }).then(response => response.json()).then(data => {
				// //console.log(data);
				// fetchEachMessage(data, token);
			// });	
		// }
	// });
// }

// //autosync();

// function fetchEachMessage(data, token) {
	// const promiseArray = data.messages.map(message => {
		// return fetch(`https://www.googleapis.com/gmail/v1/users/me/messages/${message.id}`, {
			// headers: {
			  // "Authorization": "Bearer " + token
		// }
		// }).then(response => response.json()).then(email => {
			// return cleanMailAndCreatePromptFile(email);
		// });
	// });

	// Promise.all(promiseArray)
	// .then(results => {
		// //console.log(results);
		// var finalArray = results.map(result => {
			// return result;
		// });
		// finalArray = finalArray.filter(elem => elem !== '');
		// finalArray = finalArray.filter(elem => elem !== ',');
		// var yay = finalArray.join("");
		
		// const filteredJsonL = yay.split("\n").filter(line => line.trim() !== "");
		
		// var result = filteredJsonL.join("\n");
		// console.log(result);

		// //createFileAndFineTune(result);
	  // })
	  // .catch(error => console.log(error));
// }

// async function cleanMailAndCreatePromptFile(message){
	
	// var prompt_file = "";
    // const fromEmail = getGoogleMessageEmailFromHeader('From', message);
    // const toEmail = getGoogleMessageEmailFromHeader('To', message);
	// //console.log(fromEmail, toEmail);
	// var part;
    // if (message.payload.parts) {
        // part = message.payload.parts.find((part) => part.mimeType === 'text/plain');
    // }
    // let encodedText;
    // if (message.payload.parts && part && part.body.data) {
        // encodedText = part.body.data;
    // } /*else if (message.payload.body.data) {
        // encodedText = message.payload.body.data;
    // }*/
    // if (encodedText) {
		// var decoded_message = atob(part.body.data.replace(/-/g, '+').replace(/_/g, '/') );
		// //console.log(decoded_message);
    // }
	
	// if (decoded_message !== undefined) {
		// var my_completion = await getMessageSentByMe(decoded_message, toEmail, fromEmail);
		// var prev_message = await getPreviousMessage(decoded_message, toEmail, fromEmail);
		// //console.log("cleanMailAndCreatePromptFile prev_message: " + prev_message);
		// if (message.payload.headers.find((header) => header.name === "Subject") !== undefined) {
			// if (message.payload.headers.find((header) => header.name === "Subject").value !== undefined){
				// var subject = message.payload.headers.find((header) => header.name === "Subject").value;
			// }
		// }
		// if (prev_message !== "empty message" && my_completion !== "empty completion" && subject !== undefined) {
			// if (subject.length !== 0){
				// var final_prompt = subject + ":" + prev_message;	
				// var temp = [{"prompt":final_prompt,"completion":my_completion}]	
				// temp.forEach(function(elem) {
					// prompt_file += JSON.stringify(elem) + "\n";
				// });
			// }
		// }
	// }
	
	
	// if (prompt_file.length !== 0){
		// //console.log(prompt_file);
		// return prompt_file;
	// }
// }

// function createFileAndFineTune(prompt_file){
	
	// //console.log("The final prompt_file: " + prompt_file);
						
	// const blob = new Blob([prompt_file], { type: 'application/json' });
	// const file = new File([ blob ], 'file.json')
			
	// const form = new FormData();
	// form.append('purpose', 'fine-tune');
	// form.append('file', file);		
		
	// fetch('https://api.openai.com/v1/files', {
		// method: 'POST',
		// headers: {
			// 'Authorization': 'Bearer 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'
		// },
		// body: form
		// })
		// .then(response => response.json())
		// .then(data => {
			// console.log(JSON.stringify(data));
			// //final_finetune(data.id);				
		// }).catch(error => console.error(error)); 
// }

// function final_finetune(file_id){
	
	// fetch('https://api.openai.com/v1/fine-tunes', {
		// headers: {
			// 'Authorization': 'Bearer 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'
		// }
	// }).then( response => response.json()).then (data => {
		
		// var uu = JSON.stringify(data);
		// uu = data.data;
		// var current_model = uu.pop();
		// console.log(current_model);
		
		// // First time finetuning
		// if (current_model.fine_tuned_model == null) {
			// fetch('https://api.openai.com/v1/fine-tunes', {
				// method: 'POST',
				// headers: {
					// 'Content-Type': 'application/json',
					// 'Authorization': 'Bearer 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'
				// },
				// body: JSON.stringify({
					// 'training_file': file_id,
					// 'model': 'davinci'
				// })
			// })
			// .then(response => response.json()).then (data => {
				
				// console.log(JSON.stringify(data));
				
				// // save ID to check if finetune finished or not
				// chrome.storage.local.set({'ID': data.id}, function() {
					// console.log('Value is set to ' + data.id);
				// });
				
			// }).catch(error => console.log(error));
			
		// }
		// // Finetuning the finetune
		// else {		
			// fetch('https://api.openai.com/v1/fine-tunes', {
				// method: 'POST',
				// headers: {
					// 'Content-Type': 'application/json',
					// 'Authorization': 'Bearer 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'
				// },
				// body: JSON.stringify({
					// 'training_file': file_id,
					// 'model': current_model.fine_tuned_model
				// })
			// })
			// .then(response => response.json()).then (data => {
				
				// console.log(JSON.stringify(data));
				// // save ID to check if finetune finished or not
				// chrome.storage.local.set({'ID': data.id}, function() {
					// console.log('Value is set to ' + data.id);
				// });
			// }).catch(error => console.log(error));
			
		// }
	// });
	
// }

// async function getMessageSentByMe(text, toEmail, fromEmail) {
	
	// //console.log(text);
	// if (toEmail && fromEmail && text.length !== 0) {
		// if ((toEmail.split("@").pop() === "gmail.com" || toEmail.split("@").pop() === "dtcforce.com") &&
		// (fromEmail.split("@").pop() === "gmail.com" || fromEmail.split("@").pop() === "dtcforce.com") ) {
			
			// text = text.replace(/^>.*$/gm, "");
			// text = text.replace(/On [A-Za-z]{3}, .*? (AM|PM) ([A-Za-z]+ [A-Za-z]+([\s]+[A-Za-z]+)?([A-Za-z])+.*)*/g, "");
			// text = text.replace(/<.*@.*> *(?:[\r\n])*wrote:/, "")
			// text = text.replace(/.*wrote:/, "");
			// text = text.trim();
			// console.log("My text:" + text);
			// return text;
		// }
	// }
	// else {
		// return "empty completion";
	// }
// }

// function getGoogleMessageEmailFromHeader(headerName, message) {
    // const header = message.payload.headers.find((header) => header.name === headerName);

    // if (!header) {
        // return null;
    // }

    // const headerValue = header.value; // John Doe <john.doe@example.com>

    // const email = headerValue.substring(
        // headerValue.lastIndexOf('<') + 1,
        // headerValue.lastIndexOf('>')
    // );

    // return email; // john.doe@example.com
// }

// async function getPreviousMessage(prev_message, toEmail, fromEmail) {
	
	// prev_message = prev_message.replace(/^(?!>).*$/gm, "");
	// //console.log(prev_message);
	
	// // OLD regex below:
	// //prev_message = prev_message.match(/^>.*$/gm);
	
	// // After removing my message:
	// //console.log(prev_message, toEmail, fromEmail); 
	
	// if (prev_message !== null && toEmail.split("@").pop() === "gmail.com") {
	
		// //console.log(prev_message);
		// prev_message = prev_message.match(/^>([^<]*>?)/m);
		// //console.log(prev_message);
		// prev_message = prev_message ? prev_message[1].trim() : "";
		// //console.log(prev_message);
		// prev_message = prev_message.replace(/On [A-Za-z]{3}, .*? (AM|PM) ([A-Za-z]+ [A-Za-z]+([\s]+[A-Za-z]+)?([A-Za-z])+.*)*/g, "");

		// //console.log(prev_message);

		// return prev_message;
	// }
	
	// else if (prev_message !== null && toEmail.split("@").pop() === "dtcforce.com") {
				
		// prev_message = prev_message.replace(/> --.*/s, "");
		// //console.log(prev_message);
		// prev_message = prev_message.trim();
		// prev_message = prev_message.replaceAll(">", "");
		// //console.log("prev_message: " + prev_message);
		// return prev_message;
	// }
	
	// else {
		// return "empty message";
	// }
// }
// =============================== AUTOSYNC===============================================