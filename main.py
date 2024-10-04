import requests
from fake_useragent import UserAgent
import json

protected_url = 'https://login.steampowered.com/jwt/finalizelogin'
user_agent = UserAgent()
random_user_agent = user_agent.random

# Токен для авторизации(пока беру вручную из network)
nonce = 'eyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInN0ZWFtIiwgInN1YiI6ICI3NjU2MTE5OTY3NTgyODQ0NCIsICJhdWQiOiBbICJ3ZWIiLCAicmVuZXciLCAiZGVyaXZlIiBdLCAiZXhwIjogMTc0NjQwODY2NCwgIm5iZiI6IDE3MTk0MDM3MDYsICJpYXQiOiAxNzI4MDQzNzA2LCAianRpIjogIjEwQUFfMjUyNjE5MTZfOUI4MkMiLCAib2F0IjogMTcyODA0MzcwNiwgInBlciI6IDEsICJpcF9zdWJqZWN0IjogIjE4NS4xMDcuNTYuMjM4IiwgImlwX2NvbmZpcm1lciI6ICIxODUuMTA3LjU2LjIzOCIgfQ.ECrAPDjQ0hsvgmccDf1vO7k7yTUG-gnVN_yv5kU3DFablcwcPSpCSqJNaymYn_kgh65Itssd0h0uchwDUOLGCg'
sessionid = '71c2961238ea8e906396197a'

params = {
    'nonce': nonce,
    'sessionid': sessionid,
    'redir': 'https://steamcommunity.com/login/home/?goto=',
}
headers = {
    'User-Agent': random_user_agent,
    'Referer': 'https://store.steampowered.com/',
    'Accept': 'application/json'
}

session = requests.Session()

# post запрос для авторизации
response = session.post(protected_url, data=params, headers=headers)

if response.status_code == 200:
    print("Запрос на финализацию логина успешен")
    try:
        response_data = response.json()
        print("Ответ от сервера:", json.dumps(response_data, indent=4))
    except ValueError:
        print("Ошибка при парсинге JSON")
        print("Ответ от сервера:", response.text)
        exit()

    # извлечение transfer_info для передачи токенов аутентификации между сервисами Steam для единого входа (SSO - Single Sign-On)
    transfer_info = response_data.get("transfer_info")
    if not transfer_info:
        print("Поле transfer_info не найдено в ответе")
        print("Ответ от сервера:", response_data)
        exit()
else:
    print(f"Ошибка при авторизации: {response.status_code} - {response.text}")
    exit()

# перебор каждого transfer_info
for transfer in transfer_info:
    url = transfer['url']
    params = transfer['params']

    # Отправляем post запрос для каждого URL
    transfer_response = session.post(url, data=params, headers=headers)
    if transfer_response.status_code == 200:
        print(f"Успешно переданы токены для {url}")
    else:
        print(f"Ошибка при передаче токенов для {url}: {transfer_response.status_code} - {transfer_response.text}")


# После передачи токенов выполняем GET-запрос для получения данных пользователя
userdata_url = 'https://store.steampowered.com/dynamicstore/userdata/?id=1715562716&cc=US&v=2'
response = session.get(userdata_url, headers=headers)
if response.status_code == 200:
    print("Успешно получены данные пользователя")
    session.user_data = response.json()
    # print("Ответ от сервера:", response.json())  # Выводим ответ в формате JSON
else:
    print(f"Ошибка при получении данных пользователя: {response.status_code} - {response.text}")

print("Данные пользователя из сессии:", json.dumps(session.user_data, indent=4))



# Как я понял get запрос к уведомлениям не обязателен 

# # выполняем get запрос к уведомлениям Steam 
# notifications_url = 'https://api.steampowered.com/ISteamNotificationService/GetSteamNotifications/v1'
# access_token = 'eyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTBCMF8yNTI2MTkxOV9DM0QwMSIsICJzdWIiOiAiNzY1NjExOTk2NzU4Mjg0NDQiLCAiYXVkIjogWyAid2ViOnN0b3JlIiBdLCAiZXhwIjogMTcyODEyOTAyNywgIm5iZiI6IDE3MTk0MDE1NzQsICJpYXQiOiAxNzI4MDQxNTc0LCAianRpIjogIjEwQUVfMjUyNjE5MTRfRUEyMTUiLCAib2F0IjogMTcyODA0MTU3NCwgInJ0X2V4cCI6IDE3NDYzOTAyMTYsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICIxODUuMTA3LjU2LjIzOCIsICJpcF9jb25maXJtZXIiOiAiMTg1LjEwNy41Ni4yMzgiIH0.PYsMrGQcDvrcUaPxRlWasMKmiVnkyyT0ZhArIlCVYKbwHwNk7s_kOr0q8MZZDLPVzIkLpBPQkBSkAupVlehnBQ'

# params = {
#     'access_token': access_token,
#     'origin': 'https://store.steampowered.com',
#     'input_protobuf_encoded': 'EAgYACABKAA%3D'  
# }

# response = session.get(notifications_url, headers=headers, params=params)
# if response.status_code == 200:
#     print("Успешно получены уведомления Steam.")
#     session.notifications_data = response.json()  # Сохраняем данные уведомлений в сессии
#     print("Уведомления сохранены в сессии.")
# else:
#     print(f"Ошибка при получении уведомлений: {response.status_code} - {response.text}")
# print("Уведомления из сессии:", json.dumps(session.notifications_data, indent=4))






# После передачи токенов выполняем get запрос к главной странице Steam
# Сохраняем содержимое страницы в HTML
main_page_url = 'https://store.steampowered.com/'
response = session.get(main_page_url, headers=headers)

if response.status_code == 200:
    print("Успешно получена главная страница Steam")
    with open("steam_main_page.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("HTML содержимое главной страницы сохранено в 'steam_main_page.html'")
else:
    print(f"Ошибка при получении главной страницы: {response.status_code} - {response.text}")












