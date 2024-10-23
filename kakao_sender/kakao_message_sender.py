import requests

from main_app.my_auth import KAKAO_TOKEN


def send_kakao_message_to_me():
    try:
        requests.post(
            url="https://kapi.kakao.com/v2/api/talk/memo/default/send",
            headers={
                "Authorization": f"Bearer {KAKAO_TOKEN}",
            },
            data={
                "template_object": '{"object_type": "text", "text": "srt 열차가 예매됐습니다. 10분안에 결제해주세요.", "link": {}}'
            }
        )
    except Exception as e:
        print(e)

if __name__ == '__main__':
    send_kakao_message_to_me()