import base64
import hashlib
import hmac
import json
import time

import requests

from naver_sms_sender.secret import credential

# https://api.ncloud-docs.com/docs/common-ncpapi
# method = 'POST'
# uri = 'https://sens.apigw.ntruss.com/sms/v2/services/{serviceId}/messages'
timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

url = "https://sens.apigw.ntruss.com"
uri = f"/sms/v2/services/{credential.service_id}/messages"


def make_signature(method: str, uri: str):
    access_key = f"{credential.access_key}"  # access key id (from portal or Sub Account)
    secret_key = f"{credential.secret_key}"  # secret key (from portal or Sub Account)
    secret_key = bytes(secret_key, 'UTF-8')

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey


header = {
    "Content-Type": "application/json",
    "x-ncp-apigw-timestamp": timestamp,
    "x-ncp-iam-access-key": credential.access_key,
    "x-ncp-apigw-signature-v2": make_signature('POST', uri)
}

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


# if __name__ == "__main__":
#     # make_signature()
#     res = requests.post(url + uri, headers=header, data=json.dumps(data))
#     print(res)
