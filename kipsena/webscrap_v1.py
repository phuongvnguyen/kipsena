"""
This program is to scrap news from cafef.vn
author: Phuong V. Nguyen (phuongnv@iuj.ac.jp)
"""
import bs4
import pandas
import requests
import re
import time
import pandas as pd
from IPython.core.display import display


def get_bsoup(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    # print(soup.prettify())
    return soup


def get_link(soup):
    link = []
    for sub in soup.find_all('a'):
        link.append(sub.get('href'))
        use_link = link[4:260]
    print('%d raw links found:' % (len(use_link)))
    return use_link


def clean_link(raw_links):
    cleaned_link = []
    for i in range(len(raw_links)):
        text = re.sub(r"[^A-Za-z0-9(),!?\'`]", " ", used_link[i])
        for word in text.split():
            if word.isdigit():
                cleaned_link.append(raw_links[i])
        else:
            'do no thing'
    plain_link = list(dict.fromkeys(cleaned_link))
    print('%d cleaned links found:' % (len(plain_link)))
    return plain_link


def get_news(link_news):
    date = []
    month = []
    hour = []
    indus = []
    title = []
    content = []
    for i in range(len(link_news)):
        print(link_news[i], i)
        url_spec = 'https://cafef.vn' + link_news[i]
        print(url_spec)
        spec_soup = get_bsoup(url=url_spec)
        dt = spec_soup.find_all('span', class_='time timeliveheader')
        if dt==[]:
            date.append('no record on web')
            month.append('no record on web')
            hour.append('no record on web')
            indus.append('no record on web')
            title.append(spec_soup.find_all('title')[0].text)
            text = [p.text for p in spec_soup.find_all('p')]
            # join_text = ''.join(text[6:-1])
            content.append(text[5:-1])
        else:
            dt = spec_soup.find_all('span', class_='time timeliveheader')[0]
            date.append(dt.get('data-date'))
            month.append(dt.get('data-month'))
            hour.append(dt.text)
            text = [p.text for p in spec_soup.find_all('p')]
            indus.append(text[5])
            title.append(spec_soup.find_all('title')[0].text)
            # join_text = ''.join(text)
            content.append(text[5:-1])

    news_cafef = pd.DataFrame({'Date': date,
                               'Month': month,
                               'Hour': hour,
                               'Industry': indus,
                               'Title': title,
                               'Content': content})
    return news_cafef


if __name__ == '__main__':
    while True:
        link = 'https://cafef.vn/'
        soup_cafe = get_bsoup(url=link)
        used_link = get_link(soup_cafe)
        cleaned_link = clean_link(used_link)
        my_news = get_news(cleaned_link[0:5])
        display(my_news)
        time.sleep(20)
