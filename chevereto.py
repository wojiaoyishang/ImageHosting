__author__ = "Yishang"
__date__ = "2024-06-16"
__version__ = "1.0"
__description__ = "任何 chevereto 形式的图床"

import re
import time

import requests

"""
先 GET https://www.imagehub.cc/login HTTP/1.1 获取 auth_token
再 POST https://www.imagehub.cc/login HTTP/1.1 登录
login-subject	username
password	password
auth_token	auth_token

有：
www.imagehub.cc imagehub 图床（默认）
imgse.com 路过图床
"""

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
}


def login(username, password, session=None, host="www.imagehub.cc"):
    if session is None:
        session = requests.session()

    session.headers.update(headers)
    response = session.get(f"https://{host}/login")
    match = re.search(r"""PF.obj.config.auth_token = "(.*)";""", response.content.decode())

    if match is None:  # 让 IDE 正确识别 match ，有点强迫症
        assert match is None  # 不能获取 auth_token ，可能你被 ban 了

    auth_token = match.group(1)
    session.auth_token = auth_token  # 加入 auth_token

    response = session.post(f"https://{host}/login", data={
        "login-subject": username,
        "password": password,
        "auth_token": auth_token
    }, allow_redirects=False)

    assert response.status_code == 301  # 报错登录失败

    return session


def upload_file(filename, filedata, filetype, session, expiration="", nsfw="", host="www.imagehub.cc"):
    """
    上传文件。

    空 -- 不删除
    PT5M -- 经过 5 分钟
    PT15M -- 经过 15 分钟
    PT30M -- 经过 30 分钟
    PT1H -- 经过 1 小时
    PT3H -- 经过 3 小时
    PT6H -- 经过 6 小时
    PT12H -- 经过 12 小时
    P1D -- 经过 1 天
    P2D -- 经过 2 天
    P3D -- 经过 3 天
    P4D -- 经过 4 天
    P5D -- 经过 5 天
    P6D -- 经过 6 天
    P1W -- 经过 1 周
    P2W -- 经过 2 周
    P3W -- 经过 3 周
    P1M -- 经过 1 月
    P2M -- 经过 2 月
    P3M -- 经过 3 月
    P4M -- 经过 4 月
    P5M -- 经过 5 月
    P6M -- 经过 6 月
    P1Y -- 经过 1 年

    :param filename: 文件名
    :param filedata: 文件二进制数据
    :param filetype: 文件类型
    :param session: 会话
    :param expiration: 过期时间
    :param nsfw: 是否标记为 nsfw
    :return: URL，放在一个列表里
    """
    response = session.post(f"https://{host}/json", data={
        "type": "file",
        "action": "upload",
        "timestamp": int(time.time() * 1000),
        "auth_token": session.auth_token,
        "expiration": expiration,
        "nsfw": nsfw
    }, files={'source': (filename, filedata, filetype)}, headers={'Accept': 'application/json'})

    if response.json()['success']['code'] != 200:
        raise RuntimeError(response.json())

    return [response.json()['image']['display_url']]


