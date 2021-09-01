# coding=UTF-8
import os
import json
import urllib
import requests
import configparser

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}


def get_token_appjmp(session, sku_id):
    sku_id = '100012043978'
    body = '{"action":"to","to":"https%3A%2F%2Fdivide.jd.com%2Fuser_routing%3FskuId%3D' + sku_id + '"}'
    payload = {'functionId': 'genToken',
               'clientVersion': '9.5.4',
               'client': 'android',
               'uuid': '60439a1c4e78bca9',
               'body': body,
               }
    string = 'st=1621846685250&sign=bdbfdac2873edc7ae66a71134ff28688&sv=121'
    url = 'https://api.m.jd.com/client.action?{}&{}'.format(urllib.parse.urlencode(payload), string)
    data = {'body': body}
    try:
        resp = session.post(url=url, data=data, headers=headers)
        resp_json = json.loads(resp.text)
        token_key = resp_json.get('tokenKey')
        appjmp_url = resp_json.get('url')
        return token_key, appjmp_url
    except Exception as e:
        print('获取token_key异常：{}'.format(e))
        return '', ''


def get_user_routing(session, sku_id, token_key, appjmp_url):
    payload = {'tokenKey': token_key,
               'to': 'https://divide.jd.com/user_routing?skuId={}'.format(sku_id)}
    try:
        resp = session.get(url=appjmp_url, params=payload, headers=headers, allow_redirects=False)
        user_routing = resp.headers['Location']
        return user_routing
    except Exception as e:
        print('获取user_routing异常：{}'.format(e))


def get_pt_key(session, sku_id):
    token_key, appjmp_url = get_token_appjmp(session, sku_id)
    get_user_routing(session, sku_id, token_key, appjmp_url)
    string = 'pt_pin={};pt_key={};'.format(session.cookies['pt_pin'], session.cookies['pt_key'])
    return string


def get_account(file_name='config.ini'):
    file = os.path.join(os.getcwd(), file_name)
    config = configparser.RawConfigParser()
    if not os.path.exists(file):
        config.add_section('account')
        with open(file_name, 'w') as f:
            config.write(f)
    config.read(file, encoding='utf-8-sig')
    sections = config.sections()
    if 'account' not in sections:
        config.add_section('account')
        with open(file_name, 'w') as f:
            config.write(f)
    return config.items('account')


def string_to_cookies(string):
    try:
        item_list = string.split(';')
        cookies_dict = {}
        for item in item_list:
            if item:
                name, value = item.strip().split('=', 1)
                cookies_dict[name] = value
        cookies = requests.utils.cookiejar_from_dict(cookies_dict, cookiejar=None, overwrite=True)
        return cookies
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print('Power By JACK')
    account_list = get_account()
    for account in account_list:
        session = requests.session()
        cookies = string_to_cookies(account[1])
        session.headers = headers
        session.cookies = cookies
        print('【{}】'.format(account[0]))
        string = get_pt_key(session, '')
        print(string)
    input("\n")
