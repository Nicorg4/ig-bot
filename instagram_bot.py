from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

import json
import pyautogui
import datetime
import os
from time import sleep
import re
import random
from datetime import datetime, timedelta
import spacy

import tkinter as tk
from tkinter import filedialog

DRIVER = None
USER = None
COMMENTS_INDEX = 0
OPERATOR_NAME = 'Nicolas'
MIN_POSTS = 10
CYLCLES = []
CURRENT_CYCLE = None

class Cycle:
    def __init__(self, locations, places, hashtags):
        self.locations = locations
        self.places = places
        self.hashtags = hashtags

def create_new_cycle(locations, places, hashtags): #Debe recibir informacions del panel
    cycle = Cycle(locations, places, hashtags)
    CYLCLES.append(cycle)

def create_webdriver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True) # Previene que el chrome se cierre cuando se terminen las tareas (No recomendado)
    options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.instagram.com")

    return driver

def exit_webdriver():
    DRIVER.quit()

def get_user(): #Debe recibir informacions del panel
    return ['pipsdevs@gmail.com', 'pipslabteam2023']

def login_user():
    username_input = wait_for_XPATH('//*[@id="loginForm"]/div/div[1]/div/label/input')
    password_input = wait_for_XPATH('//*[@id="loginForm"]/div/div[2]/div/label/input')

    username_input.send_keys(USER[0])
    password_input.send_keys(USER[1])

    login_button = wait_for_XPATH('//*[@id="loginForm"]/div/div[3]/button')
    login_button.click()

    sleep_random()

    print('\nSe esta utilizando la cuenta de:', USER[0], '\n\n')

def comment_posts():
    if len(CURRENT_CYCLE.locations) != 0:
        for location in CURRENT_CYCLE.locations:
            if location[2] > 0:
                comment_on_location(location)
    if len(CURRENT_CYCLE.places) != 0:
        for place in CURRENT_CYCLE.places:
            if place[1] > 0:
                comment_on_place(place)
    if len(CURRENT_CYCLE.hashtags) != 0:
        for hashtag in CURRENT_CYCLE.hashtags:
            if hashtag[1] > 0:
                comment_on_hashtag(hashtag)

def comment_on_location(location):
    comment_setup("https://www.instagram.com/explore/locations/{}/{}/".format(location[1], location[0]))
    total_comments = 0
    print('----> Comentando en', '@' + location[0], '\n')
    while total_comments < location[2]:
        total_comments += commenting_process()
        if total_comments != location[2]:
            next_post()

def comment_on_place(place):
    comment_setup("https://www.instagram.com/{}/tagged/".format(place[0]))
    total_comments = 0
    print('----> Comentando en', '@' + place[0], '\n')
    while total_comments < place[1]:
        total_comments += commenting_process()
        if total_comments != place[1]:
            next_post()

def comment_on_hashtag(hashtag):
    comment_setup("https://www.instagram.com/explore/tags/{}/".format(hashtag[0]))
    print('----> Comentando en', '#' + hashtag[0], '\n')
    total_comments = 0
    while total_comments < hashtag[1]:
        total_comments += commenting_process()
        if total_comments != hashtag[1]:
            next_post()

def comment_setup(adress):
    sleep_random()
    place_address = adress
    DRIVER.get(place_address)
    sleep_random()
    first_post = wait_for_CLASS('_aagw')
    first_post.click()
    sleep_random()

def commenting_process():
    username = get_username()
    successfull_comment = 0
    if check_user_meets_criteria():
        print('[+] Comentandole a:', username[1])
        leave_comment(username[0])
        save_contacted_user(username[1])
        successfull_comment = 1
    sleep_random()
    return successfull_comment

def get_username():
    user_anchor = (wait_for_XPATH("//div[@class='xt0psk2']//a"))
    actions = ActionChains(DRIVER)
    actions.move_to_element(user_anchor).perform()
    sleep_random()
    try:
        username = DRIVER.find_element(By.XPATH, "//div[@class='xmix8c7 x1gslohp x1rva8in']//span").text
    except:
        username = user_anchor.text

    first_name = username.split()[0]
    clean_username = re.sub(r'[^a-zA-Z]+', '', first_name).capitalize()

    if not is_name(clean_username):
        clean_username = (user_anchor.text).capitalize()

    return [clean_username, user_anchor.text]

def is_name(username):
    doc_en = nlp_en(username.capitalize())
    doc_es = nlp_es(username.capitalize())

    return any(token.ent_type_ == "PERSON" for token in doc_en) or any(token.ent_type_ == "PER" for token in doc_es)

def check_user_meets_criteria():
    if user_in_db():
        print('[-] El usuario ya esta en la base de datos\n')
        return False
    if not commenting_available():
        print('[-] El usuario no puede recibir comentarios\n')
        return False
    if not post_is_new():
        print('[-] El post es demasiado antiguo\n')
        return False
    if not check_user_uploads_enough():
        print('[-] El usuario no tiene los posts suficientes\n')
        return False
    return True

def user_in_db(): #Debe recibir informacions de la base de datos
    return False

def commenting_available():
    try:
        DRIVER.find_element(By.XPATH, "//span[text()='Comments on this post have been limited.']")
        return False
    except:
        return True
    
def check_user_uploads_enough(): 
    number_of_posts = get_user_posts()

    if number_of_posts > MIN_POSTS:
        return True
    return False

def post_is_new():
    post_date = wait_for_CLASS('_aaqe').get_attribute("datetime")
    date_now = datetime.now()
    clean_post_date = datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    a_week_from_now = date_now - timedelta(days=7)

    if clean_post_date < a_week_from_now:
        return False
    return True

def get_user_posts():
    user_anchor = (wait_for_XPATH("//div[@class='xt0psk2']//a"))
    actions = ActionChains(DRIVER)
    actions.move_to_element(user_anchor).perform()
    sleep_random()
    posts = wait_for_XPATH("//div[contains(@class, 'x6s0dn4') and contains(@class, 'xrvj5dj')]/div/div/span/span").text
    number_of_posts = int(posts.replace(",", ""))
    
    return number_of_posts

def leave_comment(username):

    comment_textarea = wait_for_NAME("textarea")
    comment_textarea.click()
    updated_textarea = wait_for_NAME("textarea")
    comment = pick_comment().format(username)
    sleep_random()
    updated_textarea.send_keys(comment)

    post_button = wait_for_XPATH("//div[contains(text(),'Post')]")
    sleep_random()
    #post_button.click()
    
    return comment

def pick_comment():
    with open("data.json") as file:
        data = json.load(file)
    comments = [comment["comment"] for comment in data["comments"]]
    global COMMENTS_INDEX
    comment = comments[COMMENTS_INDEX]
    COMMENTS_INDEX += 1
    if COMMENTS_INDEX > len(comments) - 1:
        COMMENTS_INDEX = 0
    return comment
        
def save_contacted_user(username): #Debe guardar informacion en la base de datos
    print("[+]", username,"guardado en la base de datos\n")

def next_post():
    svg_elements = DRIVER.find_elements(By.TAG_NAME, "svg")
    for svg in svg_elements:
        if svg.get_attribute('aria-label') == 'Next':
            svg.click()
            break

def send_messages():
    if len(CURRENT_CYCLE.locations) != 0:
        for location in CURRENT_CYCLE.locations:
            if location[3] > 0:
                send_message_on_location(location)
    if len(CURRENT_CYCLE.places) != 0:
        for place in CURRENT_CYCLE.places:
            if place[2] > 0:
                send_message_on_place(place)
    if len(CURRENT_CYCLE.hashtags) != 0:
        for hashtag in CURRENT_CYCLE.hashtags:
            if hashtag[2] > 0:
                send_message_on_hashtag(hashtag)

def send_message_on_location(location):
    print('----> Enviando mensajes en', '@' + location[0], '\n')

def send_message_on_place(place):
    print('----> Enviando mensajes en', '@' + place[0], '\n')

def send_message_on_hashtag(hashtag):
    print('----> Enviando mensajes en', '#' + hashtag[0], '\n')

def sleep_random():
    sleep(random.uniform(4, 7))

def wait_for_XPATH(xpath):
    while True:
        try:
            element = WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            break
        except:
            continue
    return element

def wait_for_CLASS(class_name):
    while True:
        try:
            element = WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            break
        except:
            continue
    return element

def wait_for_NAME(tag_name):
    while True:
        try:
            element = WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, tag_name)))
            break
        except:
            continue
    return element

def start_bot():
    global DRIVER
    global USER 

    if CURRENT_CYCLE == CYLCLES[0]:
        DRIVER = create_webdriver()
        USER = get_user()
        login_user()
    comment_posts()
    send_messages()
    if CURRENT_CYCLE == CYLCLES[-1]:
        exit_webdriver()

### EJECUCION ####

#Los ciclos deben ser creados desde el panel
create_new_cycle([['miami-beach-florida', '212928653', 2, 1]], [], [])
create_new_cycle([], [['kikiontheriver', 2, 1]], [['tomorrowland', 2, 1]])

nlp_en = spacy.load('en_core_web_sm')
nlp_es = spacy.load('es_core_news_sm')

for cycle in CYLCLES:
    print("#### Iniciando ciclo ####\n")
    CURRENT_CYCLE = cycle
    start_bot()
