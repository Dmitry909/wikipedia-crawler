import requests

ya = 'https://ya.ru'

header = {'cookie': 'i=op4FjmO7Nw4kqBrUmGn/jz+dZJ0b0lQsUz6cxesqAeefFk6QI1n1bqdAw/NYPyVQylrZBtmnqVQumq8rl71xP9aMqy8=; '
                    'yandexuid=5284275401623155590;'}

r = requests.get(ya, headers=header, verify=False)

for co in r.cookies.items():
    print(co)
