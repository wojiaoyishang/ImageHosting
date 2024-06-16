__author__ = "Yishang"
__date__ = "2024-06-16"
__version__ = "1.0"
__description__ = "图几度图床"

import requests

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


def upload_file(filename, filedata, filetype, session=None):
    if session is None:
        session = requests.session()

    session.get("https://img.90dao.com/", headers=headers)  # 先获取 PHPSESSID

    data = {
        "fileId": filename,
        "initialPreview": "[]",
        "initialPreviewConfig": "[]",
        "initialPreviewThumbTags": "[]",
        "apiType": "this",
        "privateStorage": ""
    }

    response = session.post("https://img.90dao.com/api/upload/upload", data=data,
                            files={"image": (filename, filedata, filetype)})

    if response.json()['code'] != 200:  # 不是则上传失败
        raise RuntimeError(response.json())

    return [response.json()['data']['url']['this']]
