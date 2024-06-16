__author__ = "Yishang"
__date__ = "2024-06-16"
__version__ = "1.0"
__description__ = "聚合图床"

import random
import hashlib
import requests

"""
POST https://api.superbed.cn/upload HTTP/1.1

nonce 生成：
Math.round(Math.random() * 1000000000)

token 来源：
getCookie("token")

ts 来源：
$.get "/?code=1" 取 json ts

sign 生成：
md5(token + "-*-" + nonce + "-*-" + ts)

_0x53cb27.append("_xsrf", getCookie("_xsrf") || "");
_0x53cb27.append("endpoints", getCookie("endpoints") || "");
_0x53cb27.append("categories", getCookie("categories") || "");


POST https://www.superbed.cn/signin HTTP/1.1

username	xxx
password	xxx
remember	off/on
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


def login(username, password, remember, session=None):
    if session is None:
        session = requests.session()

    response = session.post("https://www.superbed.cn/signin", data={
        'username': username,
        'password': password,
        'remember': 'on' if remember else "off"
    }, headers=headers)

    # {"err": 0, "user": {"_id": "xxx", "username": "xxxx",
    # "created_at": "2024-06-16 14:37:29", "email": "xxx",
    # "ip": "xxx", "password": "xxxxx",
    # "token": "xxx", "id": 122141, "images": 2,
    # "categories": {"\u9ed8\u8ba4\u76f8\u518c": 1}}}

    try:
        assert response.json()['err'] == 0
        return session
    except AssertionError:
        raise RuntimeError("用户登录失败：", response.json())


def upload_file(filename, filedata, filetype, session):
    """
    上传图片。

    :param filename: 文件名
    :param filedata: 文件二进制数据
    :param filetype: 文件类型
    :param session: 会话
    :return: URL，在一个列表里
    """
    # 获取 ts 门票
    response = session.get("https://www.superbed.cn/?code=1", headers=headers)

    # {"url": "https://api.superbed.cn/upload", "ts": 1718524816, "token": "xxx", "active": true}
    assert response.json()['active']  # 如果 active 是 False 说明服务器验证不通过
    upload_url = response.json()['url']

    # 构造表单参数
    token = session.cookies.get("token")
    nonce = str(random.randint(100000000, 999999999)) + "." + str(random.randint(1000000, 9999999))
    ts = response.json()['ts']
    sign = hashlib.md5((token + "-*-" + nonce + "-*-" + str(ts)).encode()).hexdigest()
    _xsrf = session.cookies.get("_xsrf", "")
    endpoints = session.cookies.get("endpoints", "")
    categories = session.cookies.get("categories", "")

    # {'err': 0, 'id': '666e9b93d9c307b7e9083eb3', 'url': 'https://pic.imgdb.cn/item/666e9b93d9c307b7e9083eb3.png',
    # 'size': 751791, 'ids': ['666e9b93d9c307b7e9083eb3'],
    # 'urls': ['https://pic.imgdb.cn/item/666e9b93d9c307b7e9083eb3.png']}
    response = session.post(upload_url, data={
        "token": token,
        "nonce": nonce,
        "ts": ts,
        "sign": sign,
        "_xsrf": _xsrf,
        "endpoints": endpoints,
        "categories": categories
    }, files={'file': (filename, filedata, filetype)})

    return response.json()['urls']
