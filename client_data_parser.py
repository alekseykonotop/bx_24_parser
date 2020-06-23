from transitions import move_to_link, is_transition_success
from link_parser import get_data_from_page
import pandas as pd
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException


def write_to_csv(path, data):
    """

    :param path: path to file
    :param data: the list of dicts
    :return: Boolean - result status
    """

    df = pd.DataFrame(data=data)
    df.to_csv(path, encoding='utf-8')
    print(f"CSV file recording completed")


def get_data_dict(data):
    """"
    :param data: multy-string
    :return: structured dict of personal data
    """
    tmp_dict = dict.fromkeys(['fullname', 'name', 'phone', 'email',
                              'loyalty', 'birthday', 'contr_num', 'contr_date',
                              'adress', 'ex_phone', 'ex_email', 'ex_name',
                              'ex_status'])
    for row in data.split('\n'):
        if 'Номер договора:' in row:
            contr_num = row.split(':')[-1].strip()
            tmp_dict['contr_num'] = contr_num

        if 'Дата подписания:' in row:
            contr_date = row.split(':')[-1].strip()
            tmp_dict['contr_date'] = contr_date

        if 'ФИО:' in row:
            fullname = row.split(':')[-1].strip()
            name = ' '.join(fullname.split(' ')[1:])
            tmp_dict['fullname'] = fullname
            tmp_dict['name'] = name

        if 'Дата рождения:' in row:
            birthday = row.split(':')[-1].strip()
            tmp_dict['birthday'] = birthday

        if 'тел. моб.:' in row.lower():
            phone = row.split(':')[-1].strip().replace(' ', '') \
                .replace('+', '') \
                .replace('(', '') \
                .replace(')', '') \
                .replace('-', '')

            tmp_dict['phone'] = phone

        if 'эл. почта' in row.lower():
            if '@' in row:
                email = row.split(':')[-1].strip()
            else:
                email = 'unknown'
            tmp_dict['email'] = email

        if 'ЛОЯЛЬНОСТЬ:' in row:
            loyalty = row.split(':')[-1].strip()
            tmp_dict['loyalty'] = loyalty

        if 'aдрес регистрации:' in row.lower():
            adress = row.split(':')[-1].strip()
            tmp_dict['adress'] = adress

        if 'доп. контакт 1:' in row.lower():
            if ': нет' not in row:
                ex_data = row.split(':')[-1].strip()
                if '|' in ex_data:
                    split_data = ex_data.split(' | ')
                    if len(split_data) == 3:
                        # So we have ex_phone, ex_name, ex_status
                        ex_phone = split_data[0].replace(' ', '') \
                                                .replace('+', '') \
                                                .replace('(', '') \
                                                .replace(')', '') \
                                                .replace('-', '')
                        ex_name = split_data[1]
                        ex_status = split_data[2]
                        tmp_dict['ex_phone_1'] = ex_phone
                        tmp_dict['ex_name_1'] = ex_name
                        tmp_dict['ex_status_1'] = ex_status
                    if len(split_data) == 2:
                        # So we have ex_phone, ex_name
                        ex_phone = split_data[0].replace(' ', '') \
                                                .replace('+', '') \
                                                .replace('(', '') \
                                                .replace(')', '')
                        ex_name = split_data[1]
                        tmp_dict['ex_phone_1'] = ex_phone
                        tmp_dict['ex_name_1'] = ex_name

        if 'доп. контакт 2:' in row.lower():
            if ': нет' not in row:
                ex_data = row.split(':')[-1].strip()
                if '|' in ex_data:
                    split_data = ex_data.split(' | ')
                    if len(split_data) == 3:
                        # So we have ex_phone, ex_name, ex_status
                        ex_phone = split_data[0].replace(' ', '') \
                                                .replace('+', '') \
                                                .replace('(', '') \
                                                .replace(')', '') \
                                                .replace('-', '')
                        ex_name = split_data[1]
                        ex_status = split_data[2]
                        tmp_dict['ex_phone_2'] = ex_phone
                        tmp_dict['ex_name_2'] = ex_name
                        tmp_dict['ex_status_2'] = ex_status
                    if len(split_data) == 2:
                        # So we have ex_phone, ex_name
                        ex_phone = split_data[0].replace(' ', '') \
                                                .replace('+', '') \
                                                .replace('(', '') \
                                                .replace(')', '')
                        ex_name = split_data[1]
                        tmp_dict['ex_phone_2'] = ex_phone
                        tmp_dict['ex_name_2'] = ex_name

        if 'доп. эл. почта:' in row.lower():
            if '@' in row:
                email = row.split(':')[-1].strip()
            else:
                email = 'unknown'
            tmp_dict['ex_email'] = email

    return tmp_dict






def write_to_data_file(data):
    """
    Main function to write personal data
    if txt-file
    """
    # preprocessing
    if 'main_table' in data:
        data = data.replace('main_table\n', '')
    data += '\n===end_chunk===\n\n'

    with open('July/personal_data.txt', 'a', encoding='utf-8') as f:
        f.write(data)


def parse_clients_data(driver, urls=None):
    """
    Parse personal data from all links
    :param driver: instance WebDriver
    :param urls: list of urls
    :param path: string, path to file
    :return: status code ( 200 finish successfully, 400 failed )
    """
    if not urls:
        print(f"URLs must be required")
        return

    total_data_list = []

    # for url in urls:
    for url in urls:
        # Make a transition to url
        move_to_link(driver, url)

        # separate a subpage
        subpage = '/'.join(url.split('/')[-3:-1])
        if is_transition_success(driver, subpage=subpage):
            dirty_data = get_data_from_page(driver)

            # Временно для отладки - затем удалить
            # write_to_data_file(dirty_data)  # Все работает

            personal_data_dict = get_data_dict(dirty_data)
            if not personal_data_dict:
                print(f"EMPTY personal_data_dict url: {url}")
            else:
                total_data_list.append(personal_data_dict)

    return total_data_list
