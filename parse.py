import time
import requests
import re
import json
from bs4 import BeautifulSoup
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def parse_amount(amount):
    if amount[0] in '$€¥£₽₴₩':
        currency = {
            '$': 'USD',
            '€': 'EUR',
            '¥': 'JPY',
            '£': 'GBP',
            'р': 'RUB',
            '₴': 'UAH',
            '₸': 'KZT',
            '₣': 'CHF',
            '₱': 'PHP',
            '฿': 'THB',
            '₫': 'VND',
            '₩': 'KRW',
            '₹': 'INR',
            '₪': 'ILS'
        }.get(amount[0], 'UNKNOWN')  # Получаем валюту по символу
        value = float(amount[1:].replace(',', '.'))  # Преобразуем значение в float
    else:
        currency = {
            '$': 'USD',
            '€': 'EUR',
            '¥': 'JPY',
            '£': 'GBP',
            'р': 'RUB',
            '₴': 'UAH',
            '₸': 'KZT',
            '₣': 'CHF',
            '₱': 'PHP',
            '฿': 'THB',
            '₫': 'VND',
            '₩': 'KRW',
            '₹': 'INR',
            '₪': 'ILS'
        }.get(amount[-1], 'UNKNOWN')  # Если символ валюты в конце
        value = float(amount[:-1].replace(',', '.'))  # Преобразуем значение в float

    return {
        "currency": currency,
        "value": value
    }


def parse_exchanges_rates(proxies,cookies,headers):
    # Используем requests для последующих запросов
    # print(proxies)
    session = requests.Session()
    # Настраиваем ретраи
    retry_strategy = Retry(
        total=5,  # количество попыток  
        backoff_factor=1,  # пауза между попытками
        status_forcelist=[502, 503, 504],  # для каких статусов будет повторяться запрос
    )

    # Адаптер с ретраями
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)  

    # Добавляем куки в сессию
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Добавляем заголовки в сессию
    session.headers.update(headers)

    # После передачи токенов выполняем get запрос к странице Steam
    main_page_url = 'https://store.steampowered.com/steamaccount/addfunds/?snr=1_4_4__global-header'
    response = session.get(main_page_url, headers=headers, proxies=proxies, verify=False)

    if response.status_code == 200:
        print("Успешно получена страница смены региона")

        cleaned_html = response.text.replace("&nbsp;", "")

        # Парсинг очищенного HTML с классом 'currency_change_options' в очищенном HTML
        soup = BeautifulSoup(cleaned_html, 'html.parser')
        # with open("steam_main_page.html", "w", encoding="utf-8") as file:
        #         file.write(cleaned_html)
        currency_div = soup.find('div', class_='currency_change_options')
        
        if currency_div:
            pattern = r'([€$¥£₸]\d{1,3}(?:,\d{3})?(?:\.\d{2})?)|(\d{1,10}(?:,\d{2})?[€$¥£₸р₴₩])'

            # Найти все совпадения
            matches = re.findall(pattern, currency_div.text)

            # Объединить результаты и вывести
            results = [match[0] or match[1] for match in matches]
            parsed_amounts = [parse_amount(amount) for amount in results]
            json_data = json.dumps(parsed_amounts, indent=4)
            # print(f"Найденные валюты: {json_data}")


            def calculate_currency_pair(amount1, amount2):
                return amount1['value'] / amount2['value']

            # Получаем курсы валют
            if len(parsed_amounts) >= 2:
                usd_to_eur = calculate_currency_pair(parsed_amounts[0], parsed_amounts[1])
                eur_to_usd = calculate_currency_pair(parsed_amounts[1], parsed_amounts[0])

                # Формируем новый JSON с результатами расчётов
                new_data = [
                    {
                        "currency_pair": f"{parsed_amounts[0]['currency']}/{parsed_amounts[1]['currency']}",
                        "value": round(usd_to_eur, 3)  # Округляем до 3 знаков
                    },
                    {
                        "currency_pair": f"{parsed_amounts[1]['currency']}/{parsed_amounts[0]['currency']}",
                        "value": round(eur_to_usd, 3)  # Округляем до 3 знаков
                    }
                ]

                # Преобразуем результат в формат JSON
                new_json_data = json.dumps(new_data, indent=4)
                # print(f"Полученны курсы валют: {new_json_data}")
                return new_json_data
            else:
                print("Недостаточно данных для расчета курсов валют.")

        else:
            print("div с классом 'currency_change_options' не найден.")

    else:
        print(f"Ошибка при получении главной страницы: {response.status_code} - {response.text}")
