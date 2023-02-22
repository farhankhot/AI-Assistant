// =============== AUTH ==========================
// chrome.identity.onSignInChanged.addListener(function (account_id, signedIn) {
    // if (signedIn) {
		
		// // chrome.action.setPopup({popup: "popup.html"});
		// // console.log("authed");
		
		// // Send to script.js the fact that the user is authed
		
		
    // } else {
        // // chrome.action.setPopup({popup: "logged_in.html"});
		
		// // Send to script.js the fact that the user is NOT authed
		
    // }
// });
// =============== AUTH ==========================

// ================ RESET FOR TESTING =====================
// function resetCount(){chrome.storage.local.set({'LatestMailCount': '0'});}
// resetCount();
// chrome.storage.local.clear(function() {
    // var error = chrome.runtime.lastError;
    // if (error) {
        // console.error(error);
    // }
    // // do something more
// });
// ================ RESET FOR TESTING =====================

// ===================== ON POPUP CLICK ==========================
// chrome.action.onClicked.addListener((tab) => {
	// console.log("icon clicked");
	
	// chrome.runtime.sendMessage({message: "check-linkedin-auth"});
	
	// chrome.storage.local.get(['LinkedInEmail'], function(result) {
		// // console.log(result.LinkedInEmail);
		
		// if (result.LinkedInEmail === undefined) {

			// console.log("not logged in");
            // chrome.action.setPopup({popup: "logged_in.html"});

        // } else {

            // // The user has already authenticated, show the HTML page
			// console.log("logged in");
			// //chrome.storage.local.set({'LatestMail': data.messages[0].id}
			    // chrome.tabs.query({
					// active: true,
					// currentWindow: true
				// }, function (tabs) {
					// chrome.tabs.sendMessage(tabs[0].id, {
						// todo: "toggle"
					// });
				// })
// //			chrome.action.setPopup({popup: "popup.html"});			
		// }
	// });

	
	// chrome.identity.getAuthToken({'interactive': false}, function(token, callback) {
        // if (chrome.runtime.lastError) {
            // // The user has not authenticated yet, show the OAuth button
			// console.log("not logged in");
            // chrome.action.setPopup({popup: "logged_in.html"});

        // } else {
            // // The user has already authenticated, show the HTML page
			// console.log("logged in");
			// //chrome.storage.local.set({'LatestMail': data.messages[0].id}
			    // chrome.tabs.query({
					// active: true,
					// currentWindow: true
				// }, function (tabs) {
					// chrome.tabs.sendMessage(tabs[0].id, {
						// todo: "toggle"
					// });
				// })
// //			chrome.action.setPopup({popup: "popup.html"});			
		// }
    // });
	
// });
// ===================== ON POPUP CLICK ==========================

/*chrome.contextMenus.create({
	title: "AutoComplete", 
	id: "new_id",
	contexts:["editable"]
});*/

/*chrome.contextMenus.onClicked.addListener( (info, tab) => {

  	//console.log(info);
	
	var for_completion = info.selectionText;
	
	chrome.storage.local.get(['ID'], function(result) {
		var u = result.ID;
		var fin_fetch = 'https://api.openai.com/v1/fine-tunes/' + u;
		console.log(fin_fetch);

		fetch(fin_fetch, {
			headers: {
				'Authorization': 'Bearer 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'
			}
		}).then(response => response.json())
		  .then(data => {
			if (data.status === "pending"){
				console.log("pending, using model: " + data.model);
				 // Use the fetch API to make a POST request to the OpenAI API
				fetch('https://api.openai.com/v1/completions', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': 'Bearer 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'
					},
					body: JSON.stringify({
						model: u,
						prompt: for_completion,
						max_tokens: 200,
						temperature: 0.7
					})
				})
				.then(response => response.json())
				.then(data => {
					console.log("one");			
					
					chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
						chrome.tabs.sendMessage(tab.id, {message: data.choices[0].text});
					});
					
				})
				.catch(error => console.error(error));
				
			}
			else if (data.status === "succeeded"){
				
				 // Use the fetch API to make a POST request to the OpenAI API
				fetch('https://api.openai.com/v1/completions', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': 'Bearer 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'
					},
					body: JSON.stringify({
						model: 'text-davinci-003',
						prompt: for_completion,
						max_tokens: 200,
						temperature: 0.7
					})
				})
				.then(response => response.json())
				.then(data => {
					console.log("two");
					console.log(data.choices[0].text);
					
					chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
						chrome.tabs.sendMessage(tab.id, {message: data.choices[0].text});
					});
					
				})
				.catch(error => console.error(error));			
			}
		}).catch(error => console.error(error));
	});
	
});*/

// function GetProfileInfoFromList() {
	// const ulElement = document.getElementsByClassName("reusable-search__entity-result-list list-style-none")[1];
	// var linkList = [];
	// const listItems = ulElement.querySelectorAll('li');
	
	// var count = 0;
	// listItems.forEach(li => {
		// var name = li.querySelector('a > span > span').textContent.trim();
		// var occupation = document.getElementsByClassName("entity-result__primary-subtitle t-14 t-black t-normal")[count].textContent;
		// //console.log(name + occupation);
		// //link = link.href.split('?')[0];
	
		// if (linkList.length < 1) {
			// linkList.push(name + occupation);
		// }
		
		// count += 1;
		
	// });
	// return linkList;
// }


chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
	
	// if (request.message === 'get_auth_token') {
		
		// // console.log("cc");
        
		// chrome.identity.getAuthToken({ interactive: true }, function (token, callback) {
			
			// console.log(token);
			
			// if (chrome.runtime.lastError) {
				// console.log("runtime error");
			// }else {
				// console.log("token from get_auth_token: " + token);
				
				// // Getting latest mail and setting latestmail count to 0 (FOR AUTOSYNC FEATURE)
				// // fetch("https://www.googleapis.com/gmail/v1/users/me/messages?q=from:me&maxResults=1", {
						// // headers: {
						// // "Authorization": "Bearer " + token
						// // }
				// // })
				// // .then(response => response.json())
				// // .then(data => {
					// // chrome.storage.local.set({'LatestMail': data.messages[0].id}, function() {
						// // console.log('Value is set to ' + data.messages[0].id);
					// // });
					// // chrome.storage.local.set({'LatestMailCount': "0"}, function() {
						// // console.log('Value is set to ' + '0');
					// // });
				// // });	
			// }
		// });
    // }
	
	// /*else if (request.message === 'linkedin_get_auth_token'){
		// var client_secret = "FzVZDL3m577jtI2u";
		// var client_id = "784sbgo24n1suv";
		// chrome.identity.launchWebAuthFlow({
			// interactive: true,
			// url: "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=784sbgo24n1suv&redirect_uri=https://ipdnagmfkadagdfhckmnikoklibihimi.chromiumapp.org&state=foobar&scope=r_liteprofile%20r_emailaddress"
			
		// }, function(responseUrl) {
			// const queryString = responseUrl.split("?")[1];
			// const code = queryString.split("code=")[1].split("&")[0];
			// console.log(code);
			// var final_url = "https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code="+code+
			// "&client_id="+client_id+"&client_secret="+client_secret+
			// "&redirect_uri="+"https://ipdnagmfkadagdfhckmnikoklibihimi.chromiumapp.org";
			// fetch(final_url, {
				// headers: {
				// "Content-Type": "application/x-www-form-urlencoded"
				// },
				// method: "POST"
			// }).then(response => response.json())
			// .then(data => {
				// chrome.storage.local.set({'linkedinAccessToken': data.access_token});
				// console.log(data);
			// }).catch(error => console.error(error));
		// });		
	// }*/
	
	// /*else if(request.message === "getPeople") {

		// chrome.storage.local.get(['linkedinAccessToken'], function(result) {
			// console.log(result.linkedinAccessToken)
			// const accessToken = result.linkedinAccessToken;
			
			// const headers = new Headers({
			  // "Authorization": `Bearer ${accessToken}`,
			  // "X-RestLi-Protocol-Version":"2.0.0"
			// });

			// fetch("https://api.linkedin.com/v2/people/dave-mckay-4189071", {
				// headers: headers,
				// method: "GET"
			// }).then(response => response.json())
			// .then(data => {
				// console.log(data);
			// })
		// });
	// }*/
	
	// else if (request.message === 'profile-info'){
		// var name = "Farhan";
		// var prompt_string = "This is the profile of a person: " + "\n" + "Fullname: " + request.fullName + 
		// "Title: " + request.title + "\n"+"Description: "+ request.description + " Write a polite request to connect with them. My name is " + 
		// name + " and my occupation is a Software developer"
		// console.log(prompt_string);
	
		// fetch('https://api.openai.com/v1/completions', {
			// method: 'POST',
			// headers: {
				// 'Content-Type': 'application/json',
				// 'Authorization': 'Bearer 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'
			// },
						
			// body: JSON.stringify({
				// model: 'text-davinci-003',
				// prompt: prompt_string,
				// max_tokens: 100,
				// temperature: 0.7
			// })
		// })
		// .then(response => response.json())
		// .then(data => {
			// //console.log(JSON.stringify(data));
			// console.log(data.choices[0].text);
			// chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
				// chrome.tabs.sendMessage(tabs[0].id, {message: data.choices[0].text});
			// });
			
		// }).catch(error => console.error(error));
		
	// }
	
	// else if(request.message === "GetProfileInfoFromList"){
		// console.log("iran");
		// var a = request.title;
		// var b = request.location;
		// var c = request.currentCompany;
		// fetch("http://localhost:3000/receive-link", {
			// method: "POST",
			// headers: {
				// "Content-Type": "application/json"
			// },
			// body: JSON.stringify({ a, b, c })
		// })
		// .then(response => response.json())
		// .then(data => {
			// console.log("Successfully sent link to server", data.message);
			// chrome.runtime.sendMessage({message: "show-list", list: data.message});
		// });
	// }
	
	// Textbox everywhere below
	if (request.message === "textbox-everywhere") {
		chrome.identity.getAuthToken({ interactive: true }, function (token, callback) {
			
			//console.log(token);
			
			if (chrome.runtime.lastError) {
				
				console.log("Please log in");

			}else {
				
				console.log("signed in");
				
				var prompt = request.prompt;
				fetch('https://api.openai.com/v1/completions', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': 'Bearer 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'
					},
										
					body: JSON.stringify({
						model: 'text-davinci-003',
						prompt: prompt,
						max_tokens: 250,
						temperature: 0.7
					})
				})
				.then(response => response.json())
				.then(data => {
					console.log(JSON.stringify(data));
					console.log("two");
					console.log(data.choices[0].text);
					chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
						chrome.tabs.sendMessage(tabs[0].id, {message: data.choices[0].text});
					});
					
				}).catch(error => console.error(error));
				
				// FOR AUTOSYNC FEATURE
				// chrome.storage.local.get(['ID'], function(result) {
					// var u = result.ID;
					// console.log("ID: " + u);
					// var fin_fetch = 'https://api.openai.com/v1/fine-tunes/' + u;
					// console.log(fin_fetch);
					// var for_completion = request.message;
					// //for_completion = for_completion.replaceAll("\n", '');
					// //for_completion = "Reply to this: " + for_completion + "- ";
					// console.log(for_completion);

					// fetch(fin_fetch, {
						// headers: {
							// 'Authorization': 'Bearer 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'
						// }
					// }).then(response => response.json())
					  // .then(data => {

						// if (data.status === "pending"){
							// console.log("pending, using model: " + data.model);
							 // // Use the fetch API to make a POST request to the OpenAI API
							// fetch('https://api.openai.com/v1/completions', {
								// method: 'POST',
								// headers: {
									// 'Content-Type': 'application/json',
									// 'Authorization': 'Bearer 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'
								// },
								// body: JSON.stringify({
									// model: u,
									// prompt: for_completion,
									// max_tokens: 200,
									// temperature: 0.7
								// })
							// })
							// .then(response => response.json())
							// .then(data => {
								// console.log("one");			
								// chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
									// chrome.tabs.sendMessage(tabs[0].id, {message: data.choices[0].text});
								// });
								
							// }).catch(error => console.error(error));
						// }
						// else if (data.status === "succeeded"){
							
							 // // Use the fetch API to make a POST request to the OpenAI API
							// fetch('https://api.openai.com/v1/completions', {
								// method: 'POST',
								// headers: {
									// 'Content-Type': 'application/json',
									// 'Authorization': 'Bearer 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'
								// },
								
								// //body: JSON.stringify({
									// //model: data.fine_tuned_model,
									// //prompt: for_completion,
									// //max_tokens: 150,
									// //temperature: 0.7
								// //})
								
								// body: JSON.stringify({
									// model: 'text-davinci-003',
									// prompt: for_completion,
									// max_tokens: 250,
									// temperature: 0.7
								// })
							// })
							// .then(response => response.json())
							// .then(data => {
								// console.log(JSON.stringify(data));
								// console.log("two");
								// console.log(data.choices[0].text);
								// chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
									// chrome.tabs.sendMessage(tabs[0].id, {message: data.choices[0].text});
								// });
								
							// }).catch(error => console.error(error));			
						// }
					// }).catch(error => console.error(error));				
				// });
			}
		});	
	}
});

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