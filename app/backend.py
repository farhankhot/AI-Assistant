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
import os
import sys
import pickle

q = Queue(connection=conn)

app = Flask(__name__)

async def UseBingAI(prompt):
    
    # This is getting my own cookie.json
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
    
    api = Linkedin(email, password, cookies=cookie_dict)
    
    
    convo_list=[]
    yay = api.get_conversations()

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
        
    for message_idx in range(0, len(convo['events'])):
        cleaned_up_convo = get_values_for_key('text',convo['events'][message_idx])
        convo_list.append(cleaned_up_convo)
        # print(cleaned_up_convo)
            
    return convo_list
    
def GetPeopleInterests(email, password, cookie_dict, profile_urn):
    
    api = Linkedin(email, password, cookies=cookie_dict)
    
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
    
def GetCompanyInterests(email, password, cookie_dict, public_id, profile_urn):
    
    api = Linkedin(email, password, cookies=cookie_dict)
    
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
    

# ================================================ ROUTES START =============================================

@app.route('/use-bingai', methods=['POST'])
def use_bingai():

    prompt = request.json['prompt']    
    ans = asyncio.run(UseBingAI(prompt))
    
    # print(ans)

    return jsonify(success=True, message=ans)

@app.route('/receive-link', methods=['POST'])
def receive_link():

    email = request.json['email']
    password = request.json['password']
    
    # print(email, password)
    
    # cookie_filename = "linkedin_cookies_{}.pickle".format(email)    
    # with open(cookie_filename, "rb") as infile:
        # cookie_dict = pickle.load(infile)
    
    cookies_list = request.json['cookie']
    cookie_dict = {}
    for single_dict in cookies_list:
        temp = single_dict["value"].strip('"')
        cookie_dict[single_dict["name"]] = temp
    
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
        data = q.enqueue(GetProfile, email, password, cookie_dict, title, '', mutual_connections_boolean)
        
    # print(data)
    
    job_id = data.get_id()
    
    # print(job_id)
    
    return jsonify(success=True, message=job_id)
    
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

@app.route('/job-status', methods=['POST'])
def job_status():

    job_id = request.json['jobId']
    job = q.fetch_job(job_id)
    job_status = job.get_status()
    
    return jsonify(success=True, status=job_status, result=job.result)

@app.route('/get-people-interests', methods=['POST'])
def get_people_interests():

    email = request.json['email']
    password = request.json['password']
    
    cookies_list = request.json['cookie']
    cookie_dict = {}
    for single_dict in cookies_list:
        temp = single_dict["value"].strip('"')
        cookie_dict[single_dict["name"]] = temp

    profile_urn = request.json['profileUrn']
    
    data = q.enqueue(GetPeopleInterests, email, password, cookie_dict, profile_urn)
    
    job_id = data.get_id()
    
    return jsonify(success=True, message=job_id)

@app.route('/get-company-interests', methods=['POST'])
def get_company_interests():

    email = request.json['email']
    password = request.json['password']
    
    cookies_list = request.json['cookie']
    cookie_dict = {}
    for single_dict in cookies_list:
        temp = single_dict["value"].strip('"')
        cookie_dict[single_dict["name"]] = temp
    
    public_id = request.json
    profile_urn = request.json['profileUrn']

    data = q.enqueue(GetCompanyInterests, email, password, cookie_dict, public_id, profile_urn)
    
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
    # print("get_convo_threads data: ", data)
    
    return jsonify(success=True, message=data)

@app.route('/get-convo-messages', methods=['POST'])
def get_convo_messages():

    email = request.json['email']
    password = request.json['password']
    
    cookies_list = request.json['cookie']
    cookie_dict = {}
    for single_dict in cookies_list:
        temp = single_dict["value"].strip('"')
        cookie_dict[single_dict["name"]] = temp

    api = Linkedin(email, password, cookies=cookie_dict)

    profile_urn = request.json['profileUrn']
    # print(profile_urn)
    data = get_conversation_messages(profile_urn)
    # print(data)
    
    return jsonify(success=True, message=data)

@app.route('/send-connect', methods=['POST'])
def send_connect():

    email = request.json['email']
    password = request.json['password']
    cookies_list = request.json['cookie']
    cookie_dict = {}
    for single_dict in cookies_list:
        temp = single_dict["value"].strip('"')
        cookie_dict[single_dict["name"]] = temp

    api = Linkedin(email, password, cookies=cookie_dict)

    profile_id = request.json['profileId']
    text = request.json['text']
    # data = SendConnect(api, profile_id, text)
    error_boolean = api.add_connection(profile_id, text)
    return jsonify(success=True, message=error_boolean)

@app.route('/send-message', methods=['POST'])
def send_message():

    email = request.json['email']
    password = request.json['password']
    
    cookies_list = request.json['cookie']
    cookie_dict = {}
    for single_dict in cookies_list:
        temp = single_dict["value"].strip('"')
        cookie_dict[single_dict["name"]] = temp
    
    api = Linkedin(email, password, cookies=cookie_dict)

    profile_id = request.json['profileId']
    print(profile_id)
    text = request.json['text']
    print(text)
    data = api.send_message(message_body = text, recipients=[profile_id])
    print(data)
    return jsonify(success=True, message='sent message')

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

    # ================== NOT NEEDED, SAVING IN LOCAL STORAGE ==================
    # Save cookie_dict
    # cookie_filename = "linkedin_cookies_{}.pickle".format(email)
    # with open(cookie_filename, "wb") as f:
        # pickle.dump(cookie_dict, f)
    # ================== NOT NEEDED, SAVING IN LOCAL STORAGE ==================
        
    return jsonify(success=True, message="success")
    
# ================================================ ROUTES END =============================================
