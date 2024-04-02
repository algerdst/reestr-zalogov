import json
import time
from time import sleep
import random

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from get_driver import get_driver



def input_func(browser, current_index):
    input = browser.find_element(By.CSS_SELECTOR, 'input.form-control')
    input.clear()
    input.send_keys(cads[current_index])
    sleep(random.uniform(2, 3))

    find = browser.find_element(By.ID, 'find-btn')
    find.click()

def change_ip(browser):
    response = requests.get('https://mobiproxy.net/proxy/update/019ca089e1f35683aa8f7c0062c943e9/')
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        h2 = soup.find('h2').text
        sleep_time = int(h2.split('осталось')[1].replace(' ', '').replace('сек.', ''))
        print(f'Меняем ip через {sleep_time}')
        time.sleep(sleep_time)
        requests.get('https://mobiproxy.net/proxy/update/019ca089e1f35683aa8f7c0062c943e9/')
    except:
        back = browser.find_element(By.ID, 'back-btn')
        back.click()
        print(f'Меняем ip ')

#запись всех номеров кад в список
with open('cad.txt', 'r', encoding='utf-8') as file:
    cads=[i.replace('\n','') for i in file]

#беру словарь json и вписываю последний индекс из списка cad в ключ max_index
with open('indexes.json', 'r', encoding='utf-8') as file:
    indexes_dict = json.load(file)
    indexes_dict['max_index']=len(cads)-1

# записываю новый словарь в json
with open('indexes.json', 'w', encoding='utf-8') as file:
    json.dump(indexes_dict, file, indent=4, ensure_ascii=False)

def main(current_index):
    with get_driver() as browser:
        browser.get('https://reestr-zalogov.ru/search/index')
        current_window=browser.window_handles[0]
        while True:
            input_func(browser, current_index=current_index) #Вводим запрос в строку
            sleep(10)
            try: #Если запрос запрещен, входим в этот блок и пробуем снова
                browser.find_element(By.CLASS_NAME, 'search-error-label')
                print('Запрос запрещен')
                back = browser.find_element(By.ID, 'back-btn')
                back.click()
                input_func(browser, current_index=current_index)
                sleep(10)
                try:#Если запрос запрещен, входим в этот блок и пробуем снова
                    browser.find_element(By.CLASS_NAME, 'search-error-label')
                    print('Запрос запрещен')
                    back = browser.find_element(By.ID, 'back-btn')
                    back.click()
                    input_func(browser, current_index=current_index)
                    sleep(10)
                    try:#Если запрос запрещен, меняем ip
                        browser.find_element(By.CLASS_NAME, 'search-error-label')
                        print('Запрос запрещен')
                        back = browser.find_element(By.ID, 'back-btn')
                        back.click()
                        change_ip(browser)
                        continue
                    except:
                        print()
                except:
                    print()
            except:
                print()


            download_pdf = browser.find_element(By.CLASS_NAME, 'notification')
            download_pdf.click()
            sleep(random.uniform(4, 5))
            try:#Если выскочила ошибка 403, попадаем в этот блок, закрываем окно с ошибкой, пробуем скачать снова
                browser.switch_to.window(browser.window_handles[1])
                browser.find_element(By.CLASS_NAME, 'error-text-panel')
                browser.close()
                browser.switch_to.window(current_window)
                download_pdf.click()
                time.sleep(5)
                try:#Если снова выскочила ошибка 403, попадаем в этот блок, меняем ip
                    browser.switch_to.window(browser.window_handles[1])
                    browser.find_element(By.CLASS_NAME, 'error-text-panel')
                    browser.close()
                    browser.switch_to.window(current_window)
                    change_ip(browser)
                    continue
                except:
                    time.sleep(5)
                    print(cads[current_index] + " " + "скачан")
                    current_index+=1
                    with open('indexes.json', 'w', encoding='utf-8') as file:
                        json.dump({
                            "current_index": current_index,
                            "max_index": max_index
                        }, file, indent=4, ensure_ascii=False)
                    back = browser.find_element(By.ID, 'back-btn')
                    back.click()
                    continue
            except:
                time.sleep(5)
                back = browser.find_element(By.ID, 'back-btn')
                back.click()
                print(cads[current_index]+" "+"скачан")
                current_index+=1
                with open('indexes.json', 'w', encoding='utf-8') as file:
                    json.dump({
                        "current_index": current_index,
                        "max_index": max_index
                    }, file, indent=4, ensure_ascii=False)
                continue


while True:
    with open('indexes.json', 'r', encoding='utf-8') as file:
        indexes_dict = json.load(file)
        max_index = indexes_dict['max_index']
        current_index = indexes_dict['current_index']
    if current_index>max_index:
        print('Все pdf собраны')
        break
    try:
        main(current_index=current_index)
    except:
        requests.get('https://mobiproxy.net/proxy/update/019ca089e1f35683aa8f7c0062c943e9/')
        continue