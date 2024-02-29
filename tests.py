from instagram_bot import *
import instagram_bot
import traceback

def test01():
    instagram_bot.IG_USER = 'pipslab.team@gmail.com'
    instagram_bot.IG_PASS = 'pipslabteam2023'
    instagram_bot.MIN_POSTS = 10
    instagram_bot.HEADLESS = True

    destinations = []
    destinations2 = []
    destinations3 = []

    start_time = datetime.now()

    destination1 = Destination('', '', 'faenamiamibeach', '', 20, 5, 'place')
    destination2 = Destination('', '', 'fsmadrid', '', 20, 5, 'place')
    destinations.append(destination1)
    destinations.append(destination2)
    start_bot(destinations, True)
    sleep(3600)

    destination3 = Destination('magic-hour-rooftop-bar-lounge', '187178655154203', '', '', 20, 5, 'location')
    destination4 = Destination('', '', '1hotel.southbeach', '', 20, 5, 'place')
    destinations2.append(destination3)
    destinations2.append(destination4)
    create_new_cycle(destinations2)
    start_bot(destinations2, False)
    sleep(3600)

    destination5 = Destination('', '', 'fontainebleau', '', 20, 5, 'place')
    destinations3.append(destination5)
    create_new_cycle(destinations3)
    start_bot(destinations3, False)

    end_time = datetime.now()
    
    print('\nDuracion de la ejecucion:', end_time - start_time)
    print("Total de comentarios realizados:", instagram_bot.TOTAL_COMMENTS, "\nTotal de mensajes enviados:", instagram_bot.TOTAL_DMS)

def test02():
    instagram_bot.IG_USER = 'pipsdevs@gmail.com'
    instagram_bot.IG_PASS = 'pipslabteam2023'
    instagram_bot.MIN_POSTS = 10
    instagram_bot.HEADLESS = True

    destinations = []
    destinations2 = []

    start_time = datetime.now()

    destination1 = Destination('', '', 'faenamiamibeach', '', 40, 10, 'place')
    destinations.append(destination1)
    start_bot(destinations, True)
    sleep(20)

    destination3 = Destination('nobu-malibu', '284736021647673', '', '', 3, 1, 'location')
    destinations2.append(destination3)
    start_bot(destinations2, False)

    end_time = datetime.now()
    
    print('\nDuracion de la ejecucion:', end_time - start_time)
    print("Total de comentarios realizados:", instagram_bot.TOTAL_COMMENTS, "\nTotal de mensajes enviados:", instagram_bot.TOTAL_DMS)

def test03():
    instagram_bot.IG_USER = 'pipslab.team@gmail.com'
    instagram_bot.IG_PASS = 'pipslabteam2023'
    instagram_bot.MIN_POSTS = 10
    instagram_bot.HEADLESS = True

    try:
        instagram_bot.DRIVER = create_webdriver()
        instagram_bot.USER = get_admin_user()
        sleep_random()
        login_user()
        sleep_random()
        instagram_bot.DRIVER.get("https://www.instagram.com/direct/t/17844837926960425/")
        sleep_random()
        message_textarea = wait_for_element(By.CSS_SELECTOR, 'p.xat24cr.xdj266r')
        message = "Mensaje"
        message_textarea.send_keys(message)
        sleep_random()
        message_textarea.send_keys(Keys.RETURN)
    except Exception as e:
        print("Error:", e)


def finalTest():
    instagram_bot.IG_USER = 'Paiorod'
    instagram_bot.IG_PASS = 'amordisfrute1991'
    instagram_bot.MIN_POSTS = 10
    instagram_bot.HEADLESS = False

    destinations = []
    destinations2 = []
    destinations3 = []
    destinations4 = []
    destinations5 = []
    destinations6 = []
    destinations7 = []
    destinations8 = []

    start_time = datetime.now()

    destination1 = Destination('', '', 'summit', '', 35, 10, 'place')
    destinations.append(destination1)
    start_bot(destinations, True)
    sleep(3600)

    destination3 = Destination('beverly-hills', '149983395553010', '', '', 35, 5, 'location')
    destinations2.append(destination3)
    create_new_cycle(destinations2)
    start_bot(destinations2, False)
    sleep(3600)

    destination3 = Destination('malibu-california', '213873866', '', '', 35, 10, 'location')
    destinations3.append(destination3)
    start_bot(destinations3, False)
    sleep(3600)

    destination4 = Destination('', '', 'sexyfishlondon', '', 35, 10, 'place')
    destinations4.append(destination4)
    start_bot(destinations4, False)
    sleep(3600)

    destination5 = Destination('hollywood-hills', '212998729', '', '', 35, 10, 'location')
    destinations5.append(destination5)
    start_bot(destinations5, False)
    sleep(3600)

    destination6 = Destination('', '', 'bellagio', '', 35, 10, 'place')
    destinations6.append(destination6)
    start_bot(destinations6, False)
    sleep(3600)

    destination7 = Destination('', '', 'venetianvegas', '', 35, 10, 'place')
    destinations7.append(destination7)
    start_bot(destinations7, False)
    sleep(3600)

    destination8 = Destination('', '', 'eatstk', '', 35, 10, 'place')
    destinations8.append(destination8)
    start_bot(destinations8, False)

    end_time = datetime.now()
    
    print('\nDuracion de la ejecucion:', end_time - start_time)
    print("Total de comentarios realizados:", instagram_bot.TOTAL_COMMENTS, "\nTotal de mensajes enviados:", instagram_bot.TOTAL_DMS)

try:
    finalTest()
except NoSuchElementException:
    print("\n\n[X] Se produjo una error en la ejecucion, se debe volver a iniciar el bot")
except Exception as e:
    print("[X] Ocurrio un error inesperado:\n", e)