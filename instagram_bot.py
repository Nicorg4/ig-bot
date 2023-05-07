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

import tkinter as tk
from tkinter import filedialog

DRIVER = None
USER = None
COMMENTS_INDEX = 0

OPERATOR_NAME = 'Nicolas'
LOCATIONS = [['miami-beach-florida', '212928653', 3, 1]] #[LOCATION, LOCATION_ID, COMMENTS, MESSAGES]
PLACES = [['kikiontheriver', 3, 1]] #[PLACE, COMMENTS, MESSAGES]
HASHTAGS = [['messi', 3, 1]] #[HASHTAG, COMMENTS, MESSAGES]
COMMENTS = ['Hey {} I have a proposal for you!, could you DM me please?', 'Hi {} I have a proposal for you!, could you DM me please?']
DMS = ['Hi {}, are you there?', 'Hello {}… do you have a minute?!', 'Good afternoon {}, how are you doing?', '{}, can we talk a moment?', 'Nice to meet you {}, can I talk to you for a minute?', 'How are you {}?' + OPERATOR_NAME + 'here!!'] 
MIN_POSTS = 10

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

def get_user():
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
    if len(LOCATIONS) != 0:
        for location in LOCATIONS:
            if location[2] > 0:
                comment_on_location(location)
    if len(PLACES) != 0:
        for place in PLACES:
            if place[1] > 0:
                comment_on_place(place)
    if len(HASHTAGS) != 0:
        for hashtag in HASHTAGS:
            if hashtag[1] > 0:
                comment_on_hashtag(hashtag)

def comment_on_location(location):
    wait_for_XPATH("//button[contains(text(),'Save Info')]")
    sleep_random()
    location_address = "https://www.instagram.com/explore/locations/{}/{}/".format(location[1], location[0])
    DRIVER.get(location_address)
    print('----> Comentando en', '@' + location[0], '\n')
    sleep_random()
    first_post = wait_for_CLASS('_aagw')
    first_post.click()
    sleep_random()
    total_comments = 0
    while total_comments < location[2]:
        username = get_username()
        if check_user_meets_criteria():
            print('[+] Comentandole a:', username)
            leave_comment(username)
            save_contacted_user(username)
            total_comments += 1
        sleep_random()
        if total_comments != location[2]:
            next_post()

def comment_on_place(place):
    sleep_random()  
    place_address = "https://www.instagram.com/{}/tagged/".format(place[0])
    DRIVER.get(place_address)
    print('----> Comentando en', '@' + place[0], '\n')
    sleep_random()
    first_post = wait_for_CLASS('_aagw')
    first_post.click()
    sleep_random()
    total_comments = 0
    while total_comments < place[1]:
        username = get_username()
        if check_user_meets_criteria():
            print('[+] Comentandole a:', username)
            leave_comment(username)
            save_contacted_user(username)
            total_comments += 1
        sleep_random()
        if total_comments != place[1]:
            next_post()

def comment_on_hashtag(hashtag):
    sleep_random()
    place_address = "https://www.instagram.com/explore/tags/{}/".format(hashtag[0])
    DRIVER.get(place_address)
    sleep_random()
    print('----> Comentando en', '#' + hashtag[0], '\n')
    first_post = wait_for_CLASS('_aagw')
    first_post.click()
    sleep_random()
    total_comments = 0
    while total_comments < hashtag[1]:
        username = get_username()
        if check_user_meets_criteria():
            print('[+] Comentandole a:', username)
            leave_comment(username)
            save_contacted_user(username)
            total_comments += 1
        sleep_random()
        if total_comments != hashtag[1]:
            next_post()

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

    if clean_username == '':
        clean_username = user_anchor.text

    return clean_username

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

def user_in_db():
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

def get_user_posts(): #Se deberia modificar
    username = (wait_for_XPATH("//div[@class='xt0psk2']//a")).text
    DRIVER.execute_script("window.open('');")
    DRIVER.switch_to.window(DRIVER.window_handles[1])
    location_address = "https://www.instagram.com/{}".format(username)
    DRIVER.get(location_address)
    sleep_random()
    posts = wait_for_CLASS("_ac2a").text
    sleep_random()
    DRIVER.close()
    DRIVER.switch_to.window(DRIVER.window_handles[0])
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
    global COMMENTS_INDEX
    comment = COMMENTS[COMMENTS_INDEX]
    COMMENTS_INDEX += 1
    if COMMENTS_INDEX > len(COMMENTS) - 1:
        COMMENTS_INDEX = 0
    return comment
        
def save_contacted_user(username):
    print("[+] Usuario guardado en la base de datos\n")

def next_post():
    svg_elements = DRIVER.find_elements(By.TAG_NAME, "svg")
    for svg in svg_elements:
        if svg.get_attribute('aria-label') == 'Next':
            svg.click()
            break

def send_messages():
    if len(LOCATIONS) != 0:
        for location in LOCATIONS:
            if location[3] > 0:
                send_message_on_location(location)
    if len(PLACES) != 0:
        for place in PLACES:
            if place[2] > 0:
                send_message_on_place(place)
    if len(HASHTAGS) != 0:
        for hashtag in HASHTAGS:
            if hashtag[2] > 0:
                send_message_on_hashtag(hashtag)

def send_message_on_location(location):
    print('[+] Enviando mensajes en', location[0])

def send_message_on_place(place):
    print('[+] Enviando mensajes en', place[0])

def send_message_on_hashtag(hashtag):
    print('[+] Enviando mensajes en', hashtag[0])

def sleep_random():
    sleep(random.uniform(3, 5))

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

    DRIVER = create_webdriver()
    USER = get_user()
    login_user()
    comment_posts()
    send_messages()
    exit_webdriver()

start_bot()