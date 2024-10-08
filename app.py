from typing import Optional
from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('currency_rates.db')
    conn.row_factory = sqlite3.Row
    return conn

# Маршрут для получения курсов валют с диапазоном дат и необязательными параметрами
@app.get("/rates/")
def get_rate(currency_code: Optional[str] = None, 
             base_currency_code: Optional[str] = None, 
             start_date: Optional[str] = None, 
             end_date: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Построение запроса динамически
    query = "SELECT * FROM currency_exchange WHERE 1=1"
    params = []
    
    if currency_code:
        query += " AND currency_code = ?"
        params.append(currency_code)
        
    if base_currency_code:
        query += " AND base_currency_code = ?"
        params.append(base_currency_code)
    
    # Добавление диапазона дат
    if start_date and end_date:
        query += " AND date BETWEEN ? AND ?"
        params.append(start_date)
        params.append(end_date)
    elif start_date:
        query += " AND date >= ?"
        params.append(start_date)
    elif end_date:
        query += " AND date <= ?"
        params.append(end_date)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        raise HTTPException(status_code=404, detail="Rate not found")
    
    return {"rates": [dict(row) for row in rows]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)