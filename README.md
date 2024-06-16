# Python 图床爬虫

#### 介绍
集成了市面上大部分的图床，可以通过函数直接调用。如有疑问或者发现新的图床，请提交 PR 或者 Issues 。

 **目前程序并不完善，仅供测试使用，欢迎大家参与开发。** 

#### 支持的图床

| 图床         | 支持访客 | 网址                      | 爬虫方式 | 限制说明 |
|------------|------|-------------------------|-----------|---------|
| postimages | √ | https://postimages.org/ | 爬虫，无反爬 | 不清楚 |
| 图几度图床 | √ | https://img.90dao.com/ | 爬虫，无反爬 | 单个文件支持最大 3 MB. 每次最多允许 5 张图片上传 |
| imagehub （chevereto）| × | https://www.imagehub.cc/ | 爬虫，无反爬 | 支持单张最大10MB图片 |
| 路过图床（chevereto）| × | https://imgse.com/ | 爬虫，无反爬 | 最大单张支持10MB图片 |
| 聚合图床 | × | https://www.superbed.cn/ | 爬虫，有反爬 | 普通用户不清楚，VIP才能用API |
| 水墨图床 | × | https://img.ink/ | API直接调用 | 普通用户最大 2GB 空间 |

#### 使用方法

+ 示例（postimages，无须登录）

```python
import mimetypes
import postimages

filepath = "test.png"
filename = filepath.split('/')[-1]

# 尝试确定文件类型
filetype, _ = mimetypes.guess_type(filepath)
if filetype is None:
    filetype = 'application/octet-stream'  # 使用通用二进制类型，如果无法猜测类型

# 读取文件数据
with open(filepath, 'rb') as file:
    filedata = file.read()

print(postimages.upload_file(filename, filedata, filetype)[0])
```

+ 说明

每个模块都有 `upload_file` 函数，其基本定义如下代码所示，这个函数至少接受 `filename`, `filedata`, `filetype` 三个参数，至于为什么不直接通过文件路径直接上传文件的原因是为了提供更大的操作性。比如在处理已经预先保存在内存中的文件时：我在网络上爬取了图片到内存，我可以直接通过 `upload_file` 函数进行上传。

```python
def upload_file(filename, filedata, filetype, session=None):
    """
    将文件上传至 xxx。    
    """
```

参数 `session` 是 `requests.Session` ，保留这个参数是为了更好的控制请求流程与方式（特别是设计到登录的时候），以下例子可以切换请求时的代理：

```python
session = requests.session()

# 设置代理
session.proxies.update({
    'http': 'http://10.10.1.10:3128',
    'https': 'https://10.10.1.10:1080',
})

print(postimages.upload_file(filename, filedata, filetype)[0], session=session)
```

+ 示例（聚合图床，需要登录）

```python
import mimetypes
import postimages

filepath = "test.png"
filename = filepath.split('/')[-1]

# 尝试确定文件类型
filetype, _ = mimetypes.guess_type(filepath)
if filetype is None:
    filetype = 'application/octet-stream'  # 使用通用二进制类型，如果无法猜测类型

# 读取文件数据
with open(filepath, 'rb') as file:
    filedata = file.read()

# 登录图床
session = superbed.login("username", "password", remember=False)

# 上传图片
print(superbed.upload_file(filename, filedata, filetype, session=session)[0])
```

+ 说明

在需要登录才能使用的图床中，必须先调用 `login` 函数登录，登录成功后会返回 `session` （失败报错），这个 `session` 会保存你的登录信息，需要传递给 `upload_file` 函数。

 **注意：不同平台的图床决定了 `upload_file` 所支持的参数，比如 `postimages` 的 `upload_file` 还支持 `optsize`（重设大小） `expire`（过期时间） 参数，具体参数内容请查看函数注释。** 
