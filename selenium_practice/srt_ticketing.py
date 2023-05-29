from time import sleep

from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from selenium_practice import my_auth

options = Options()
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(executable_path="chromedriver", options=options)  # 크롬드라이버 경로


def main():
    # u = "https://www.naver.com"
    korail_site = "https://etk.srail.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000"
    driver.get(korail_site)
    driver.implicitly_wait(10)  # 0.5초 기다림 (웹브라우저 로딩 sync 맞추기위해서)

    input_id_pwd()
    click_login_button()
    find_condition()


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


def find_condition():
    # select 필드의 옵션 value를 선택합니다
    # 1. 출발역 입력
    _select_station(id="dptRsStnCd", station_number="0551")  # 수서
    # 2. 도착역 입력
    _select_station(id="arvRsStnCd", station_number="0015")  # 동대구
    # 3. 출발일 입력
    element = driver.find_element(by=By.CLASS_NAME, value="calendar1")
    date = "2023.06.02"
    driver.execute_script(f"arguments[0].value = '{date}';", element)
    element.submit()
    # driver.execute_script("arguments[0].value = 'New Value';", element)

    # 4. ~ 시간 이후
    select = Select(driver.find_element(by=By.ID, value="dptTm"))
    time = "20"
    select.select_by_value(f"{time}0000")  # 14시 이후
    driver.implicitly_wait(10)
    # 5. 조회하기 버튼 클릭
    submit = driver.find_element(by=By.CLASS_NAME, value="btn_midium.wp100.btn_burgundy_dark.corner.val_m")
    submit.click()
    driver.implicitly_wait(100)

    # 6. 예약하기

    idx = 0
    while True:
        # 테이블 제목 인덱스 0,1 은 제외시킨다
        t = driver.find_elements(by=By.TAG_NAME, value='tr')[2]  # 첫번째 티켓
        if t.find_elements(by=By.TAG_NAME, value='td')[6].text == "매진":
            idx += 1
            print(f"매진{idx}")
            sleep(3)
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
            driver.execute_script(f'document.getElementsByClassName("btn_small btn_burgundy_dark val_m wx90")[{idx}].click()')
            # 이메일이나 카톡으로 알람을 주면 좋을거 같음
        driver.refresh()
        # return


def _select_station(id, station_number):
    select = Select(driver.find_element(by=By.ID, value=id))
    select.select_by_value(station_number)  # 수서


if __name__ == "__main__":
    main()
