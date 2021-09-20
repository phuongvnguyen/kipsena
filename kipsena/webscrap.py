"""
This program is to scrap news from cafef.vn
author: Phuong V. Nguyen (phuongnv@iuj.ac.jp)
"""
import pandas as pd
import requests
import bs4
from IPython.core.display import display


def get_title(link='https://cafef.vn/'):
    """
    This function is to get list of titles from cafef
    :param link: default link is cafef
    :return:
    """
    page = requests.get(link)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    # soup.prettify()
    Title = []
    soup.find_all('span')
    ## title pickup
    soup.find_all('span', class_='inner')
    for tit in soup.find_all('span', class_='inner'):
        Title.append(tit.text)
    Title
    ## time publish
    Date = []
    Month = []
    Hour = []
    for dt in soup.find_all('span', class_='time timeliveheader'):
        Date.append(dt.get('data-date'))
        Month.append(dt.get('data-month'))
        Hour.append(dt.text)
    news = pd.DataFrame({'Date': Date,
                         'Month': Month,
                         'Hour': Hour,
                         'Title': Title})
    display(news)
    return news


if __name__ == '__main__':
    get_title()
