import re
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from dotenv import load_dotenv
import os
import random

def get_random_value_for_timer(range=False):
  """
  If you pass the range, the range should be a list with two elements: min value and max value
  """
  if range == False:
    return random.choice(random.uniform(1.5, 7))
  else:
    return random.uniform(range[0], range[1])

def removing_chats(driver): 
  try:
      chats = driver.find_elements(By.XPATH, '//*[contains(@class,"msg-overlay-bubble-header msg")]')
      for chat in chats:
          driver.find_element(By.XPATH, '//button[contains(@class,"msg-overlay-bubble-header__control artdeco")]').click()
          time.sleep(get_random_value_for_timer([1.5,2]))
              
  except:
      pass

class LinkedinDriver:

    
    def __init__(self, user, password):
        self.driver = self.__setting_driver()
        self.user = user
        self.password = password
        self.driver.get("https://www.linkedin.com")
        
    def __setting_driver(self, headless=False, docker=False):
        #These lines are for avoid been detected as a bot
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--log-level=3') #To avoid see warnings in the console
    
        if headless & docker:
            chrome_options.add_argument('--no-sandbox') #Added for docker
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-dev-shm-usage') #Added for docker
            driver = webdriver.Chrome(options = chrome_options)
        else:
            driver = webdriver.Chrome(options = chrome_options)
        print("Done. Log in...")


        return driver

    def login(self):
        print(f"Logging into the account {self.user}...")
        #Cliqueamos en el botón de Iniciar Sesión
        WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class,"nav__button-secondary")]'))).click()
        time.sleep(get_random_value_for_timer([1,2]))

        print("Inserting the username...")        
        #Detectamos el casillero de usuario
        username = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name = "session_key"]')))
        #Lo limpiamos
        username.clear()
        time.sleep(get_random_value_for_timer([2,4]))
        
        #Colocamos el usuario ofrecido
        username.send_keys(self.user)
        time.sleep(get_random_value_for_timer([2,3]))

        print("Inserting the password...")
        #Detectamos el casillero con la password
        password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name = "session_password"]')))
        #Lo limpiamos
        password.clear()
        time.sleep(get_random_value_for_timer([1,2]))
        
        #Colocamos el pw ofrecido
        password.send_keys(self.password)
        time.sleep(get_random_value_for_timer([1,2]))
        
        print("Waiting while logging...")
        #Hacemos clic en iniciar sesión para entrar al portal
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-litms-control-urn="login-submit"]'))).click()
        time.sleep(get_random_value_for_timer([4,6]))

    def go_to_follows_page(self):
        self.driver.get("https://www.linkedin.com/mynetwork/network-manager/people-follow/following/")
        time.sleep(get_random_value_for_timer([4,6]))

    def going_into_the_bottom(self):
        msg = self.driver.find_element(By.XPATH, "//div[contains(@class,'scroll__content')]/p").text
        removing_chats(self.driver)
        self.total_cases = int(re.search('[0-9]{1,}', msg).group())
        self.total_scrolls = round(((self.total_cases*20)/100))
        for number in range(0,self.total_scrolls):
            time.sleep(get_random_value_for_timer([0.4,1.6]))
            self.driver.execute_script(f"window.scrollBy(0, {get_random_value_for_timer([300,650])});")
        print("We are in the bottom...")

    def removing_follows(self, percentage=0.7):
        #Percentage represent how much of the total follows we have we want to remove (we start from the bottom, so the older ones)
        limit = self.total_cases * abs(percentage - 1)
        removing_chats(self.driver)
        number = 0
        while True:
            all_buttons = self.driver.find_elements(By.XPATH, '//button[contains(@aria-label,"Haz clic para dejar de seguir a")]')
            if (number % 2 == 0)&(number > 4):
                self.driver.execute_script(f"window.scrollBy(0, -{get_random_value_for_timer([150,250])});")
            time.sleep(get_random_value_for_timer([1,1.6]))
            removing_chats(self.driver)
            all_buttons[-1].click()
            time.sleep(get_random_value_for_timer([1,1.6]))
            self.driver.find_elements(By.XPATH, '//div[contains(@class,"actionbar")]//button[2]')[0].click()
            removing_chats(self.driver)
            time.sleep(get_random_value_for_timer([1,1.6]))
            number += 1
            print(f"We remove the follow number: {number}")
            
            if len(all_buttons) <= limit:
                break

        print("Logging out...")
        self.driver.find_element(By.XPATH, "//span[text()='Yo']//parent::button").click()
        time.sleep(get_random_value_for_timer([0.7,2]))
        self.driver.get("https://www.linkedin.com/m/logout/")
        time.sleep(get_random_value_for_timer([2,4]))   

if __main__ == '__name__':
    bot = LinkedinDriver(user = '', password = '')
    bot.login()
    bot.go_to_follows_page()
    bot.going_into_the_bottom()
    bot.removing_follows()
