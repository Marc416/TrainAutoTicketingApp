# post로 request 날리기
import json
from time import sleep

import requests

from naver_sms_sender import make_signature

data = {
    "type": "SMS",
    "from": "01048746269",
    "subject": "SRT 예매 완료",
    "content": "SRT 예매 완료 10분내로 결제를 완료해주세요.",
    "messages": [
        {
            "to": "01048746269"
        }
    ]
}


class SendMessage:
    def send(self):
        res = requests.post(make_signature.url + make_signature.uri, headers=make_signature.header, data=json.dumps(data))
        print(res.content)
        print(res.status_code)
        # if res.status_code == 401:
        #     # sleep(5)
        #     self.send()
