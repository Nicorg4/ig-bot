from time import sleep
from datetime import datetime, timedelta
from collections import deque
import json
import pyautogui
import os
import re
import random
import pyperclip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import spacy
from colorama import Fore, Back, Style

DRIVER = None
USER = None
IG_USER = None
IG_PASS = None
COMMENTS_INDEX = 0
MESSAGES_INDEX = 0
MIN_POSTS = 0
TOTAL_COMMENTS = 0
TOTAL_DMS = 0
CURRENT_CYCLE = None
TOO_OLD_COUNTER = 0
DM_SPAM_PROTECTION_COUNTER = 0
SPAM_MAX_WINDOW = 10
HEADLESS = False
NLP_EN = spacy.load('en_core_web_sm')
NLP_ES = spacy.load('es_core_news_sm')

class Cycle:
    def __init__(self, destinations):
        self.destinations = destinations

class Destination:
    def __init__(self, location_name, location_id, place_name, hashtag_name, number_of_comments, number_of_messages, type):
        self.location_name = location_name
        self.location_id = location_id
        self.place_name = place_name
        self.hashtag_name = hashtag_name
        self.number_of_comments = number_of_comments
        self.number_of_messages = number_of_messages
        self.type = type

def create_new_cycle(destinations):
    cycle = Cycle(destinations)
    return cycle

def create_webdriver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True) # Previene que el chrome se cierre cuando se terminen las tareas (No recomendado)
    options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    options.add_argument("--incognito")
    if HEADLESS:
        options.add_argument('--headless')  # Iniciar en modo headless
    options.add_argument('--window-size=1920x1080')  # Tamaño de ventana
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.instagram.com")

    return driver

def exit_webdriver():
    DRIVER.quit()

def get_admin_user():
    return [IG_USER, IG_PASS]

def login_user():
    username_input = wait_for_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
    password_input = wait_for_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')

    username_input.send_keys(USER[0])
    password_input.send_keys(USER[1])

    sleep_random()

    login_button = wait_for_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
    login_button.click()

    print(Fore.MAGENTA + 'Se esta utilizando la cuenta de:', USER[0], '\n')

def contact_users():
    for destination in CURRENT_CYCLE.destinations:
        if destination.type == "location":
            comment_on_location(destination)
            send_messages(destination)
        if destination.type == "place":
            comment_on_place(destination)
            send_messages(destination)
        if destination.type == "hashtag":
            comment_on_hashtag(destination)
            send_messages(destination)

def comment_on_location(location):
    comment_setup("https://www.instagram.com/explore/locations/{}/{}/".format(location.location_id, location.location_name), location.location_name)
    total_comments = 0
    while total_comments < location.number_of_comments:
        total_comments += commenting_process()
        if old_counter_too_big():
            global TOO_OLD_COUNTER
            TOO_OLD_COUNTER = 0
            print(Fore.RED + "[-] Los posts son demasiado viejos \n")
            break
        next_post()

def comment_on_place(place):
    comment_setup("https://www.instagram.com/{}/tagged/".format(place.place_name), place.place_name)
    total_comments = 0
    while total_comments < place.number_of_comments:
        total_comments += commenting_process()
        if old_counter_too_big():
            global TOO_OLD_COUNTER
            TOO_OLD_COUNTER = 0
            print(Fore.RED + "[-] Los posts son demasiado viejos \n")
            break
        next_post()

def comment_on_hashtag(hashtag):
    comment_setup("https://www.instagram.com/explore/tags/{}/".format(hashtag.hashtag_name), hashtag.hashtag_name)
    total_comments = 0
    while total_comments < hashtag.number_of_comments:
        total_comments += commenting_process()
        if old_counter_too_big():
            global TOO_OLD_COUNTER
            TOO_OLD_COUNTER = 0
            print(Fore.RED + "[-] Los posts son demasiado viejos \n")
            break
        next_post()

def comment_setup(adress, name):
    try:
        WebDriverWait(DRIVER, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "_aa56")))
    except:
        pass
    DRIVER.get(adress)
    print(Fore.MAGENTA + '-------------------------------------\n')
    print(Fore.MAGENTA + 'Comentando en', '#' + name, '\n')
    print(Fore.MAGENTA + '-------------------------------------\n')
    sleep_random()
    first_post = wait_for_element(By.CLASS_NAME, '_aagw')
    first_post.click()
    sleep_random()

def commenting_process():
    successfull_comment = 0
    try:
        username = get_username()
    except:
        return successfull_comment
    
    print(Fore.GREEN + '[+] Comentandole a', username[1])
    if check_user_meets_criteria(username[1], username[0]):
        if leave_comment(username[0]):
            save_contacted_user(username[1], 'Comment')
            global TOTAL_COMMENTS
            TOTAL_COMMENTS += 1
            successfull_comment = 1
    sleep_random()
    return successfull_comment

def get_username():
    user_anchor = wait_for_element(By.XPATH, "//div[@class='xt0psk2']//a")
    username_from_anchor = user_anchor.text
    actions = ActionChains(DRIVER)
    actions.move_to_element(user_anchor).perform()
    sleep_random()
    try:
        username = wait_for_element(By.XPATH, "//div[@class='xmix8c7 x1gslohp x1rva8in']//span").text
    except:
        username = username_from_anchor

    first_name = username.split()[0]
    clean_username = re.sub(r'[^a-zA-Z]+', '', first_name).capitalize()

    if not is_name(clean_username):
        clean_username = (user_anchor.text).capitalize()
    
    return [clean_username, username_from_anchor]

def is_name(username):
    doc_en = NLP_EN(username.capitalize())
    doc_es = NLP_ES(username.capitalize())

    return any(token.ent_type_ == "PERSON" for token in doc_en) or any(token.ent_type_ == "PER" for token in doc_es)

def check_user_meets_criteria(username, name):
    if not commenting_available():
        print(Fore.RED + '[-] El usuario no puede recibir comentarios\n')
        return False
    if user_in_db(username):
        print(Fore.RED + '[-] El usuario ya esta en la base de datos\n')
        return False
    if not post_is_new():
        print(Fore.RED + '[-] El post es demasiado antiguo\n')
        increase_old_counter()
        return False
    if not check_user_uploads_enough():
        print(Fore.RED + '[-] El usuario no tiene los posts suficientes\n')
        return False
    # if user_is_brand(username, name):
    #     print('[-] El usuario es una empresa\n')
    #     return False
    return True

def increase_old_counter():
    global TOO_OLD_COUNTER
    TOO_OLD_COUNTER += 1

def old_counter_too_big():
    if TOO_OLD_COUNTER >= 5:
        return True

def user_in_db(username):
    users = get_users_in_db()
    for user in users:
        if user['Username'] == username:
            return True
    return False

def commenting_available():
    try:
        short_wait_for_element(By.XPATH, "//span[text()='Comments on this post have been limited.']")
    except:
        try:
            short_wait_for_element(By.TAG_NAME, "textarea")
            return True
        except:
            return False
    return False
 
def check_user_uploads_enough(): 
    number_of_posts = get_user_posts()

    if number_of_posts > MIN_POSTS:
        return True
    return False

def post_is_new():
    try:
        post_date = short_wait_for_element(By.CLASS_NAME, '_aaqe').get_attribute("datetime")
        date_now = datetime.now()
        clean_post_date = datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        a_week_from_now = date_now - timedelta(days=7)
        return clean_post_date >= a_week_from_now
    except:
        return False

def user_is_brand(username, name):
    if is_name(name):
        return False
    else:
        main_window_handle = DRIVER.current_window_handle
        location_address = "https://www.instagram.com/{}".format(username)
        sleep_random()
        DRIVER.execute_script("window.open(arguments[0]);", location_address)
        new_window_handle = DRIVER.window_handles[-1]
        DRIVER.switch_to.window(new_window_handle)
        try:
            sleep_random()
            DRIVER.find_element(By.XPATH, '//div[@dir="auto"]')
            DRIVER.close()
            DRIVER.switch_to.window(main_window_handle)
            return True
        except:
            DRIVER.close()
            DRIVER.switch_to.window(main_window_handle)
            return False

def get_user_posts():
    try:
        user_anchor = short_wait_for_element(By.XPATH, "//div[@class='xt0psk2']//a")
        actions = ActionChains(DRIVER)
        actions.move_to_element(user_anchor).perform()
        sleep_random()
        posts = short_wait_for_element(By.XPATH, "//div[contains(@class, 'x6s0dn4') and contains(@class, 'xrvj5dj')]/div/div/span/span").text

        if 'K' in posts:
            posts = posts.replace('K', '')
            posts = float(posts) * 1000
            posts = int(posts)
        elif ',' in posts:
            posts = posts.replace(',', '')
            posts = int(posts)
    except:
        return 0
    
    return int(posts)

def leave_comment(username):
    try:
        comment_textarea = wait_for_element(By.TAG_NAME, "textarea")
        comment_textarea.click()
        updated_textarea = wait_for_element(By.TAG_NAME, "textarea")
        comment = pick_comment().format(username)

        sleep_random()

        for s in comment:
            if s == ',':
                emoji = "🙋🏽‍♂️"
                pyperclip.copy(emoji)
                updated_textarea.send_keys(Keys.CONTROL, 'v')
                sleep(random.uniform(0.005, 0.02))
            updated_textarea.send_keys(s)
            sleep(random.uniform(0.005, 0.02))

        sleep_random()

        #updated_textarea.send_keys(Keys.RETURN)  # o wait_for_element(By.XPATH, "//div[contains(text(),'Post')]").click()

        return True
    except:
        print(Fore.RED + "[-] El usuario bloqueo los comentarios \n")
        return False

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
        
def save_contacted_user(username, method):
    user = [{"Username": username, "Method": method}]
    existing_users = get_users_in_db()
    existing_users.extend(user)

    with open("contacted_users.json", 'w') as file:
        json.dump(existing_users, file)

    print(Fore.GREEN + "[+]", username,"guardado en la base de datos\n")

def get_users_in_db():
    try:
        with open('contacted_users.json', 'r') as file:
            usuarios = json.load(file)
    except FileNotFoundError:
        usuarios = []
    return usuarios

def next_post():
    while True:
        try:
            svg_elements = DRIVER.find_elements(By.TAG_NAME, "svg")
            for svg in svg_elements:
                if svg.get_attribute('aria-label') == 'Next':
                    svg.click()
                    break
            break
        except:
            continue

def send_messages(destination):
    global DM_SPAM_PROTECTION_COUNTER
    global SPAM_MAX_WINDOW
    number_of_messages = 0
    main_window_handle = DRIVER.current_window_handle
    while number_of_messages < destination.number_of_messages:
        if DM_SPAM_PROTECTION_COUNTER < SPAM_MAX_WINDOW:
            username = get_username()
            print('[+] Enviandole mensaje a', username[1])
            if check_user_meets_criteria_dm(username[1]):
                visit_profile(username[1])
                sleep_random()
                if send_message(username):
                    number_of_messages += 1
                DRIVER.close()
                DRIVER.switch_to.window(main_window_handle)
                sleep_random()
        else:
            print(Fore.CYAN + "[-] Se activo el protocolo de prevencion de deteccion de spam\n")
            DM_SPAM_PROTECTION_COUNTER = 0
            SPAM_MAX_WINDOW = 5
            break
        next_post()

def check_user_meets_criteria_dm(username):
    if user_in_db(username):
        print(Fore.YELLOW + '[-] El usuario ya esta en la base de datos\n')
        return False
    return True

def visit_profile(username):
    location_address = "https://www.instagram.com/{}".format(username)
    DRIVER.execute_script("window.open(arguments[0]);", location_address)
    new_window_handle = DRIVER.window_handles[-1]
    DRIVER.switch_to.window(new_window_handle)

def send_message(username):
    global DM_SPAM_PROTECTION_COUNTER
    global TOTAL_DMS
    global SPAM_MAX_WINDOW
    
    try:
        message_button = wait_for_element(By.CSS_SELECTOR, "div.x1i10hfl[role='button']")
        message_button.click()
        sleep_random()
    except:
        print(Fore.RED + "[-] El usuario", username[1], 'no puede recibir mensajes \n')
        return False

    try:
        not_now_button = WebDriverWait(DRIVER, 2).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Not Now']")))
        not_now_button.click()
    except:
        pass
    
    try:
        message_textarea = WebDriverWait(DRIVER, 5).until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
    except TimeoutException:
        try:
            message_textarea = WebDriverWait(DRIVER, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.xat24cr.xdj266r')))
        except TimeoutException:
            DM_SPAM_PROTECTION_COUNTER += 1
            print(Fore.RED + '[-] El usuario', username[1], 'tiene la cuenta privada', '\n')
            return False

    sleep_random()

    message = pick_message().format(username[0])
    for s in message:
        if s == ',':
            emoji = "🙋🏽‍♂️"
            pyperclip.copy(emoji)
            message_textarea.send_keys(Keys.CONTROL, 'v')
            sleep(random.uniform(0.005, 0.02))
        message_textarea.send_keys(s)
        sleep(random.uniform(0.005, 0.02))

    sleep_random()
    #message_textarea.send_keys(Keys.RETURN)
    save_contacted_user(username[1], 'DM')

    TOTAL_DMS += 1
    DM_SPAM_PROTECTION_COUNTER = 0
    SPAM_MAX_WINDOW = 10

    return True

def pick_message():
    with open("data.json") as file:
        data = json.load(file)
    messages = [message["message"] for message in data["messages"]]
    global MESSAGES_INDEX
    message = messages[MESSAGES_INDEX]
    MESSAGES_INDEX += 1
    if MESSAGES_INDEX > len(messages) - 1:
        MESSAGES_INDEX = 0
    return message

def return_home():
    DRIVER.get("https://www.instagram.com")

def sleep_random():
    sleep(random.uniform(1, 3))

def wait_for_element(method, tag):
    element = WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((method, tag)))
    return element

def short_wait_for_element(method, tag):
    element = WebDriverWait(DRIVER, 2).until(EC.presence_of_element_located((method, tag)))
    return element
   
def bot_setup(id):
    global DRIVER
    global USER 

    if id:
        while True:
            try:
                DRIVER = create_webdriver()
                USER = get_admin_user()
                login_user()
                break
            except:
                exit_webdriver()
                continue
    contact_users()
    print(Fore.MAGENTA + "\n#### Ciclo finalizado ####\n")
    return_home()

def start_bot(destinations, id):
    global CURRENT_CYCLE

    cycle = create_new_cycle(destinations)
    CURRENT_CYCLE = cycle
    print(Fore.MAGENTA + "\n#### Iniciando ciclo nuevo ####\n")
    bot_setup(id)