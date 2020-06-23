
from bx_authorization import bx_autorize
from transitions import move_to_link, is_transition_success
from link_parser import collect_links, write_to_txt_file
from client_data_parser import parse_clients_data, write_to_csv
import local_settings as p_set
import os
from datetime import datetime


def main():
    start = datetime.now()
    driver = bx_autorize(p_set.LOG_URL)

    if driver:
        print(f"Авторизация прошла успешно")
    else:
        print(f"Проблемы авторизации\nЗавершение программы")
        quit()
    print(f"Current url= {driver.current_url}")
    # Move to groups
    subpage = 'workgroups'
    work_page_url = f"{p_set.URL}/{subpage}"
    move_to_link(driver, work_page_url)

    if is_transition_success(driver, subpage=subpage):
        print(f"Successful transition to working groups.")

        print(f"Current url= {driver.current_url}")

        # Has be sure that the filter has value of "loyal customers"

        # Collect all client's groups links
        clients_urls = collect_links(driver)

        path_to_write = 'July/workgroups_links.txt'
        write_to_txt_file(path_to_write, data=clients_urls)

    else:
        print(f"Unsuccessful transition to working groups.")

    # Now start client data parse
    if os.access(path_to_write, os.R_OK):
        cleared_customer_data = parse_clients_data(driver, urls=clients_urls)  # a list of dicts of personal data
        write_to_csv('July/cleared_customer_data.csv', cleared_customer_data)

    end = datetime.now()
    print('END PROGRAM!')
    print(f"Total time: {end - start} minutes")


if __name__ == "__main__":
    main()

