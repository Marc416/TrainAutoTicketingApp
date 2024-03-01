from enum import Enum
from time import sleep

from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

from email_sender import gmail_sender
from naver_sms_sender import send_sms
from main_app import my_auth

options = Options()
options.add_experimental_option("detach", True)
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)  # 크롬드라이버 경로


def main():
    # u = "https://www.naver.com"
    korail_site = "https://etk.srail.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000"
    driver.get(korail_site)
    driver.implicitly_wait(10)  # 0.5초 기다림 (웹브라우저 로딩 sync 맞추기위해서)

    input_id_pwd()
    click_login_button()
    catch_ticket()


def input_id_pwd():
    input_id = "srchDvNm01"
    input_pwd = "hmpgPwdCphd01"
    id_field = driver.find_element(by=By.ID, value=input_id)
    id_field.send_keys(my_auth.my_id)
    pwd_field = driver.find_element(by=By.ID, value=input_pwd)
    pwd_field.send_keys(my_auth.my_pwd)
    driver.implicitly_wait(10)


def click_login_button():
    # 클래스가 띄어쓰기로 돼 있으면 '.'으로 교체합니다
    submit_button = driver.find_element(by=By.CLASS_NAME, value="submit.btn_pastel2.loginSubmit")
    submit_button.click()
    driver.implicitly_wait(30)


def catch_ticket():
    # select 필드의 옵션 value를 선택합니다
    # 1. 출발역 입력
    dparting_station(station=STATION.수서)
    # 2. 도착역 입력
    arrival_station(station=STATION.동대구)
    # 3. 출발일 입력
    select_departing_date(date="2023.01.21")

    # 4. ~ 시간 이후
    select_ticket_time_after("14")
    # 5. 조회하기 버튼 클릭
    click_submit_for_search()

    # 6. 예약하기


    # 테이블 제목 인덱스 0,1 은 제외시킨다
    # 0: ex)동대구 → 수서   2023년 6월 5일(월)
    # 1: 테이블 컬럼
    # index 2 가 첫번째 티켓임.
    _ticket_base_index = 1
    _target_row = 2     # n번 째 티켓
    target_ticket = _ticket_base_index + _target_row    # 몇번o째 티켓인지
    # _ticket_column_type: {0: 구분, 1: 열차종류, 2: 열차번호, 3: 출발시간, 4: 도착시간, 5: 소요시간, 6: 예약하기(매진)}
    _ticket_column_type = 6
    idx = 0  # 시도횟수
    while True:
        # 타겟한 티켓 찾기
        ticket_element = driver.find_elements(by=By.TAG_NAME, value='tr')[target_ticket]  # n번째 티켓
        ticket = ticket_element.find_elements(by=By.TAG_NAME, value='td')[_ticket_column_type]
        ticket_name = ticket.text
        if ticket_name == "매진" or ticket_name == "입석+좌석":
            idx += 1
            print(f"{ticket_name}:{idx}")
            # 밴을 당하지 않기 위해 n초 텀을 가집니다
            sleep(1)
            driver.refresh()
            continue

        book_buttons = driver.find_elements(by=By.CLASS_NAME, value="btn_small.btn_burgundy_dark.val_m.wx90")
        for idx, book_button in enumerate(book_buttons):
            if idx != 0:
                driver.implicitly_wait(20)
                print(f"{idx}번째 예약하기 버튼이 아님")
                driver.refresh()
                continue

            try:
                if book_button.text != "예약하기":
                    print(f"{idx}번째 예약하기 버튼이 아님")
                    driver.implicitly_wait(20)
                    driver.refresh()
                    continue
            except StaleElementReferenceException as e:
                driver.implicitly_wait(20)
                driver.refresh()
                continue
            driver.implicitly_wait(100)
            driver.execute_script(f'document.getElementsByTagName("tr")[{target_ticket}].getElementsByTagName("td")[{_ticket_column_type}].getElementsByTagName("a")[0].click()')
            send_sms.SendMessage().send()
            # joonheealert로 gmail 보내기
            gmail_sender.sendmail()
            return
        driver.refresh()


class STATION(Enum):
    동대구 = "0015"
    수서 = "0551"
    부산 = "0020"

def select_departing_date(date):
    element = driver.find_element(by=By.CLASS_NAME, value="calendar1")
    driver.execute_script(f"arguments[0].value = '{date}';", element)
    element.submit()

# 출발역
def dparting_station(station):
    _select_station(id="dptRsStnCd", station_number=station.value)  # 수서


# 도착역
def arrival_station(station):
    _select_station(id="arvRsStnCd", station_number=station.value)  # 수서

# 출발역, 도착역 공통
def _select_station(id, station_number):
    select = Select(driver.find_element(by=By.ID, value=id))
    select.select_by_value(station_number)  # 수서


# 00 시 이후 (srt 페이지에 나와 있는 시간대. 모바일 아님!), 2자리 수로 표현할것
def select_ticket_time_after(time_after):
    select = Select(driver.find_element(by=By.ID, value="dptTm"))
    time = time_after
    select.select_by_value(f"{time}0000")  # 14시 이후
    driver.implicitly_wait(10)


def click_submit_for_search():
    submit = driver.find_element(by=By.CLASS_NAME, value="btn_midium.wp100.btn_burgundy_dark.corner.val_m")
    driver.implicitly_wait(100)
    submit.click()



if __name__ == "__main__":
    main()
