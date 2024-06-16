__author__ = "Yishang"
__date__ = "2024-06-16"
__version__ = "1.0"
__description__ = "水墨图床"

import requests


# 官方有提供 API 直接调用

def upload_file(filename, filedata, filetype, token, folder=""):
    """
    上传图片

    :param filename: 文件名
    :param filedata: 文件文件二进制数据
    :param filetype: 文件类型
    :param token: 提供的 token
    :param folder: 自定义上传文件夹名，仅支持一级目录，会在外链中展示。仅支持英文与数字，不存在的文件夹会自动创建。
    :return: URL，放在列表里
    """
    response = requests.post("https://img.ink/api/upload", data={'folder': folder},
                             files={'image': (filename, filedata, filetype)},
                             headers={'token': token})

    if response.json()['code'] != 200:  # 不是则上传失败
        raise RuntimeError(response.json())

    return [response.json()['data']['url']]

