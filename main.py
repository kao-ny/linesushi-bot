from linebot.models import (
    TextSendMessage,
)

import urllib.request
import urllib.parse

import json
import pandas as pd

def create_message(latitude, longitude):
    urlbase = 'https://api.gnavi.co.jp/RestSearchAPI/20150630/?'

    q = [
        ('keyid', '4e7a04b747477a337e42203df3db7b19'),
        ('latitude', float(latitude)),
        ('longitude', float(longitude)),
        ('category_s', 'RSFST03001'), # 寿司
        ('format', 'json')
    ]

    url = urlbase + urllib.parse.urlencode(q)

    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req)

    content = json.loads(res.read().decode('utf8'))

    shops = pd.DataFrame(index=[], columns=["name", "url_mobile", "budget"])
    for i in content['rest']:
        s_name = i['name']
        s_url = i['url_mobile']
        if i['budget'] == {}:
            s_budget = 0
        else:
            s_budget = int(i['budget'])

        series = pd.Series([s_name, s_url, s_budget], index=shops.columns)
        shops = shops.append(series, ignore_index=True)

    shops.sort_values('budget', inplace=True, ascending=False)

    result_shop = shops.iloc[0]
    name = result_shop['name']
    url_mobile = result_shop['url_mobile']
    budget = result_shop['budget']

    msg = '🍣 {name}\n💸 {budget} YEN\n\n🌐: {url_mobile}'.format(name=name, budget=budget, url_mobile=url_mobile)
    message = TextSendMessage(text = msg)

    return message
