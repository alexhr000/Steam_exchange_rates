from urllib import request
from parse import parse_exchanges_rates
from Steam_auth import Steam_auth
from db_input import db_input
from proxies import get_active_proxies
from logger import send_msg_to_telegram, setup_logger
import asyncio
import json
import urllib3
import schedule
import time


async def update_currency_rates():
    try:
        logger = setup_logger()  
        # получаем список прокси
        # with open('proxies.json', 'r', encoding='utf-8') as file:
        #     proxies_list = json.load(file)
        proxies_list = get_active_proxies()
        # Авторизуемся в стим через селениум и получаем данные для сессии 
        auth_data = Steam_auth()
        cookies = auth_data[0]
        headers = auth_data[1]
        exchanges_rates_list = []
        # обходим список стран(прокси)
        for proxies in proxies_list:
            exchanges_rates_list.append(parse_exchanges_rates(proxies,cookies,headers))

        # Форматируем с отступами для лучшей читаемости
        formatted_str = ""
        for exchange_rate_str in exchanges_rates_list:
            try:
                # Преобразуем строку в объект Python (список словарей)
                exchange_rate_data = json.loads(exchange_rate_str)
                # Форматируем данные в нужном виде
                for item in exchange_rate_data:
                    formatted_str += f'"currency_pair": "{item["currency_pair"]}",\n"value": {item["value"]}\n'
            except json.JSONDecodeError as e:
                print(f"Ошибка при обработке JSON: {e}")
        await send_msg_to_telegram(f'Результат парсинга: {formatted_str}')
        # Запись результата в бд 
        db_input(exchanges_rates_list)
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}") 
        await send_msg_to_telegram(f'Произошла ошибка: {e}')
def run_async_update_currency_rates():
    loop = asyncio.get_event_loop()
    loop.create_task(update_currency_rates()) 

schedule.every().day.at("21:00").do(run_async_update_currency_rates)

async def main():
 # Запуск асинхронной функции в синхронном контексте
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)  # Задержка для предотвращения излишней нагрузки

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # убрать варнинг о сертификатах
    asyncio.run(main())