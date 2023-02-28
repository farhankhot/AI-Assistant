from linkedin_api import Linkedin
import json
from flask import Flask, request, jsonify
# from bertopic import BERTopic
import emoji
import re
import asyncio
from EdgeGPT import Chatbot
from rq import Queue
from worker import conn
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import speech_recognition as sr
import sys
import requests
from bs4 import BeautifulSoup

q = Queue(connection=conn)

app = Flask(__name__)

SEED_URL = 'https://www.linkedin.com/login'

session = requests.Session() 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-dev-shm-usage')

prefs = {"download.default_directory": r"~/",
        "directory_upgrade": True}

chrome_options.add_experimental_option("prefs", prefs)

chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)

async def UseBingAI(prompt):
    
    # Get actual location of cookie.json here
    bot = Chatbot(cookiePath='./cookie.json')

    ans_json = await bot.ask(prompt=prompt)    
    ans = ans_json['item']['messages'][1]['text']
    
    await bot.close()
    return ans

def get_values_for_key(key, dictionary):
    values = []
    for k, v in dictionary.items():
        if k == key:
            values.append(v)
        elif isinstance(v, dict):
            values.extend(get_values_for_key(key, v))
    return values    

# def GenerateCorpus(api, profile):
    
    # yay = api.get_profile_posts(profile, post_count = 100)
    
    # post_corpus = []
    # for post in yay:
        # person_corpus = get_values_for_key("text", post)
        # # print("ii", person_corpus)
        # person_corpus = [item for item in person_corpus if isinstance(item, dict)]
        # # print("jj",person_corpus)

        # try:
            # if len(person_corpus) == 1:
                # person_corpus = get_values_for_key("text", person_corpus[0])
            # else:
                # person_corpus = get_values_for_key("text", person_corpus[1])
            
            # person_corpus = emoji.demojize(person_corpus)
            # # print("dd", person_corpus)
            # post_corpus.append(person_corpus)
        # except:
            # pass
    
    # print("post_corpus", post_corpus)
    # return post_corpus
        
# def ModelAndReturnTopicList(api, profile_id):
    
    # post_corpus = GenerateCorpus(api, profile_id)
    
    # topic_model = BERTopic(min_topic_size=10, verbose=True)
    # topics, _ = topic_model.fit_transform(post_corpus)
    # freq = topic_model.get_topic_info()
    # print(freq)
    # print(freq.head(10))
    # print(topic_model.get_topic(1))
    
    # # For now, let us send n if there are n or -1 if there are none
    # # Need to see how can we send all? Maybe the best ones from a group
    # final_topics = []
    # if len(topic_model.get_topics()) == 1:
        # for tup in topic_model.get_topic(-1):
            # final_topics.append(tup[0])
    # else:
        # for topic in topic_model.get_topics():
            # if topic != -1:
                # for tup in topic_model.get_topic(topic):
                    # final_topics.append(tup[0])
    # print(final_topics)
    
    # return final_topics

def GetProfile(api, search_params, location, mutual_connections_boolean):
    print("location", location)
    
    list_of_people = api.search_people(keyword_title = search_params['title'],
    regions = [location if location != '' else ''],
    keyword_company = search_params['currentCompany'],
    network_depth = "S" if mutual_connections_boolean == True else "O")
    
    # print(list_of_people)
    
    full_profile_list = []
    for person in list_of_people[0:3]:
        prof = api.get_profile(person['public_id'])
        
        # print(prof)
        
        prof_skills = api.get_profile_skills(person['public_id'])
        prof['skills'] = prof_skills
        prof['public_id'] = person['public_id']
        prof['profile_urn'] = person['urn_id']
        
        # Get mutual connections
        
        full_profile_list.append(prof)
        
    # print(full_profile_list)
    
    return full_profile_list
    
def SendConnect(api, profile_id, text):
    error_boolean = api.add_connection(profile_id, text)
    print(error_boolean)

def get_geo_urn(api, location):
    url_params = {
        "accept": "application/vnd.linkedin.normalized+json+2.1",
        "accept-language": "en-US,en;q=0.9,ml;q=0.8",
        "csrf-token": "ajax:5885116779205486121",
        "x-restli-protocol-version": "2.0.0"
    }
    res = api._fetch(f"/typeahead/hitsV2?keywords={location}&origin=OTHER&q=type&queryContext=List(geoVersion-%3E3,bingGeoSubTypeFilters-%3EMARKET_AREA%7CCOUNTRY_REGION%7CADMIN_DIVISION_1%7CCITY)&type=GEO")
    # , params = url_params)

    # res = api._fetch(f"/me")
    # print(res.json()['elements'][0]['targetUrn'])
    geo_urn = res.json()['elements'][0]['targetUrn'] # Output: urn:li:fs_geo:103644278
    geo_urn = re.search("\d+", geo_urn).group()
    return geo_urn

def get_conversation_threads(email, password):
    print("nn", email)
    
    api = Linkedin(email, password)
    print(api)
    
    convo_list=[]
    yay = api.get_conversations()
    print(yay)
    for thread_idx in range(0, len(yay)):
        first_name = get_values_for_key('firstName', yay['elements'][thread_idx]['participants'][0])
        last_name = get_values_for_key('lastName', yay['elements'][thread_idx]['participants'][0])
        full_name = first_name[0] + " " + last_name[0]
        
        profile_urn = get_values_for_key('dashEntityUrn', yay['elements'][thread_idx]['participants'][0])
        # print(profile_urn)
        regex = r"profile:(.+)"
        match = re.search(regex, profile_urn[0])
        if match:
            result = match.group(1)
            # print(result)
            # uu = api.get_conversation(result)
            # print(uu)
        
            convo_list.append([full_name, result])
        
        # for message_idx in range(0, len(yay['elements'][thread_idx]['events'])):
            # cleaned_up_convo = get_values_for_key('text', yay['elements'][thread_idx]['events'][message_idx])
            # print(cleaned_up_convo) 
            
    return convo_list

def get_conversation_messages(conversation_id):
    
    email = request.json['email']
    password = request.json['password']
    api = Linkedin(email, password)

    convo_list=[]
    convo = api.get_conversation_details(conversation_id)
    
    print(convo)
        
    for message_idx in range(0, len(convo['events'])):
        cleaned_up_convo = get_values_for_key('text',convo['events'][message_idx])
        convo_list.append(cleaned_up_convo)
        # print(cleaned_up_convo)
            
    return convo_list
    
    
@app.route('/use-bingai', methods=['POST'])
def use_bingai():

    prompt = request.json['prompt']    
    ans = asyncio.run(UseBingAI(prompt))
    print(ans)

    return jsonify(success=True, message=ans)

@app.route('/receive-link', methods=['POST'])
def receive_link():

    email = request.json['email']
    password = request.json['password']
    
    api = Linkedin(email, password)
    # print(email, password)
    title = request.json
    # print("title", title)
    
    location = request.json['location']
    mutual_connections_boolean = request.json['mutualConnections']
    
    if location != '':
        location_geo_urn = get_geo_urn(api, location)
        data = q.enqueue(GetProfile, api, title, location_geo_urn, mutual_connections_boolean)
    else:
        data = q.enqueue(GetProfile, api, title, '', mutual_connections_boolean)
    # print(data)
    # time.sleep(150)
    job_id = data.get_id()
    print(job_id)
    return jsonify(success=True, message=job_id)
    

@app.route('/job-status', methods=['POST'])
def job_status():

    job_id = request.json['jobId']

    job = q.fetch_job(job_id)
    job_status = job.get_status()
    return jsonify(success=True, status=job_status, result=job.result)
    
# @app.route('/get-interests', methods=['POST'])
# def get_interests():

    # email = request.json['email']
    # password = request.json['password']
    # api = Linkedin(email, password)
    
    

    # public_id = request.json
    # # print("get_interests", public_id['publicId'])
    # data = ModelAndReturnTopicList(api, public_id['publicId'])
    # # print(data)
    
    # return jsonify(success=True, message=data)
    
def GetPeopleInterests(request_json):

    email = request_json['email']
    password = request_json['password']
    
    api = Linkedin(email, password)

    profile_urn = request_json['profileUrn']
    # print(profile_urn)

    person_interests = api._fetch(f"/graphql?includeWebMetadata=true&variables=(profileUrn:urn%3Ali%3Afsd_profile%3A{profile_urn},sectionType:interests,tabIndex:1,locale:en_US)&&queryId=voyagerIdentityDashProfileComponents.38247e27f7b9b2ecbd8e8452e3c1a02c")
    person_interests = person_interests.json()
    person_interests_json = json.dumps(person_interests)

    # print(type(person_interests))
    # print(person_interests_json)

    # ============= Getting interests of People =============================
    pattern = re.compile(r'"(urn:li:fsd_profile:[^"]*)"')
    matches = re.findall(pattern, person_interests_json)
    # print(matches)
    people_the_profile_is_interested_in_set = set(matches)
    people_the_profile_is_interested_in = [s.split(':')[-1] for s in people_the_profile_is_interested_in_set]

    print(people_the_profile_is_interested_in)

    # Get the profile urn, get the name and store in another list
    final_people_the_profile_is_interested_in = []
    for profile_urn in people_the_profile_is_interested_in:
    
        temp = api.get_profile(profile_urn)
        first_name = temp['firstName']
        last_name = temp['lastName']
        full_name = first_name + " " + last_name 
        final_people_the_profile_is_interested_in.append([full_name, profile_urn])

    print(final_people_the_profile_is_interested_in)
    print(len(final_people_the_profile_is_interested_in))
    # ============= Getting interests of People =============================
    
    return final_people_the_profile_is_interested_in

 
@app.route('/get-people-interests', methods=['POST'])
def get_people_interests():

    data = q.enqueue(GetPeopleInterests, request.json)
    
    job_id = data.get_id()
    
    return jsonify(success=True, message=job_id)
    
    
    
def GetCompanyInterests(request_json):

    email = request_json['email']
    password = request_json['password']
    api = Linkedin(email, password)

    public_id = request_json
    profile_urn = request_json['profileUrn']
    
    person_interests = api._fetch(f"/graphql?includeWebMetadata=true&variables=(profileUrn:urn%3Ali%3Afsd_profile%3A{profile_urn},sectionType:interests,tabIndex:1,locale:en_US)&&queryId=voyagerIdentityDashProfileComponents.38247e27f7b9b2ecbd8e8452e3c1a02c")
    person_interests = person_interests.json()
    person_interests_json = json.dumps(person_interests)
    
    # ============= Getting first 20 interests of Companies =============================
    pattern_for_company = re.compile(r'"(urn:li:fsd_company:[^"]*)"')
    matches_for_company = re.findall(pattern_for_company, person_interests_json)
    
    # print(matches)
    
    companies_the_profile_is_interested_in_set = set(matches_for_company)
    companies_the_profile_is_interested_in = [s.split(':')[-1] for s in companies_the_profile_is_interested_in_set]
    
    # get the profile urn, get the name and store in another list
    final_companies_the_profile_is_interested_in = []
    for company_id in companies_the_profile_is_interested_in:
        temp = api.get_company(company_id)
        # print(temp)
        company_name = temp['universalName']
        final_companies_the_profile_is_interested_in.append([company_name, company_id])

    print(final_companies_the_profile_is_interested_in)
    print(len(final_companies_the_profile_is_interested_in))
    # ============= Getting first 20 interests of Companies =============================
    
    return final_companies_the_profile_is_interested_in
    

@app.route('/get-company-interests', methods=['POST'])
def get_company_interests():

    data = q.enqueue(GetCompanyInterests, request.json)
    
    job_id = data.get_id()
    
    return jsonify(success=True, message=job_id)
 
# @app.route('/get-interests-from-thread', methods=['POST'])
# def get_interests_from_thread():
    
    
    # email = request.json['email']
    # password = request.json['password']
    # api = Linkedin(email, password)

    # profile_urn = request.json['publicId']
    # # print("get_interests", public_id['publicId'])
    # data = ModelAndReturnTopicList(api,profile_urn)
    # # print(data)
    
    # return jsonify(success=True, message=data)
    
@app.route('/get-convo-threads', methods=['POST'])
def get_convo_threads():

    email = request.json['email']
    password = request.json['password']
    print(email)
    
    # api = Linkedin(email, password)
    # print("api", api)
    data = get_conversation_threads(email, password)
    print("da", data)
    
    return jsonify(success=True, message=data)

@app.route('/get-convo-messages', methods=['POST'])
def get_convo_messages():

    
    email = request.json['email']
    password = request.json['password']
    api = Linkedin(email, password)
    

    profile_urn = request.json['profileUrn']
    # print(profile_urn)
    data = get_conversation_messages(profile_urn)
    # print(data)
    
    return jsonify(success=True, message=data)

@app.route('/send-connect', methods=['POST'])
def send_connect():

    email = request.json['email']
    password = request.json['password']
    api = Linkedin(email, password)

    profile_id = request.json['profileId']
    text = request.json['text']
    # data = SendConnect(api, profile_id, text)
    error_boolean = api.add_connection(profile_id, text)
    return jsonify(success=True, message=error_boolean)

@app.route('/send-message', methods=['POST'])
def send_message():

    email = request.json['email']
    password = request.json['password']
    api = Linkedin(email, password)

    profile_id = request.json['profileId']
    print(profile_id)
    text = request.json['text']
    print(text)
    data = api.send_message(message_body = text, recipients=[profile_id])
    print(data)
    return jsonify(success=True, message='sent message')

@app.route('/send-code', methods=['POST'])
def send_code():
    print("new", driver.page_source)
    code = request.json['code']
    print(code)
    
    code_textbox = driver.find_element(By.ID, "input__email_verification_pin")
    code_textbox.send_keys(code)
    
    code_submit_button = driver.find_element(By.ID, "email-pin-submit-button")
    code_submit_button.click()
    
    return jsonify(success=True, message="success")

# def SendCode(driver, code=None):
    # if code is None:
        # print("new", driver.page_source)

@app.route('/linkedin-login', methods=['POST'])
def linkedin_login():
    # print(request.json)
    email = request.json['email']
    password = request.json['password']    
   
    driver.get(SEED_URL)
        
    payload = {'session_key': email,
               # 'loginCsrfParam': loginCsrfParam,
               'session_password': password}
    
    email_field = driver.find_element(By.NAME, "session_key")
    password_field = driver.find_element(By.NAME, "session_password")
    
    email_field.send_keys(email)
    password_field.send_keys(password)
    
    submit_button = driver.find_element(By.CSS_SELECTOR, ".btn__primary--large")
    submit_button.click()
    
    print(driver.current_url)
    
    url = driver.current_url
    
    if (url.startswith("https://www.linkedin.com/checkpoint")):
    
        wait = WebDriverWait(driver, timeout=29)  
        captcha_iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(captcha_iframe)
        
        second_iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(second_iframe)
        
        # print("second driver", driver.page_source)
        
        third_iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(third_iframe)
        # print("driver", driver.page_source)
            
        # final_iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        # driver.switch_to.frame(final_iframe) 
        time.sleep(10)        
        # print("final iframe source", driver.page_source)
        
        # verify_button = driver.find_element(By.ID, "home_children_button")
        # # print("verify button", verify_button)
        # verify_button.click()
        
        # time.sleep(3)
        # print("html after verify_button clicked", driver.page_source)
        
        # third iframe contains button to download wav file
        switch_to_audio_button = driver.find_element(By.ID, "fc_meta_audio_btn")
        switch_to_audio_button.click()
        # print("after clicking audio button", driver.page_source)
        
        download_audio_button = driver.find_element(By.ID, "audio_download")
        download_audio_button.click()
        
        audio_response_textbox = driver.find_element(By.ID, "audio_response_field")
        
        # print(driver.page_source)
        
        # game = wait.until(EC.presence_of_element_located((By.ID, "game")))
        # print(game)
        # screenshot = driver.get_screenshot_as_base64()
        # return jsonify(success=False, message=screenshot)
        
        # Wait for the file to finish downloading
        # print(os.getcwd())
        
        downloads_folder = os.path.expanduser('~/')
        downloaded_file = None
        timeout = 10  # maximum time to wait for download to complete (in seconds)
        start_time = time.time()
        while time.time() < start_time + timeout:
            # Check for any new files in the downloads folder
            files = [f for f in os.listdir(downloads_folder) if f.endswith('.wav')]
            if files:
                # Assume the most recent file is the one we want
                downloaded_file = os.path.join(downloads_folder, max(files, key=os.path.getctime))
                break
            else:
                # Wait a bit before checking again
                time.sleep(1)

        # Get the URL of the downloaded file
        if downloaded_file:
            # url = 'file://' + os.path.abspath(downloaded_file)
            # print('Downloaded file URL:', url)
            
            r = sr.Recognizer()

            # Load the audio file
            with sr.AudioFile(downloaded_file) as source:
                audio_data = r.record(source)

            # Perform speech-to-text conversion
            try:
                text = r.recognize_google(audio_data)
                print('Transcription:', text)
                text = text.replace("-", "")
                text = text.replace(" ", "")
                print("final text", text)
                audio_response_textbox.send_keys(text)
                print(audio_response_textbox.get_attribute('value'))
           
                audio_submit_button = driver.find_element(By.ID, "audio_submit")
                
                # driver.switch_to.default_content()
                # payload = {
                    # 'csrfToken': driver.find_element(By.NAME, 'csrfToken').get_attribute('value'),
                    # 'pageInstance': driver.find_element(By.NAME, 'pageInstance').get_attribute('value'),
                    # # 'resendUrl': driver.find_element(By.NAME, 'resendUrl').get_attribute('value'),
                    # 'challengeId': driver.find_element(By.NAME, 'challengeId').get_attribute('value'),
                    # 'language': 'en-US',
                    # 'displayTime': driver.find_element(By.NAME, 'displayTime').get_attribute('value'),
                    # 'challengeSource': driver.find_element(By.NAME, 'challengeSource').get_attribute('value'),
                    # 'requestSubmissionId': driver.find_element(By.NAME, 'requestSubmissionId').get_attribute('value'),
                    # 'challengeType': driver.find_element(By.NAME, 'challengeType').get_attribute('value'),
                    # 'challengeData': driver.find_element(By.NAME, 'challengeData').get_attribute('value'),
                    # 'challengeDetails': driver.find_element(By.NAME, 'challengeDetails').get_attribute('value'),
                    # 'failureRedirectUri': driver.find_element(By.NAME, 'failureRedirectUri').get_attribute('value'),
                    # 'pin': text
                # }
                
                # VERIFY_URL = 'https://www.linkedin.com/checkpoint/challenge/verify'
                # session.post(VERIFY_URL, data=payload)
                
                audio_submit_button.click()
                time.sleep(5)

                # print(driver.page_source)
                print(driver.current_url)
                cookies = driver.manage().getCookies();
                
                if driver.current_url.startswith("https://www.linkedin.com/feed"):
                    api = Linkedin("", "", cookies)
                    return jsonify(success=True, message="success")
                else:
                    return jsonify(success=False, message="success")
                
                # return jsonify(success=True, message="success")
                
            except sr.UnknownValueError:
                print('Unable to transcribe audio')    

            
        
        else:
            print('File not found in downloads folder')
            

    
    
    return jsonify(success=True, message="success")

@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"
   
    