// TODO:
// Google news integration with interests
// New Message
// Back Button
// Clean functions
// Error handling

window.onload = async function() {

	document.getElementById("SubmitButton").addEventListener("click", function() {

		var email = document.getElementById("email").value;
		var password = document.getElementById("password").value;
		// alert(email);
		// alert(password);

		fetch("https://ai-assistant.herokuapp.com/linkedin-login", {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({
					email: email,
					password: password
				})
			})
			.then(response => response.json())
			.then(data => {

				if (data.success === true) {

					// show the messages part
					document.getElementById("login-page").style.display = "none";
					document.getElementById("linkedin-search-page").style.display = "block";
					document.getElementById("messages-page").style.display = "block";

					chrome.storage.local.set({
						'LinkedinEmail': email
					});
					chrome.storage.local.set({
						'LinkedinPassword': password
					});
				} else {
					
					// document.getElementById("ErrorContainer").innerHTML = "Invalid login info. Please try again";

					const img = new Image();
					var screenshot = data.message; 
					console.log("screenshot", data.message);
					img.src = `data:image/png;base64,${screenshot}`;
					
					console.log(data.success);
					document.getElementById("ErrorContainer").appendChild(img);
					
					document.getElementById("ErrorContainer").appendChild(img)
					
					// var f = document.createElement("textbox");
					// var captchaSubmitButton = document.createElement("button");
					// document.getElementById("ErrorContainer").appendChild(f);
					
					// var codeInputBox = document.createElement("input");
					// codeInputBox.type = "text";
					// document.getElementById("ErrorContainer").appendChild(codeInputBox);
					// var codeSubmitButton = document.createElement("button");
					// codeSubmitButton.innerHTML = "Submit code";
					// codeSubmitButton.id = "CodeSubmitButton";
					// document.getElementById("ErrorContainer").appendChild(codeSubmitButton);
					
					// document.getElementById("CodeSubmitButton").onclick = function() {
						// fetch("https://ai-assistant.herokuapp.com/send-code", {
							// method: "POST",
							// headers: {
								// "Content-Type": "application/json"
							// },
							// body: JSON.stringify({
								// code: codeInputBox.value
							// })
						// })
						// .then(response => response.json())
						// .then(data => {
							// if (data.success === true) {
													
								// // show the messages part
								// console.log(data);
					
								// document.getElementById("login-page").style.display = "none";
								// document.getElementById("linkedin-search-page").style.display = "block";
								// document.getElementById("messages-page").style.display = "block";

								// chrome.storage.local.set({
									// 'LinkedinEmail': email
								// });
								// chrome.storage.local.set({
									// 'LinkedinPassword': password
								// });
							// }
							
						// });
					// }
					
				}
			});
	});

	var emailResult = await chrome.storage.local.get(['LinkedinEmail']);
	
	// console.log(emailResult);
	
	var email = emailResult.LinkedinEmail;
	var passwordResult = await chrome.storage.local.get(['LinkedinPassword']);
	var password = passwordResult.LinkedinPassword;
	
	// console.log(email, password);

	// Show login-page
	if (email === undefined || password === undefined) {	
		document.getElementById("login-page").style.display = "block";
		document.getElementById("linkedin-search-page").style.display = "none";
		document.getElementById("messages-page").style.display = "none";
	} 
	// Show linkedin-search and messages-page
	else {
		document.getElementById("login-page").style.display = "none";
		document.getElementById("linkedin-search-page").style.display = "block";
		document.getElementById("messages-page").style.display = "block";
	}

	/*const textareas = document.querySelectorAll("textarea");

	// Loop through each textarea/div
	textareas.forEach(textarea => {
		// Create a new button
		const button = document.createElement("button");
		button.innerHTML = "AutoComplete";

		// Add event listener for when the button is clicked
		button.addEventListener("click", e => {
			// Do something when the button is clicked (e.g. check grammar)
			chrome.runtime.sendMessage({ message: textarea.value});
			chrome.runtime.onMessage.addListener(
			  function(request, sender, sendResponse) {
				textarea.value += request.message;
			  });
		});

		// Add event listener for when the textarea/div is focused
		textarea.addEventListener("focus", e => {
			// Append the button to the textarea/div
			textarea.parentNode.insertBefore(button, textarea);

		});

		textarea.addEventListener("blur", e => {
			// Check if button is clicked or not
			if(!button.click){
			  // Remove the button from the textarea/div
			  button.remove();
			}
		});
	});*/
	
	document.getElementById("ProfileInfoButton").onclick = function() {

		fetch("https://www.linkedin.com/voyager/api/typeahead/hitsV2?keywords=USA&origin=OTHER&q=type&queryContext=List(geoVersion-%3E3,bingGeoSubTypeFilters-%3EMARKET_AREA%7CCOUNTRY_REGION%7CADMIN_DIVISION_1%7CCITY)&type=GEO", {
			"headers": {
				"accept": "application/vnd.linkedin.normalized+json+2.1",
				"accept-language": "en-US,en;q=0.9,ml;q=0.8",
				"csrf-token": "ajax:5885116779205486121",
				"x-restli-protocol-version": "2.0.0"
			},
			"body": null,
			"method": "GET",
			"mode": "cors",
			"credentials": "include"
		}).then(r => r.json()).then(console.log)

		var title = document.getElementById("title").value;
		var location = document.getElementById("Location").value;
		var currentCompany = document.getElementById("CurrentCompany").value;
		var mutualConnectionsBoolean = document.getElementById("MutualConnectionsBoolean").checked;

		fetch("https://ai-assistant.herokuapp.com/receive-link", {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({
					email: email,
					password: password,
					title: title,
					location: location,
					currentCompany: currentCompany,
					mutualConnections: mutualConnectionsBoolean
				})
			})
			.then(response => response.json())
			.then(data => {

				console.log("Successfully sent link to server", data.message);

				var jobId = data.message;
				function checkJobStatus(jobId) {
					fetch("https://ai-assistant.herokuapp.com/job-status", {
						method: "POST",
						headers: {
							"Content-Type": "application/json"
						},
						body: JSON.stringify({
							jobId: jobId
						})
					})
					
					.then(response => response.json())
					.then(data => {
						
						const status = data.status;
						
						if (status === 'finished') {
							
							const resultArray = data.result;
							
							// console.log(result);
							// return result;
							
							document.getElementById("linkedin-search-page").style.display = "none";
							document.getElementById("linkedin-page").style.display = "block";

							var myArray = resultArray;
							// var myArray = data.message;
							var pageSize = 1;
							var currentPage = 0;

							// Divide the array into pages
							var pages = [];
							for (var i = 0; i < myArray.length; i += pageSize) {
								pages.push(myArray.slice(i, i + pageSize));
							}

							var copyProfile = JSON.parse(JSON.stringify(pages[currentPage]));
							var first_name = copyProfile[0]['firstName'] + " " + copyProfile[0]['lastName'];
							var first_title = copyProfile[0]['headline'];
							var profileId = copyProfile[0]['profile_id'];
							var summary = copyProfile[0]['summary'];
							var skills = copyProfile[0]['skills'];
							var public_id = copyProfile[0]['public_id'];
							var profileUrn = copyProfile[0]['profile_urn'];

							document.getElementById("name").innerHTML = first_name;
							document.getElementById("title").innerHTML = first_title;
							
							var nextButton = document.getElementById("next-button");
							
							nextButton.addEventListener("click", function() {
								
								// Clear
								document.getElementById("my-textarea").value = "";
								document.getElementById("CheckboxContainer").innerHTML = "";
								document.getElementById("InterestsContainer").innerHTML = "";
								document.getElementById("PeopleInterestsContainer").innerHTML = "";
								document.getElementById("CompanyInterestsContainer").innerHTML = "";					
					
								// Increment the current page index
								currentPage = (currentPage + 1) % pages.length;
								var copyProfile = JSON.parse(JSON.stringify(pages[currentPage]));
								var name = copyProfile[0]['firstName'] + " " + copyProfile[0]['lastName'];
								var title = copyProfile[0]['headline'];
								var profileId = copyProfile[0]['profile_id'];
								var summary = copyProfile[0]['summary'];
								var skills = copyProfile[0]['skills'];
								var publicId = copyProfile[0]['public_id'];
								var profileUrn = copyProfile[0]['profile_urn'];

								document.getElementById("name").innerHTML = name;
								document.getElementById("title").innerHTML = title;
								
								document.getElementById("PeopleInterestsButton").onclick = function() {

									fetch("https://ai-assistant.herokuapp.com/get-people-interests", {
										method: "POST",
										headers: {
											"Content-Type": "application/json"
										},
										body: JSON.stringify({
											email: email,
											password: password,
											profileUrn: profileUrn
										})
									})
									.then(response => response.json())
									.then(data => {
										
										var jobId = data.message;
										
										console.log("job of people interests", jobId);
										
										function checkJobStatus(jobId) {
											fetch("https://ai-assistant.herokuapp.com/job-status", {
												method: "POST",
												headers: {
													"Content-Type": "application/json"
												},
												body: JSON.stringify({
													jobId: jobId
												})
											})
											
											.then(response => response.json())
											.then(data => {
												
												const status = data.status;
												console.log(status);
												
												if (status === 'finished') {
												
													console.log("Successfully gotten people interests", data.result);
													
													const words = data.result;

													// var words = data.message;
													
													var container = document.getElementById('PeopleInterestsContainer');

													for (var i = 0; i < words.length; i++) {

														var checkbox = document.createElement('input');
														checkbox.type = 'checkbox';
														checkbox.value = words[i][0];
														checkbox.id = words[i][1];
														var label = document.createElement('label');
														label.textContent = words[i][0];
														label.appendChild(checkbox);
														container.appendChild(label);
													}
													
													
												} else {
													// The job is not finished yet, check again in 1 second
													setTimeout(() => checkJobStatus(jobId), 1000);
												}
											});
												
										}
										checkJobStatus(data.message);
											
									});
								}
								
								document.getElementById("CompanyInterestsButton").onclick = function() {

									fetch("https://ai-assistant.herokuapp.com/get-company-interests", {
										method: "POST",
										headers: {
											"Content-Type": "application/json"
										},
										body: JSON.stringify({
											email: email,
											password: password,
											profileUrn: profileUrn
										})
									})
									.then(response => response.json())
									.then(data => {
										
										var jobId = data.message;
										
										console.log("job of company interests", jobId);
										
										function checkJobStatus(jobId) {
											fetch("https://ai-assistant.herokuapp.com/job-status", {
												method: "POST",
												headers: {
													"Content-Type": "application/json"
												},
												body: JSON.stringify({
													jobId: jobId
												})
											})
											
											.then(response => response.json())
											.then(data => {
												
												const status = data.status;
												console.log(status);
												
												if (status === 'finished') {
												
													console.log("Successfully gotten company interests", data.result);
													
													const words = data.result;
																
													var container = document.getElementById('CompanyInterestsContainer');

													for (var i = 0; i < words.length; i++) {

														var checkbox = document.createElement('input');
														checkbox.type = 'checkbox';
														checkbox.value = words[i][0];
														checkbox.id = words[i][1];
														var label = document.createElement('label');
														label.textContent = words[i][0];
														label.appendChild(checkbox);
														container.appendChild(label);
													}
													
													
												} else {
													// The job is not finished yet, check again in 1 second
													setTimeout(() => checkJobStatus(jobId), 1000);
												}
											});
												
										}
										checkJobStatus(data.message);
											
									});
								
								}
								document.getElementById("GenerateConnectNoteButton").onclick = function() {
									var checkboxes = document.querySelectorAll('input[type=checkbox]');
									var topicList = [];
									for (var i = 0; i < checkboxes.length; i++) {
										if (checkboxes[i].checked) {
											var topic = checkboxes[i].value;
											topicList.push(topic);
										}
									}
									var topicListString = topicList.toString();

									var prompt_string = "This is the profile of a person: " + "\n" + name 
									+ " This is their summary: " + summary +
									" These are their interests: " + topicListString 
									+ " Use the internet to get something useful about the interests and use it in the request. "
									+ " Write a request to connect with them. Make it casual but eyecatching. The goal is to ask about their current Salesforce implementation. The length should be no more than 70 words.";
									
									// console.log(prompt_string);			
													
									fetch("https://ai-assistant.herokuapp.com/use-bingai", {
										method: "POST",
										headers: {
											"Content-Type": "application/json"
										},
										body: JSON.stringify({
											prompt: prompt_string
										})
									})
									.then(response => response.json())
									.then(data => {
										
										console.log(data.message);
										
										document.getElementById("my-textarea").value = data.message;
										

									}).catch(error => console.error(error));
					
								}

								document.getElementById("send-button").onclick = function() {

									// fetch to server.js, with profileId and text
									fetch("https://ai-assistant.herokuapp.com/send-connect", {
											method: "POST",
											headers: {
												"Content-Type": "application/json"
											},
											body: JSON.stringify({
												email: email,
												password: password,
												profileId: profileId,
												text: document.getElementById("my-textarea").value
											})
										})
										.then(response => response.json())
										.then(data => {
											console.log("Successfully sent connect to server", data.message);
										});
								}
								
								
							});

							// document.getElementById("InterestsButton").onclick = function() {

									// fetch("https://ai-assistant.herokuapp.com/get-interests", {
											// method: "POST",
											// headers: {
												// "Content-Type": "application/json"
											// },
											// body: JSON.stringify({
												// email: email,
												// password: password,
												// publicId: publicId
											// })
										// })
										// .then(response => response.json())
										// .then(data => {
											// console.log("Successfully gotten interests", data.message);

											// var words = data.message;
											// var container = document.getElementById('CheckboxContainer');

											// for (var i = 0; i < words.length; i++) {

												// var checkbox = document.createElement('input');
												// checkbox.type = 'checkbox';
												// checkbox.value = words[i];
												// var label = document.createElement('label');
												// label.textContent = words[i];
												// label.appendChild(checkbox);
												// container.appendChild(label);
											// }
										// });
								// }
								
								document.getElementById("PeopleInterestsButton").onclick = function() {

									fetch("https://ai-assistant.herokuapp.com/get-people-interests", {
										method: "POST",
										headers: {
											"Content-Type": "application/json"
										},
										body: JSON.stringify({
											email: email,
											password: password,
											profileUrn: profileUrn
										})
									})
									.then(response => response.json())
									.then(data => {
										
										var jobId = data.message;
										
										console.log("job of people interests", jobId);
										
										function checkJobStatus(jobId) {
											fetch("https://ai-assistant.herokuapp.com/job-status", {
												method: "POST",
												headers: {
													"Content-Type": "application/json"
												},
												body: JSON.stringify({
													jobId: jobId
												})
											})
											
											.then(response => response.json())
											.then(data => {
												
												const status = data.status;
												console.log(status);
												
												if (status === 'finished') {
												
													console.log("Successfully gotten people interests", data.result);
													
													const words = data.result;

													// var words = data.message;
													
													var container = document.getElementById('PeopleInterestsContainer');

													for (var i = 0; i < words.length; i++) {

														var checkbox = document.createElement('input');
														checkbox.type = 'checkbox';
														checkbox.value = words[i][0];
														checkbox.id = words[i][1];
														var label = document.createElement('label');
														label.textContent = words[i][0];
														label.appendChild(checkbox);
														container.appendChild(label);
													}
													
													
												} else {
													// The job is not finished yet, check again in 1 second
													setTimeout(() => checkJobStatus(jobId), 1000);
												}
											});
												
										}
										checkJobStatus(data.message);
											
									});
								}
								
								document.getElementById("CompanyInterestsButton").onclick = function() {

									fetch("https://ai-assistant.herokuapp.com/get-company-interests", {
										method: "POST",
										headers: {
											"Content-Type": "application/json"
										},
										body: JSON.stringify({
											email: email,
											password: password,
											profileUrn: profileUrn
										})
									})
									.then(response => response.json())
									.then(data => {
										
										var jobId = data.message;
										
										console.log("job of company interests", jobId);
										
										function checkJobStatus(jobId) {
											fetch("https://ai-assistant.herokuapp.com/job-status", {
												method: "POST",
												headers: {
													"Content-Type": "application/json"
												},
												body: JSON.stringify({
													jobId: jobId
												})
											})
											
											.then(response => response.json())
											.then(data => {
												
												const status = data.status;
												console.log(status);
												
												if (status === 'finished') {
												
													console.log("Successfully gotten company interests", data.result);
													
													const words = data.result;
																
													var container = document.getElementById('CompanyInterestsContainer');

													for (var i = 0; i < words.length; i++) {

														var checkbox = document.createElement('input');
														checkbox.type = 'checkbox';
														checkbox.value = words[i][0];
														checkbox.id = words[i][1];
														var label = document.createElement('label');
														label.textContent = words[i][0];
														label.appendChild(checkbox);
														container.appendChild(label);
													}
													
													
												} else {
													// The job is not finished yet, check again in 1 second
													setTimeout(() => checkJobStatus(jobId), 1000);
												}
											});
												
										}
										checkJobStatus(data.message);
											
									});
								
								}

								document.getElementById("GenerateConnectNoteButton").onclick = function() {
									var checkboxes = document.querySelectorAll('input[type=checkbox]');
									var topicList = [];
									for (var i = 0; i < checkboxes.length; i++) {
										if (checkboxes[i].checked) {
											var topic = checkboxes[i].value;
											topicList.push(topic);
										}
									}
									var topicListString = topicList.toString();

									var prompt_string = "This is the profile of a person: " + "\n" + first_name 
									+ " This is their summary: " + summary +
									" These are their interests: " + topicListString 
									+ " Use the internet to get something useful about the interests and use it in the request. "
									+ " Write a request to connect with them. Make it casual but eyecatching. The goal is to ask about their current Salesforce implementation. The length should be no more than 70 words.";
									
									// console.log(prompt_string);			
													
									fetch("https://ai-assistant.herokuapp.com/use-bingai", {
										method: "POST",
										headers: {
											"Content-Type": "application/json"
										},
										body: JSON.stringify({
											prompt: prompt_string
										})
									})
									.then(response => response.json())
									.then(data => {
										
										console.log(data.message);
										
										document.getElementById("my-textarea").value = data.message;
										

									}).catch(error => console.error(error));
					
								}

								document.getElementById("send-button").onclick = function() {

									// fetch to server.js, with profileId and text
									fetch("https://ai-assistant.herokuapp.com/send-connect", {
											method: "POST",
											headers: {
												"Content-Type": "application/json"
											},
											body: JSON.stringify({
												email: email,
												password: password,
												profileId: profileId,
												text: document.getElementById("my-textarea").value
											})
										})
										.then(response => response.json())
										.then(data => {
											console.log("Successfully sent connect to server", data.message);
										});
								}
															
						} else {
							// The job is not finished yet, check again in 1 second
							setTimeout(() => checkJobStatus(jobId), 1000);
						}
					});
				}
				// Keep polling until we get a proper answer
				checkJobStatus(data.message);	
						
			});							
	}

	document.getElementById("MessagesButton").onclick = function() {

		document.getElementById("linkedin-search-page").style.display = "none";

		// console.log(email);

		fetch("https://ai-assistant.herokuapp.com/get-convo-threads", {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({
					email: email,
					password: password
				})
			})
			.then(response => response.json())
			.then(data => {
				console.log("Successfully gotten conversation threads", data.message);

				var words = data.message;
				var container = document.getElementById('ThreadsContainer');

				for (var i = 0; i < words.length; i++) {

					var button = document.createElement('input');
					button.type = 'button';
					button.value = words[i][0];
					button.id = words[i][1];
					button.className = "OpenConvoButton";
					var label = document.createElement('label');
					label.textContent = words[i][0];
					label.appendChild(button);
					container.appendChild(label);
				}
				const convoButtons = document.querySelectorAll('.OpenConvoButton');
				convoButtons.forEach(function(button) {
					button.addEventListener('click', function() {

						// Clear the buttons, create a header of button.value
						container.style.display = "none";
						var msg_container = document.getElementById("MessagesContainer");
						var new_h1 = document.createElement("h1")
						new_h1.innerHTML = button.value;

						msg_container.appendChild(new_h1);

						// Display the messages, create a textarea with "Get Interests" and "Generate Message" button
						fetch("https://ai-assistant.herokuapp.com/get-convo-messages", {

								method: "POST",
								headers: {
									"Content-Type": "application/json"
								},
								body: JSON.stringify({
									email: email,
									password: password,
									profileUrn: button.id
								})
							})
							.then(response => response.json())
							.then(data => {
								
								console.log("Successfully gotten messages", data.message);

								var new_p = document.createElement("p");
								new_p.textContent = data.message;
								new_p.style.color = "white";

								var new_textarea = document.createElement("textarea");
								new_textarea.id = "messageTextbox";
								var generate_interests_button = document.createElement("button");
								generate_interests_button.textContent = "Get Interests";
								var generate_message_button = document.createElement("button");
								generate_message_button.textContent = "Generate Message";

								var send_message_button = document.createElement("button");
								send_message_button.textContent = "Send Message";

								msg_container.appendChild(new_p);
								msg_container.appendChild(new_textarea);
								msg_container.appendChild(generate_interests_button);
								msg_container.appendChild(generate_message_button);
								msg_container.appendChild(send_message_button);	

								generate_interests_button.onclick = function() {

									fetch("https://ai-assistant.herokuapp.com/get-interests-from-thread", {
											method: "POST",
											headers: {
												"Content-Type": "application/json"
											},
											body: JSON.stringify({
												email: email,
												password: password,
												publicId: button.id
											})
										})
										.then(response => response.json())
										.then(data => {
											console.log("Successfully gotten interests", data.message);

											var words = data.message;
											var container = document.getElementById('InterestsContainer');

											for (var i = 0; i < words.length; i++) {

												var checkbox = document.createElement('input');
												checkbox.type = 'checkbox';
												checkbox.value = words[i];
												var label = document.createElement('label');
												label.textContent = words[i];
												label.appendChild(checkbox);
												container.appendChild(label);
											}
										});
								}

								// If generate_message_button is clicked
								generate_message_button.onclick = function() {

									var checkboxes = document.querySelectorAll('input[type=checkbox]');
									var topicList = [];
									for (var i = 0; i < checkboxes.length; i++) {
										if (checkboxes[i].checked) {
											var topic = checkboxes[i].value;
											topicList.push(topic);
										}
									}
									var topicListString = topicList.toString();
									
									var prompt_string = "Reply to this: " + data.message;
										
									fetch('https://api.openai.com/v1/completions', {
											method: 'POST',
											headers: {
												'Content-Type': 'application/json',
												'Authorization': 'Bearer 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'
											},

											body: JSON.stringify({
												model: 'text-davinci-003',
												prompt: prompt_string,
												max_tokens: 55,
												temperature: 0.7
											})
									})
									.then(response => response.json())
									.then(data => {
										//console.log(JSON.stringify(data));
										console.log(data.choices[0].text);
										new_textarea.value = data.choices[0].text;

									}).catch(error => console.error(error));

									// document.getElementById("my-textarea").value = prompt_string;
								}

								send_message_button.onclick = function() {

									fetch("https://ai-assistant.herokuapp.com/send-message", {
											method: "POST",
											headers: {
												"Content-Type": "application/json"
											},
											body: JSON.stringify({
												email: email,
												password: password,
												profileId: button.id,
												text: new_textarea.value
											})
										})
										.then(response => response.json())
										.then(data => {
											console.log("Successfully sent connect to server", data.message);
										});
								}
							});
					});
				});
			});
	}
};

// chrome.runtime.onMessage.addListener(async function(request, sender, sendResponse) {

// });