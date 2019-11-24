# cloud-ocr

调用百度/讯飞 OCR 开放api识别图片中的文字

### Prerequisite

Python 3.6.6 以上

### Installation

```shell
pip install cloud-ocr
```

### Usage

首先需要申请对应平台的调用密钥
 - 百度 (https://console.bce.baidu.com/ai/)
 - 讯飞 

```python
from cloud_ocr import *

# use xunfei (需将外网ip添加到讯飞api控制台白名单)
client = XunFeiOcr(app_id, app_key)
client.analyze(image_path)

# use baidu api, url可选择general(默认), basicGeneral, basicAccurate,  accurate几个选项
client = BaiduOcr(app_id, api_key, secret_key)
print(client.analyze(img_path, url))

# throttle api call frequency.
ocr_func = Throttle(seconds=1)(client.analyze) # call api every second
for i in range(10):
  ocr_func(img_path)
```

