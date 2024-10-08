import requests
from proxy_seller_user_api import Api
from config import API_KEY

def generate_proxy_string(data):
    proxy_info = data  # Извлекаем первый элемент списка
    login = proxy_info['login']
    password = proxy_info['password']
    port = 10000  # Используем фиксированный порт, как в примере
    host = 'res.proxy-seller.com'  # Используем домен
    
    proxies = {
        "http": f"http://{login}:{password}@{host}:{port}",
        "https": f"https://{login}:{password}@{host}:{port}"
    }
    # print(proxy_string)
    return proxies



def get_active_proxies():
    try:
        api = Api({'key':API_KEY})
        result = []
        proxy_list = api.residentList()

        for proxy in proxy_list:
            result.append(generate_proxy_string(proxy))
            # result.append(generate_proxy_string(proxy))
        return result
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


# print(get_active_proxies())



