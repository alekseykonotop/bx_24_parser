# Parse all links on work groups

import local_settings as p_set
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pygeckodriver import geckodriver_path

from transitions import move_to_link, is_transition_success
import local_settings as p_set


def write_to_txt_file(file_name="data.txt", data=None):
    """
    Запишем данные в файл
    :param data: list of unique links
    :param file_name: str
    :return: None
    """
    if not data:
        print(f"[ write_to_file ]: Data is empty")
        return

    # Check the existence of path
    ret = os.access(file_name, os.W_OK)
    if not ret:
        os.mkdir(file_name.split('/')[0])

    with open(file_name, 'w', encoding='utf-8') as f:
        for link in data:
            f.write(f"{link}\n")


def write_problem_to_log(url):
    url = str(url)
    with open('problem_logs.txt', 'a', encoding='utf-8') as f:
        f.write(f"{url}\n\n")


def collect_links(driver, attribute_type='', attribute_value=''):
    """
    Собирает все ссылки с указанным атрибутом и значением
    данного атрибута с учетом пагинации.
    :param driver: instance of WebDriver
    :param attribute_type: string
    :param attribute_value: string
    :return: list of urls
    """
    all_urls = []

    # Determine the number of pages
    nav_pages_div = driver.find_element_by_class_name('navigation-pages')
    num_pages = int(nav_pages_div.find_elements_by_class_name('navigation-page-numb')[-1].text)
    # print(f"Count page= {num_pages}")

    for page_num in range(1, num_pages + 1):
        url_to_transition = f"{p_set.URL}/workgroups/?sonet_user_groups=page-{page_num}"
        move_to_link(driver, url_to_transition)

        if is_transition_success(driver, subpage=url_to_transition):
            # print(f"Successful transition to page {page_num}.")
            sonet_block = driver.find_element_by_class_name('sonet-groups-group-block-shift')

            # Find all group links
            group_elems = sonet_block.find_elements_by_class_name("sonet-groups-group-link")
            # print(f"Page {page_num}\nFound {len(group_elems)} urls\n")

            for elem in group_elems:
                elem_url = elem.get_attribute('href')
                if elem_url not in [p_set.TEST_GROUP_URL, p_set.IGNORE_URL_1, p_set.IGNORE_URL_2]:
                    all_urls.append(elem_url)
        else:
            print(f"Unsuccessful transition to page {page_num}.")

    print(f"We successfully collected {len(all_urls)} urls.")

    return all_urls



def get_data_from_page(driver):
    """
    Заполняем словарь данными из самого первого поста на странице
    :param driver: WebDriver instance
    :return: dict
    """

    try:
        element = driver.find_element_by_xpath('//*[contains(@id, "blog_post_more_") and @class="feed-post-text-more"]')  # рабочий xpath
        driver.execute_script('arguments[0].scrollIntoView(true);', element)  # Прокрутка к целевому элементу - работает
        driver.implicitly_wait(15)
        element.click()
    except ElementNotInteractableException as eie:
        print(f"Raise exception {eie}")
        write_problem_to_log(driver.current_url)
    except NoSuchElementException as ee:
        print(f"Raise exception {ee}")
        write_problem_to_log(driver.current_url)
    else:
        table_elem = driver.find_element_by_xpath('//*[contains(@id, "feed-post-contentview-BLOG_POST-")]')
        # print(f"{table_elem.text}")
        return table_elem.text

    return None




