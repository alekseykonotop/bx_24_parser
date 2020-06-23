# Функции перехода по ссылкам и ожидания успешного перехода

import local_settings as p_set

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pygeckodriver import geckodriver_path


def is_transition_success(driver, subpage):
    """
    Функция задержки потока выполнения до момента
    получение положительной проверки полного соответствия url и link
    :param driver: instance of WebDriver
    :param subpage: subpage name, string
    :return: Boolean type
    """

    wait = WebDriverWait(driver, 15)

    try:
        wait.until(EC.url_contains(subpage))
        return True
    except TimeoutException:
        print(f"URL doesn't match the subpage: {subpage}")
        return False


def move_to_link(driver, url=''):
    """

    :param driver: instance of selenium.webdriver
    :param url: page url, string
    :param sub_page_name: subpage name, string
    :return: driver
    """
    if not url:
        print(f"You must enter a transition url.")
        return

    driver.get(url)


