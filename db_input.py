from datetime import datetime
import sqlite3
import json

def db_input(exchanges_rates_list):
    conn = sqlite3.connect('currency_rates.db')
    cursor = conn.cursor()

    # Сохранение данных в базу данных
    for item in exchanges_rates_list:
        json_data = json.loads(item)
        for exchange in json_data:
            currency_pair = exchange['currency_pair']
            value = exchange['value']
            
            # Разделение валютной пары
            base_currency, currency_code = currency_pair.split('/')
            
            # Получение текущей даты
            date = datetime.now().strftime('%Y-%m-%d')

            # Вставка данных в таблицу
            cursor.execute('''
            INSERT INTO currency_exchange (currency_code, base_currency_code, exchange_rate, date)
            VALUES (?, ?, ?, ?)
            ''', (currency_code, base_currency, value, date))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()