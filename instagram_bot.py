from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager

import json
import pyautogui
import datetime
from time import sleep
import os

import tkinter as tk
from tkinter import filedialog

CONTACTED_USERS = []
CURRENT_USER = []
DMS = 3
COMMENTS = 5
DRIVER = None

def create_webdriver():

    # Creacion del webdriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # Saca los warnings no se por que
    #options.add_experimental_option("detach", True) # Previene que el chrome se cierre cuando se terminen las tareas (No recomendado)
    options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe' #Direccion del navegador C:\Program Files\Google\Chrome\Application\chrome.exe
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=service, options=options)

    return driver

def get_website():
    # Ingresar a la pagina solicitada
    DRIVER.get("https://www.instagram.com")

def login_user():
    # Buscar los inputs del form de login
    username_input = wait_for_XPATH('//*[@id="loginForm"]/div/div[1]/div/label/input')
    password_input = wait_for_XPATH('//*[@id="loginForm"]/div/div[2]/div/label/input')

    # Insertar las credenciales en los inputs
    username_input.send_keys(CURRENT_USER[0])
    password_input.send_keys(CURRENT_USER[1])

    # Buscar y clickear el boton de login
    login_button = wait_for_XPATH('//*[@id="loginForm"]/div/div[3]/button')
    login_button.click()

    sleep(3)

    print('\nSe esta utilizando la cuenta de: ', CURRENT_USER[0])

def get_location_page():
    # Acceder a la pagina del lugar
    wait_for_XPATH("//button[contains(text(),'Save Info')]")
    location_address = "https://www.instagram.com/explore/locations/{}/{}/".format(CURRENT_USER[3], CURRENT_USER[2])
    DRIVER.get(location_address)

def click_on_post():
    # Ingresar al primer post
    first_post = wait_for_CLASS('_aagw')
    first_post.click()

def comment_posts():
    i = 0
    while i < COMMENTS:
        current_username = (wait_for_XPATH("//div[@class='xt0psk2']//a")).text
        print('Buscando a', current_username, 'en la base de datos')
        if check_user_in_db(current_username) or check_user_contacted(current_username):
            print('El usuario ya fue contactado anteriormente')
            next_post()
        else:
            print('El usuario no esta registrado, se le enviara un comentario')
            comment_sent = leave_a_comment(current_username)
            if comment_sent == None:
                print('No se puede enviar el comentario')
                next_post()
            else:
                save_owner_username(current_username)
                if i != COMMENTS - 1:
                    next_post()
                i += 1

def next_post():
    svg_elements = DRIVER.find_elements(By.TAG_NAME, "svg")
    for svg in svg_elements:
        if svg.get_attribute('aria-label') == 'Next':
            svg.click()
            break

def leave_a_comment(username):
    try:
        comment_textarea = DRIVER.find_element(By.TAG_NAME, "textarea")
        comment = 'Hey {} I have a proposal for you, could you dm me please?'.format(username)
        comment_textarea.click()
        updated_textarea = DRIVER.find_element(By.TAG_NAME, "textarea")
        updated_textarea.send_keys(comment)
    except:
        return None

    post_button = wait_for_XPATH("//div[contains(text(),'Post')]")
    #post_button.click()
    #sleep(2)
    print("Se realizo un comentario con exito a:", username)

    return comment

def save_owner_username(current_username):
    if current_username not in CONTACTED_USERS:
        CONTACTED_USERS.append(current_username)
    else:
        print('El usuario ya fue contactado anteriormente')
        
def contact_users():
    write_users_on_db()
    visit_profile()

def visit_profile():
    i = 0
    try:
        while i < DMS:
            username = CONTACTED_USERS[i]
            location_address = "https://www.instagram.com/{}".format(username)
            DRIVER.get(location_address)
            if check_user_messaged(username):
                print('Ya se le envio un mensaje a este usuario')
            else:
                message_info = send_message(username)
                message= message_info[0]
                reason= message_info[1]
                if message == None:
                    CONTACTED_USERS.remove(username)
                    register_failed_message(username, reason)
                else:
                    register_message(username, message, CURRENT_USER)
                    print("Mensaje enviado exitosamente a:", username)
                    i = i + 1 
    except:
        return print('No hay mas usuarios para contactar')

def send_message(username):
    message_button = message_button_missing_handler("div.x1i10hfl[role='button']")
    reason = ''
    if message_button == None:
        reason = 'El usuario no puede recibir mensajes'
        print('El usuario no puede recibir mensajes')
        return [None, reason]
    message_button.click()

    sleep(3)

    try:
        not_now_button = DRIVER.find_element(By.XPATH, "//button[text()='Not Now']")
        not_now_button.click()
    except:
        pass
    
    sleep(3)

    try:
        message_textarea = DRIVER.find_element(By.TAG_NAME, "textarea")
        message = 'Hey {}, do you have a minute?'.format(username)
        message_textarea.send_keys(message)
    except NoSuchElementException:
        message = None
        reason = 'El usuario tiene la cuenta privada'
        print('El usuario tiene la cuenta privada')

    #sleep(2)
    #pyautogui.press('enter')
    #sleep(1)

    return [message, reason]

def register_message(user, message, CURRENT_USER):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists("message_register.json"):
        # Abrir el archivo JSON en modo de lectura
        with open("message_register.json", "r") as file:
            message_register = json.load(file)
    else:
        # Si el archivo no existe, crear una lista vacía
        message_register = []

    # Crear un nuevo message_dict y agregarlo a la lista de mensajes
    new_message_dict = {"From": CURRENT_USER, "To": user,"Message": message, "Time": current_time}
    message_register.append(new_message_dict)

    # Escribir el contenido actualizado de vuelta al archivo JSON
    with open("message_register.json", "w") as file:
        json.dump(message_register, file)
   
def exit_webdriver():
    DRIVER.quit()

def get_users():
    with open("users.json", "r") as f:
        data = json.load(f)
    
    users = []

    for user in data['users']:
        username = user["username"]
        password = user["password"]
        location = user["location"]
        location_id = user["location_id"]
        users.append([username, password, location, location_id])

    return users

def write_users_on_db():
    with open('contacted_users.txt', 'a+') as f:
        for contacted_user in CONTACTED_USERS:
            f.write(contacted_user)
            f.write('\n')
        f.close()

def get_explorer():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    return file_path

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

def wait_for_NAME(tag_name):
    while True:
        try:
            element = WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, tag_name)))
            break
        except:
            continue
    return element

def wait_for_CSS(css_selector):
    while True:
        try:
            element = WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            break
        except:
            continue
    return element

def message_button_missing_handler(css_selector):
    try:
        element = WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    except:
        element = None

    return element

def check_user_in_db(username):
    try:
        with open('contacted_users.txt', 'r') as f:
            content = f.read()
            usernames = content.split('\n')
    except:
        print("Archivo no disponible")
        return False

    found = False
    for u in usernames:
        if u == username:
            return True

    return False

def check_user_contacted(username):
    found = False
    for u in CONTACTED_USERS:
        if u == username:
            return True

    return False

def register_failed_message(username, reason):
    with open('failed_message_register.txt', 'a+') as f:
        f.write(username)
        f.write(' - ' + reason)
        f.write('\n')
        f.close()

def check_user_messaged(username):
    # Abrir el archivo JSON en modo de lectura
    with open("message_register.json", "r") as file:
        message_register = json.load(file)

    # Verificar si el usuario se encuentra en algún campo "To"
    for message in message_register:
        if username in message["To"]:
            return True
    return False

def main():

    global DRIVER

    DRIVER = create_webdriver() #Crea el webdriver que se encarga de controlar el navegador
    
    get_website() #Ingresa a https://www.instagram.com
    
    login_user() #Logea al usuario que se va a utilizar

    get_location_page() #Ingresa a la locacion que le corresponde al usuario actual
    
    click_on_post() # Hace un click en el primer post para ingresar a el

    comment_posts() #Deja un comentario en el post en el que esta parado

    contact_users() #Envia un mensaje directo a algunos de los usuarios a los que se le realizo un comentario en una publicacion

    exit_webdriver() #Finaliza el webdriver


def start_bot():
    if DMS >= COMMENTS:
        return -1
    
    users = get_users() #Obtiene una lista de los usuarios que van a utilizarse
    #explorer = get_explorer()

    for user in users:
        global CURRENT_USER
        CURRENT_USER = user
        global CONTACTED_USERS 
        CONTACTED_USERS = []
        main()

start_bot()