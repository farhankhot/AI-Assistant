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
import pickle

q = Queue(connection=conn)

app = Flask(__name__)

SEED_URL = 'https://www.linkedin.com/login'

session = requests.Session() 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-dev-shm-usage')
chrome_options.add_argument('window-size=1920x1480')

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
desired_capabilities = DesiredCapabilities.CHROME.copy()
desired_capabilities['acceptInsecureCerts'] = True

prefs = {"download.default_directory": r"~/",
        "directory_upgrade": True}

chrome_options.add_experimental_option("prefs", prefs)

chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options,
desired_capabilities=desired_capabilities)

# cookies_list = [
# {
    # "domain": ".www.linkedin.com",
    # "expirationDate": 1712716185.471855,
    # "hostOnly": False,
    # "httpOnly": False,
    # "name": "G_ENABLED_IDPS",
    # "path": "/",
    # "sameSite": None,
    # "secure": False,
    # "session": False,
    # "storeId": None,
    # "value": "google"
# },
# {
    # "domain": ".linkedin.com",
    # "expirationDate": 1709692200.726415,
    # "hostOnly": False,
    # "httpOnly": False,
    # "name": "bcookie",
    # "path": "/",
    # "sameSite": "no_restriction",
    # "secure": True,
    # "session": False,
    # "storeId": None,
    # "value": "\"v=2&8ac1832a-1a62-40b1-8feb-836eaeaef11f\""
# },
# {
    # "domain": "www.linkedin.com",
    # "expirationDate": 1678309394.355053,
    # "hostOnly": True,
    # "httpOnly": False,
    # "name": "fid",
    # "path": "/",
    # "sameSite": None,
    # "secure": False,
    # "session": False,
    # "storeId": None,
    # "value": "AQEiYoDdgkUr9AAAAYae_IEC3x5bzU00hYI2U0uD-km_8WndTQr3atuxbAxFhsaxFT1mn8EofhBz7Q"
# },
# {
    # "domain": "www.linkedin.com",
    # "expirationDate": 1693708178,
    # "hostOnly": True,
    # "httpOnly": False,
    # "name": "g_state",
    # "path": "/",
    # "sameSite": None,
    # "secure": False,
    # "session": False,
    # "storeId": None,
    # "value": "{\"i_l\":3,\"i_p\":1678760978978}"
# },
# {
    # "domain": ".www.linkedin.com",
    # "expirationDate": 1709692200.726354,
    # "hostOnly": False,
    # "httpOnly": True,
    # "name": "li_at",
    # "path": "/",
    # "sameSite": "no_restriction",
    # "secure": True,
    # "session": False,
    # "storeId": None,
    # "value": "AQEDAReEU6IAnGyYAAABhrnnetIAAAGG3fP-0lYAc8O01hCt_wRtE-nShHjyZm_inTYnD9HgQ-BvXSO0TPnMBmcATdNmvpmU2HB7PpQFVLKJn0vUec9NUc7jTAaMGW7L7jdVs1KUfXRRK7TN6dMuXVIg"
# },
# {
    # "domain": ".linkedin.com",
    # "hostOnly": False,
    # "httpOnly": False,
    # "name": "lang",
    # "path": "/",
    # "sameSite": "no_restriction",
    # "secure": True,
    # "session": True,
    # "storeId": None,
    # "value": "v=2&lang=en-us"
# },
# {
    # "domain": ".linkedin.com",
    # "expirationDate": 1678242600.890006,
    # "hostOnly": False,
    # "httpOnly": False,
    # "name": "lidc",
    # "path": "/",
    # "sameSite": "no_restriction",
    # "secure": True,
    # "session": False,
    # "storeId": None,
    # "value": "\"b=OB30:s=O:r=O:a=O:p=O:g=3526:u=10:x=1:i=1678156200:t=1678242600:v=2:sig=AQFdAG0wtgLrbvEobVI6nOPhmfaNiG7Y\""
# },
# {
    # "domain": ".www.linkedin.com",
    # "expirationDate": 1709692200.726434,
    # "hostOnly": False,
    # "httpOnly": True,
    # "name": "bscookie",
    # "path": "/",
    # "sameSite": "no_restriction",
    # "secure": True,
    # "session": False,
    # "storeId": None,
    # "value": "\"v=1&202301191743020e425572-9697-4266-8d06-e5bfd24ae794AQG0b_kpGiEXydi0cGvMlrGaQ6KvPyzZ\""
# },
# {
    # "domain": ".www.linkedin.com",
    # "expirationDate": 1685932200.726405,
    # "hostOnly": False,
    # "httpOnly": False,
    # "name": "JSESSIONID",
    # "path": "/",
    # "sameSite": "no_restriction",
    # "secure": True,
    # "session": False,
    # "storeId": None,
    # "value": "\"ajax:4076532646350810552\""
# },
# {
    # "domain": ".www.linkedin.com",
    # "expirationDate": 1709692200.726277,
    # "hostOnly": False,
    # "httpOnly": True,
    # "name": "li_rm",
    # "path": "/",
    # "sameSite": "no_restriction",
    # "secure": True,
    # "session": False,
    # "storeId": None,
    # "value": "AQGaQ1AkJKJX1gAAAYazomBRfil0bK-ooeEbqRebyOm2vZtfNqUJfwNRTLR8pxe2e2sVGcd3ai_2WzvgDgtf9eyCM-GmKmRQGvVl3G8U-epeNTsM1oczOJ5g"
# },
# {
    # "domain": ".www.linkedin.com",
    # "expirationDate": 1693704601,
    # "hostOnly": False,
    # "httpOnly": False,
    # "name": "li_theme",
    # "path": "/",
    # "sameSite": None,
    # "secure": True,
    # "session": False,
    # "storeId": None,
    # "value": "light"
# },
# {
    # "domain": ".www.linkedin.com",
    # "expirationDate": 1693704601,
    # "hostOnly": False,
    # "httpOnly": False,
    # "name": "li_theme_set",
    # "path": "/",
    # "sameSite": None,
    # "secure": True,
    # "session": False,
    # "storeId": None,
    # "value": "app"
# },
# {
    # "domain": ".linkedin.com",
    # "expirationDate": 1685932200.726369,
    # "hostOnly": False,
    # "httpOnly": False,
    # "name": "liap",
    # "path": "/",
    # "sameSite": "no_restriction",
    # "secure": True,
    # "session": False,
    # "storeId": None,
    # "value": "True"
# },
# {
    # "domain": "www.linkedin.com",
    # "hostOnly": True,
    # "httpOnly": False,
    # "name": "PLAY_LANG",
    # "path": "/",
    # "sameSite": None,
    # "secure": False,
    # "session": True,
    # "storeId": None,
    # "value": "en"
# },
# {
    # "domain": "www.linkedin.com",
    # "hostOnly": True,
    # "httpOnly": True,
    # "name": "PLAY_SESSION",
    # "path": "/",
    # "sameSite": "lax",
    # "secure": True,
    # "session": True,
    # "storeId": None,
    # "value": "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InNlc3Npb25faWQiOiJiNzFhMjU1ZS04YzU5LTRmYTctYjAzZC05ODQwNzJjZTRiNzR8MTY3Njk1MTAxOCIsImFsbG93bGlzdCI6Int9IiwicmVjZW50bHktc2VhcmNoZWQiOiIiLCJyZWZlcnJhbC11cmwiOiJodHRwczovL3d3dy5saW5rZWRpbi5jb20vZGV2ZWxvcGVycy9hcHBzL25ldz9zcmM9b3Itc2VhcmNoJnZlaD13d3cuZ29vZ2xlLmNvbSIsImFpZCI6IiIsIlJOVC1pZCI6InwwIiwicmVjZW50bHktdmlld2VkIjoiNTQ4MzYwfDEzNDEzODd8NTIyOTM1fDUxMjQwNSIsIkNQVC1pZCI6IsOrR0nDrV46TMKowoDDsDE7Ti12VyIsImZsb3dUcmFja2luZ0lkIjoiR29rdXBOdHNSYjJNcmlUei9VWm5nUT09IiwiZXhwZXJpZW5jZSI6ImVudGl0eSIsImlzX25hdGl2ZSI6ImZhbHNlIiwidHJrIjoiIn0sIm5iZiI6MTY3Njk1MzI3NiwiaWF0IjoxNjc2OTUzMjc2fQ.QWV2AriMTimBGvDdnirV4cvb8F-S39vfogz-AF9Hufg"
# },
# {
    # "domain": ".linkedin.com",
    # "hostOnly": False,
    # "httpOnly": False,
    # "name": "sdsc",
    # "path": "/",
    # "sameSite": "no_restriction",
    # "secure": True,
    # "session": True,
    # "storeId": None,
    # "value": "1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D"
# },
# {
    # "domain": ".www.linkedin.com",
    # "expirationDate": 1679362201,
    # "hostOnly": False,
    # "httpOnly": False,
    # "name": "timezone",
    # "path": "/",
    # "sameSite": None,
    # "secure": True,
    # "session": False,
    # "storeId": None,
    # "value": "America/New_York"
# },
# {
    # "domain": ".linkedin.com",
    # "expirationDate": 1680744602,
    # "hostOnly": False,
    # "httpOnly": False,
    # "name": "UserMatchHistory",
    # "path": "/",
    # "sameSite": "no_restriction",
    # "secure": True,
    # "session": False,
    # "storeId": None,
    # "value": "AQKhbmYv6v4RjwAAAYa554JBBK31KtqudlqDZL_43uzc5uCaMT5zs7Mn07uXW93z5dDFPJb1QZnpGcm6Mkqj02Dy87GxwL0ZBOWWa2xi244YNZDm_zNqNiSAVzk0I7GbDwbZ2eBhQlDLX0OYZbHTjWhfLFxkXg0x5vAACRN3IqNUkRXfGPfsr9csvgnUI4_Ul6Y1jNnB19Edl31007UJo6KBvEluXjPlqAdS6dlyBeieTVkKbhX9kSkkGwpRYXCxQVmdo47Gzw"
# },
# {
    # "domain": ".linkedin.com",
    # "expirationDate": 1712702472.149992,
    # "hostOnly": False,
    # "httpOnly": False,
    # "name": "visit",
    # "path": "/",
    # "sameSite": "no_restriction",
    # "secure": True,
    # "session": False,
    # "storeId": None,
    # "value": "v=1&M"
# }
# ]
    
# cookie_dict = {}
# for single_dict in cookies_list:
    # temp = single_dict["value"].strip('"')
    # cookie_dict[single_dict["name"]] = temp

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

def GetProfile(email, password, cookie_dict, search_params, location, mutual_connections_boolean):

    print("location", location)
    
    # cookie_filename = "linkedin_cookies_{}.pickle".format(email)    
    # with open(cookie_filename, "rb") as infile:
        # cookie_dict = pickle.load(infile)
    
    api = Linkedin(email, password, cookies=cookie_dict)
    
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
        
    res = api._fetch(f"/typeahead/hitsV2?keywords={location}&origin=OTHER&q=type&queryContext=List(geoVersion-%3E3,bingGeoSubTypeFilters-%3EMARKET_AREA%7CCOUNTRY_REGION%7CADMIN_DIVISION_1%7CCITY)&type=GEO")

    # res = api._fetch(f"/me")
    # print(res.json()['elements'][0]['targetUrn'])
    geo_urn = res.json()['elements'][0]['targetUrn'] # Output: urn:li:fs_geo:103644278
    geo_urn = re.search("\d+", geo_urn).group()
    return geo_urn

def get_conversation_threads(email, password, cookie_dict):
    print("nn", email)
    
    api = Linkedin(email, password, cookies=cookie_dict)
    
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
    cookie_dict = request.json['cookie']
    # print(email, password)
    
    # cookie_filename = "linkedin_cookies_{}.pickle".format(email)    
    # with open(cookie_filename, "rb") as infile:
        # cookie_dict = pickle.load(infile)
    
    api = Linkedin(email, password, cookies=cookie_dict)
        
    title = request.json
    # print("title", title)
    
    location = request.json['location']
    mutual_connections_boolean = request.json['mutualConnections']
    
    if location != '':
        location_geo_urn = get_geo_urn(api, location)
        data = q.enqueue(GetProfile, email, password, cookie_dict, title, location_geo_urn, mutual_connections_boolean)
        # data = q.enqueue(GetProfile, api, title, location_geo_urn, mutual_connections_boolean)

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

    person_interests = api._fetch(f"/graphql?includeWebMetadata=True&variables=(profileUrn:urn%3Ali%3Afsd_profile%3A{profile_urn},sectionType:interests,tabIndex:1,locale:en_US)&&queryId=voyagerIdentityDashProfileComponents.38247e27f7b9b2ecbd8e8452e3c1a02c")
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
    
    person_interests = api._fetch(f"/graphql?includeWebMetadata=True&variables=(profileUrn:urn%3Ali%3Afsd_profile%3A{profile_urn},sectionType:interests,tabIndex:1,locale:en_US)&&queryId=voyagerIdentityDashProfileComponents.38247e27f7b9b2ecbd8e8452e3c1a02c")
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
    cookies_list = request.json['cookie']
    
    cookie_dict = {}
    for single_dict in cookies_list:
        temp = single_dict["value"].strip('"')
        cookie_dict[single_dict["name"]] = temp
    
    # cookie_dict = dict(zip(range(len(cookie_dict)), cookie_dict))
    
    # print(cookie_dict)
    # print(type(cookie_dict))
    # print(email)
    
    # api = Linkedin(email, password)
    # print("api", api)
    data = get_conversation_threads(email, password, cookie_dict)
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

@app.route('/captcha-ans', methods=['POST'])
def captcha_ans():
    time.sleep(6)
    print("new", driver.page_source)
    code = request.json['code']
    print("code from captcha ans: ", code)
    code = "image"+code
    
    # Get the image li's
    li_elements = driver.find_element(By.CSS_SELECTOR, 'ul.my-class > li')
    
    for li in li_elements:
        if code == li.get_attribute("id"):
            li.click()
    
            time.sleep(2)
            print(driver.current_url)
       
    # return jsonify(success=True, message="success")

@app.route('/save-cookie', methods=['POST'])
def save_cookie():
    
    email = request.json['email']
    password = request.json['password'] 
    cookies_list = request.json['cookie']    
    
    cookie_dict = {}
    for single_dict in cookies_list:
        temp = single_dict["value"].strip('"')
        cookie_dict[single_dict["name"]] = temp
    
    # TODO: TRY CATCH HERE
    api = Linkedin(email, password, cookies=cookie_dict)
    
    # Save cookie_dict
    cookie_filename = "linkedin_cookies_{}.pickle".format(email)
    with open(cookie_filename, "wb") as f:
        pickle.dump(cookie_dict, f)
        
    return jsonify(success=True, message="success")


@app.route('/linkedin-login', methods=['POST'])
def linkedin_login():
    
    email = request.json['email']
    password = request.json['password']    
    
    # api = Linkedin(email, password)
    api = Linkedin(email, password, cookies= cookie_dict)
    
    location = 'usa'
    res = api._fetch(f"/typeahead/hitsV2?keywords={location}&origin=OTHER&q=type&queryContext=List(geoVersion-%3E3,bingGeoSubTypeFilters-%3EMARKET_AREA%7CCOUNTRY_REGION%7CADMIN_DIVISION_1%7CCITY)&type=GEO")
    print("yay", res)
    geo_urn = res.json()['elements'][0]['targetUrn'] # Output: urn:li:fs_geo:103644278
    geo_urn = re.search("\d+", geo_urn).group()
    print(geo_urn)
    
   
    # driver.get(SEED_URL)
    
    # # print(driver.get_cookies())    
    
    # login_csrf_param = driver.find_element(By.NAME, "loginCsrfParam").get_attribute('value')   

    # payload = {'session_key': email,
               # 'loginCsrfParam': login_csrf_param,
               # 'session_password': password}
                   
    # email_field = driver.find_element(By.NAME, "session_key")
    # password_field = driver.find_element(By.NAME, "session_password")
    
    # email_field.send_keys(email)
    # password_field.send_keys(password)
    
    # submit_button = driver.find_element(By.CSS_SELECTOR, ".btn__primary--large")
    # submit_button.click()
            
    # print(driver.current_url)
    
    # url = driver.current_url
    
    # # api = Linkedin(email, password)
    
    # if (url.startswith("https://www.linkedin.com/checkpoint")):
        
        # # print(driver.page_source)
        
        # wait = WebDriverWait(driver, timeout=29)  
        # captcha_iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        # driver.switch_to.frame(captcha_iframe)
        
        # second_iframe = driver.find_element(By.TAG_NAME, "iframe")
        # driver.switch_to.frame(second_iframe)
        
        # # print("second driver", driver.page_source)
        
        # third_iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        # driver.switch_to.frame(third_iframe)
        
        # # ============================ IMAGE VERSION ==================================================
        # image_iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        
        # iframe_width = image_iframe.size['width']
        # iframe_height = image_iframe.size['height']
        # iframe_x = image_iframe.location['x']
        # iframe_y = image_iframe.location['y']
        
        # driver.switch_to.frame(image_iframe)
        
        # time.sleep(5)
        
        # # print(driver.page_source)
        
        # driver.find_element(By.ID, "home_children_button").click()
        
        # time.sleep(2)
        
        # # print("driver", driver.page_source)
                    
        # # print("html after verify_button clicked", driver.page_source)
        
        # # screenshot = driver.get_screenshot_as_png()

        # # # Crop the screenshot to only the contents of the iframe
        # # from PIL import Image
        # # screenshot = Image.open(screenshot)
        # # iframe_screenshot = screenshot.crop((iframe_x, iframe_y, iframe_x + iframe_width, iframe_y + iframe_height))
        
        # screenshot = driver.get_screenshot_as_base64()
        # driver.switch_to.default_content()
        # return jsonify(success=False, message=screenshot)  
        # ============================ IMAGE VERSION ==================================================        
        
        # # ==================== SOUND VERSION =================================================
        # # TODO: CASE WHERE NEW CAPTCHA APPEARS WITHOUT A DOWNLOAD BUTTON, ONLY PLAY BUTTON
              # # DIFFERENT TYPES OF QUESTIONS ASKED 
        
        # # third iframe contains button to download wav file
        # switch_to_audio_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fc_meta_audio_btn"]')))
                
        # switch_to_audio_button.send_keys("\n")
    
        # time.sleep(5) 
        
        # # screenshot = driver.get_screenshot_as_base64()
        # # return jsonify(success=False, message=screenshot) 
        
        # # download_audio_button = wait.until(EC.presence_of_element_located((By.ID, "audio_download")))
        
        # # time.sleep(5)                
        
        # # download_audio_button.click()
        
        # print(driver.page_source)
        
        # # ================================ Pushing play button ==============================
        # audio_play_button = driver.find_element(By.ID, "audio_play").click()
        # time.sleep(5)
        # # Get the audio tag src
        # audio_tag = driver.find_element(By.ID, "fc_audio_el")
        # audio_src_b64 = audio_tag.get_attribute("src")
        # print(audio_src_b64)
        # import base64
        # downloaded_file = open("temp.wav", "wb")
        # decode_string = base64.b64decode(audio_src_b64)
        # downloaded_file.write(decode_string)
        # print(downloaded_file)
        # # ================================ Pushing play button ==============================
        
        # audio_response_textbox = driver.find_element(By.ID, "audio_response_field")        
        
        # downloads_folder = os.path.expanduser('~/')
        # downloaded_file = None
        # timeout = 10  # maximum time to wait for download to complete (in seconds)
        # start_time = time.time()
        # while time.time() < start_time + timeout:
            # # Check for any new files in the downloads folder
            # files = [f for f in os.listdir(downloads_folder) if f.endswith('.wav')]
            # if files:
                # # Assume the most recent file is the one we want
                # downloaded_file = os.path.join(downloads_folder, max(files, key=os.path.getctime))
                # break
            # else:
                # # Wait a bit before checking again
                # time.sleep(1)

        # if downloaded_file:
            
            # # Perform speech-to-text conversion
            # key = "sk-BQ0tK7GxoNDv0zYjTkT1T3BlbkFJ2TAJQSSJ4UEYSrDPn68"
            # final_key = key + "7"
            # try:
                # import openai
                # openai.api_key = final_key
                # audio_file = open(os.path.abspath(downloaded_file), "rb")
                # text = openai.Audio.transcribe("whisper-1", audio_file) 
                # text = text["text"]
                # # text = r.recognize_google(audio_data)
                # print('Transcription:', text)
                # text = text.replace("-", "")
                # text = text.replace(",", "")
                # text = text.replace(" ", "")
                # text = text.replace(".", "")

                # print("final text", text)
                
                # audio_response_textbox.send_keys(text)
                # print(audio_response_textbox.get_attribute('value'))
           
                # audio_submit_button = driver.find_element(By.ID, "audio_submit")
                                
                # audio_submit_button.click()           

                # time.sleep(5)
                # # print(driver.page_source)

                # print("cssq", driver.current_url)
                                                
                # cookie_dict = {}
                # for single_dict in driver.get_cookies():
                    # temp = single_dict["value"].strip('"')
                    # cookie_dict[single_dict["name"]] = temp
                    
                # api = Linkedin(email, password, cookies=cookie_dict)
                
                # # Save cookie_dict
                # cookie_filename = "linkedin_cookies_{}.pickle".format(email)
                # with open(cookie_filename, "wb") as f:
                    # # json.dump(cookie_dict, f)
                    # pickle.dump(cookie_dict, f)
                
                # # location = 'usa'
                # # res = api._fetch(f"/typeahead/hitsV2?keywords={location}&origin=OTHER&q=type&queryContext=List(geoVersion-%3E3,bingGeoSubTypeFilters-%3EMARKET_AREA%7CCOUNTRY_REGION%7CADMIN_DIVISION_1%7CCITY)&type=GEO")
                # # print("yay", res)
                # # geo_urn = res.json()['elements'][0]['targetUrn'] # Output: urn:li:fs_geo:103644278
                # # geo_urn = re.search("\d+", geo_urn).group()
                # # print(geo_urn)
                # # return jsonify(success=True, message="success")
                
            # except sr.UnknownValueError:
                # print('Unable to transcribe audio')
        
        # else:
            # print('File not found in downloads folder')
        # # ==================== SOUND VERSION =================================================
    
    return jsonify(success=True, message="success")

@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"
   
    