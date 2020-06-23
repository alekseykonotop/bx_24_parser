# Модуль авторизации в личном аккаунта Битрикса 24


import local_settings as p_set
# p_set - private settings

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pygeckodriver import geckodriver_path


def get_driver_instance():
    """
    Set custom settings to window
    :return: driver instance
    """
    driver = webdriver.Firefox(executable_path=geckodriver_path)
    driver.set_window_position(0, 0)
    driver.set_window_size(2560, 1600)

    return driver


def bx_autorize(url):
    """
    :param url: str, main url to get autorization
    :return: driver instance by Selenium WebDriver
    """

    driver = get_driver_instance()
    wait = WebDriverWait(driver, 20)
    driver.get(url)
    # driver.implicitly_wait(5)
    # Ждем пока не отобразится форма с тегом form
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'form')))

    # Input email
    email_xpath = '//*[@id="login"]'  # XPATH
    login_elem = driver.find_element_by_xpath(email_xpath)
    login_elem.send_keys(p_set.EMAIL)
    login_elem.send_keys(Keys.RETURN)

    driver.implicitly_wait(5)
    next_btm_xpath = '/html/body/div[1]/div[2]/div/div[1]/div/div/div[3]/div/form/div/div[5]/button[1]'
    next_btm = driver.find_element_by_xpath(next_btm_xpath)
    hover = ActionChains(driver).move_to_element(next_btm)  # Для передвижения мышки на елемент
    hover.perform()
    driver.implicitly_wait(1)
    next_btm.click()

    # Input password
    driver.implicitly_wait(20)
    password_xpath = '//*[@id="password"]'
    pass_el = driver.find_element_by_xpath(password_xpath)
    pass_el.send_keys(p_set.PASSWORD)
    pass_el.send_keys(Keys.RETURN)

    attempt = 0
    while attempt < 4:
        attempt += 1

        try:
            print(f"Authorization attempt #{attempt} running.")
            wait.until(EC.url_contains('stream/?current_fieldset=SOCSERV'))
            print("Main page downloaded successfully.")
            return driver
        except TimeoutException:
            print(f"Authorization attempt #{attempt} failed")
            continue

    print(f"Authorization failed")
    driver.quit()
    return None