import datetime
import time
from enum import Enum
from time import sleep
import os

from selenium import webdriver
from selenium.common import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from kakao_sender.kakao_message_sender import send_kakao_message_to_me

from main_app import my_auth

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("headless")
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)
DEFAULT_TIME_OUT_SECOND = 120  # 브라우저대기시간 ; 대기자가 많은경우 60초이상으로 설정하여 기다리기


class STATION(Enum):
    동대구 = "0015"
    수서 = "0551"
    부산 = "0020"
    평택 = "0553"
    오송 = "0297"


# 시간대(온라인홈페이지에 나온는 시간대만 사용가능)
class TIME(Enum):
    _00 = "00"
    _02 = "02"
    _04 = "04"
    _06 = "06"
    _08 = "08"
    _10 = "10"
    _12 = "12"
    _14 = "14"
    _16 = "16"
    _18 = "18"
    _20 = "20"
    _22 = "22"


class TRAIN_TYPE_ID(Enum):
    전체 = "trnGpCd109"
    SRT = "trnGpCd300"
    KTX_SRT = "trnGpCd900"


def main():
    korail_site = "https://etk.srail.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000"
    driver.get(korail_site)
    driver.implicitly_wait(3)  # 0.5초 기다림 (웹브라우저 로딩 sync 맞추기위해서)

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


def click_login_button():
    # 클래스가 띄어쓰기로 돼 있으면 '.'으로 교체합니다
    submit_button = WebDriverWait(driver, DEFAULT_TIME_OUT_SECOND).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "submit.btn_pastel2.loginSubmit"))
    )
    submit_button.click()


def catch_ticket():
    # select 필드의 옵션 value를 선택합니다
    # 1. 출발역 입력
    dparting_station(station=STATION.동대구)
    # 2. 도착역 입력
    arrival_station(station=STATION.수서)
    # 3. 출발일 입력
    select_departing_date(date="2025.04.06")

    # 4. ~ 시간 이후
    select_ticket_time_after(time_after=TIME._12)
    # 5. 조회하기 버튼 클릭
    click_submit_for_search(timeout=DEFAULT_TIME_OUT_SECOND)

    # 6. 열차타입 선택
    select_train_type(train_type=TRAIN_TYPE_ID.SRT)

    # 7. 예약하기
    # 테이블 제목 인덱스 0,1 은 제외시킨다
    # 0: ex)동대구 → 수서   2023년 6월 5일(월)
    # 1: 테이블 컬럼
    # index 2 가 첫번째 티켓임.
    _ticket_base_index = 1
    _target_row = 3  # n번 째 티켓
    target_ticket = _ticket_base_index + _target_row  # 몇번o째 티켓인지
    # _ticket_column_type: {0: 구분, 1: 열차종류, 2: 열차번호, 3: 출발시간, 4: 도착시간, 5: 소요시간, 6: 예약하기(매진)}
    _ticket_column_type = 6  # 5: 특실, 6: 일반실
    count = 0  # 예약 시도횟수
    while True:
        # 타겟한 티켓 찾기
        # ticket_element = driver.find_elements(by=By.TAG_NAME, value='tr')[target_ticket]  # n번째 티켓
        try:
            refresh_timeout = 2  # 태그가 안보이면 2초 기다림("짧게설정하는게좋음")

            # Wait until the presence of the element located
            WebDriverWait(driver, refresh_timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))

            # Now find the elements
            ticket_element = driver.find_elements(by=By.TAG_NAME, value='tr')[target_ticket]  # n번째 티켓

        except TimeoutException:
            print("Timed out waiting for the element to load")
            click_show_train_list_btn()
            continue
        except IndexError:
            driver.refresh()
            continue
        ticket = ticket_element.find_elements(by=By.TAG_NAME, value='td')[_ticket_column_type]
        ticket_name = ticket.text
        if ticket_name == "매진" or ticket_name == "입석+좌석":
            count += 1
            print(f"{datetime.datetime.now()} {ticket_name}:{count}")
            # 밴을 당하지 않기 위해 n초 텀을 가집니다
            sleep(1 )
            driver.refresh()
            continue

        book_buttons = driver.find_elements(by=By.CLASS_NAME, value="btn_small.btn_burgundy_dark.val_m.wx90")
        for count, book_button in enumerate(book_buttons):
            if count != 0:
                print(f"{count}번째 예약하기 버튼이 아님")
                driver.refresh()
                continue

            try:
                if book_button.text != "예약하기":
                    print(f"{count}번째 예약하기 버튼이 아님")
                    driver.refresh()
                    continue
            except StaleElementReferenceException as e:
                driver.refresh()
                continue
            driver.execute_script(f'document.getElementsByTagName("tr")[{target_ticket}].getElementsByTagName("td")[{_ticket_column_type}].getElementsByTagName("a")[0].click()')
            # driver.quit()
            print("예약하기 버튼 클릭됨")
            os.system('say "티켓이 예매됐어 빨리 카드결제해"')
            send_kakao_message_to_me()
            return
        driver.refresh()


def select_departing_date(date):
    # element = driver.find_element(by=By.CLASS_NAME, value="calendar1")

    element = WebDriverWait(driver, DEFAULT_TIME_OUT_SECOND).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "calendar1"))
    )
    driver.execute_script(f"arguments[0].value = '{date}';", element)


# 열차타입 선택 : 전체, SRT, KTX+SRT
def select_train_type(train_type: TRAIN_TYPE_ID):
    WebDriverWait(driver, DEFAULT_TIME_OUT_SECOND).until(EC.presence_of_all_elements_located((By.NAME, "trnGpCd")))
    driver.execute_script("window.scrollTo(0, 0);")
    radio_button = driver.find_element(By.ID, train_type.value)  # ID로 라디오 버튼 찾기
    radio_button.click()
    click_show_train_list_btn()


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
def select_ticket_time_after(time_after: TIME):
    select = Select(driver.find_element(by=By.ID, value="dptTm"))
    time = time_after.value
    select.select_by_value(f"{time}0000")  # 14시 이후


def click_submit_for_search(timeout=DEFAULT_TIME_OUT_SECOND):
    try:

        submit = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_midium.wp100.btn_burgundy_dark2.corner.val_m")), None
        )
        submit.click()

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".tal_c.mgt30 .inquery_btn"))  # 다음 페이지의 요소 선택자
        )

        print("Submit button clicked.")

    except TimeoutException:
        print("Timed out waiting for the submit button to become clickable.")

    except NoSuchElementException:
        print("Submit button not found.")


def click_show_train_list_btn():
    try:
        # 다중 클래스에 접근하려면 By.CSS_SELECTOR 사용
        show_train_list_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".tal_c.mgt30 .inquery_btn"))
        )

        # 버튼 클릭 시도
        show_train_list_btn.click()

        # 페이지 로딩 대기
        WebDriverWait(driver, DEFAULT_TIME_OUT_SECOND).until(EC.presence_of_element_located((By.CLASS_NAME, 'etk-seat')))
        print("Page refreshed and fully loaded.")

    # 클릭과 관련된 다양한 예외 처리
    except ElementClickInterceptedException:
        print("Element click intercepted, attempting to refresh the page.")
        driver.refresh()

    except StaleElementReferenceException:
        print("Stale element reference, refreshing the page.")
        driver.refresh()

    except NoSuchElementException:
        print("No such element, attempting to refresh and find it again.")
        driver.refresh()

    except TimeoutException:
        print("Timed out waiting for the element to be clickable, refreshing the page.")
        driver.refresh()

    except TypeError as e:
        print(f"TypeError occurred: {e}, refreshing the page.")
        driver.refresh()


if __name__ == "__main__":
    main()
