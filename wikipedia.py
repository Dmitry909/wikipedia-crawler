import requests
from bs4 import BeautifulSoup
import time

start_url = 'https://en.wikipedia.org/wiki/Special:Random'
final_url = 'https://en.wikipedia.org/wiki/Philosophy'


def get_first_link(cur_url):
    r = requests.get(cur_url)
    html_cur_page = r.text
    soup = BeautifulSoup(html_cur_page, 'html.parser')
    title = soup.title.string
    title = title[:len(title) - 12]
    div_text = soup.find(id='mw-content-text')
    next_url = ''
    for el in div_text:
        div_text = el
        break
    was_real_text = False
    for el in div_text.find_all('p'):
        el = str(el)
        if el[:2] == '<p':
            el = el[2:]
            el = el[el.find('>') + 1:]
            el = el[:len(el) - 4]
            el = el[:el.rfind('>') + 1]
        if (len(el) > 2 and el[1] == 'i' and el[-2] == 'i') or el.find('not-searchable') > -1 or el.find('role="note"') > -1 or el.find('class="image"') > -1:
            continue
        el = el.replace('<a ', '<a>')
        el = el.replace('/a>', '<a>')
        was_real_text = True
        els = el.split('<a>')
        balance = 0
        for s in els:
            while len(s) and (s[-1] == '<' or s[-1] == '>'):
                s = s[:len(s) - 1]
            if s.find('href=') > -1 and s[-1] != ']':
                if balance == 0:
                    s = s[s.find('href=') + 6:]
                    next_url = s[:s.find('"')]
                    break
            else:
                balance += s.count('(') - s.count(')')
        # lis = el.find_all('a')
        # for link in lis:
        #     if len(lis) and link.get('href').find(':') == -1:
        #         next_url = link.get('href')
        #         break
        if len(next_url):
            break
    if next_url == '':
        return title, ''
    return title, cur_url[:cur_url.find('wiki/') - 1] + next_url


cnt_ph = 0
iterations = 100
for i in range(iterations):
    cur_url = start_url
    visited = set()
    print(cur_url)
    while cur_url != final_url:
        title, next_url = get_first_link(cur_url)
        print(next_url)
        if title in visited:
            print('loop :(')
            break
        visited.add(title)
        # time.sleep(2.5)
        cur_url = next_url
    if cur_url == final_url:
        # print('Philosophy')
        print('success!')
        cnt_ph += 1

print('accuracy:', cnt_ph / iterations)