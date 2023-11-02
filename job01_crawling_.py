from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

options = ChromeOptions()
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경
df = pd.DataFrame()

wait = WebDriverWait(driver, 1)

for i in range(3,4):
    if i==0:
        url1 = 'https://www.tripadvisor.co.kr/Attractions-g4-Activities-Europe.html'
    else:
        url1 = 'https://www.tripadvisor.co.kr/Attractions-g4-Activities{}-Europe.html'.format("-oa{}".format(30*i))
    driver.get(url1)

    for j in range(2,40):
        try:
            driver.find_element(By.XPATH,'//*[@id="lithium-root"]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/section[{}]/div/div/div/div/article/div[2]/header/div/div/div/a[1]/h3/div/span/div'.format(j)).click()
            time.sleep(5)
            # 새 창이 열리기를 기다립니다.
            # WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            # 모든 창 핸들을 가져옵니다
            window_handles = driver.window_handles

            # 가장 최근에 열린 창으로 전환합니다
            new_window_handle = window_handles[-1]
            driver.switch_to.window(new_window_handle)

            location = []
            country = []
            address = []
            review = []

            locations = driver.find_element(By.XPATH,
                                        '//*[@id="lithium-root"]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1').text  # 여행지 읽기
            location.append(locations)

            countrys = driver.find_element(By.XPATH,'//*[@id="lithium-root"]/main/div[1]/div[1]/div/div/div[2]/a/span/span').text # 나라 읽기
            country.append(countrys)
            print(country)
            print(location)

            clicked_page_html = driver.page_source
            soup = BeautifulSoup(clicked_page_html, 'html.parser')

            # <head> 태그를 찾습니다. # <meta> 태그 중에서 name이 "apple-itunes-app"이고 content에 "app-argument"를 가지는 태그를 찾습니다.
            head_meta_tag = soup.find('head').find('meta', attrs={'name': 'apple-itunes-app', 'content': re.compile(r'app-argument')})
            # content 속성 값을 가져옵니다.
            content_value = head_meta_tag['content']
            # 'app-argument=' 뒤의 URL을 추출합니다.
            addresss = content_value.split('app-argument=')[1]
            address.append(addresss)
            print(address)

            driver.find_element(By.XPATH,'//*[@id="tab-data-qa-reviews-0"]/div/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/button').click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="menu-item-ko"]')))
            driver.find_element(By.XPATH,'//*[@id="menu-item-ko"]').click()
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[1]/div/div/div[3]/a/span')))
            except:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[2]/div/div/div[3]/a/span')))
            for l in range(20):
                for k in range(1,11):
                    #더보기
                    try :
                        driver.find_element(By.XPATH,'//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[{}]/div/div/div[5]/div[2]/button/span'.format(k)).click()
                    except :
                        print("2. error")
                        pass
                    #리뷰1
                    try :
                        review1 = driver.find_element(By.XPATH,'//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[{}]/div/div/div[3]/a/span'.format(k)).text
                    except :
                        try :
                            review1 = driver.find_element(By.XPATH,'//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[{}]/div/div/div[3]/a/span'.format(k+1)).text
                        except:
                            print("2.5 error")
                            continue
                    #리뷰2
                    try :
                        review2 = driver.find_element(By.XPATH,'//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[{}]/div/div/div[5]/div[1]/div/span/span'.format(k)).text
                    except :
                        try:
                            review2 = driver.find_element(By.XPATH,'//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[{}]/div/div/div[5]/div[1]/div/span/span'.format(k+1)).text
                        except:
                            print("3. error")
                            continue
                    review_temp = review1 + " " + review2
                    review.append(review_temp)

                    df_temp = pd.DataFrame({'location': location, 'country': country, 'address': address, 'review': review})
                    df = df.append(df_temp, ignore_index=True)
                    print(review)
                    review=[]
                try:
                    driver.find_element(By.XPATH,'//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[11]/div[1]/div/div[1]/div[2]/div/a').click()
                except:
                    driver.find_element(By.XPATH,
                                        '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[12]/div[1]/div/div[1]/div[2]/div/a').click()
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[1]/div/div/div[3]/a/span')))
                except:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[2]/div/div/div[3]/a/span')))
                # time.sleep(1)
            driver.close()
            time.sleep(0.5)
            driver.switch_to.window(window_handles[0])
            # # 가장 최근에 열린 창 이전의 창 핸들을 선택합니다 (예: 두 번째 창)
            # previous_window_handle = window_handles[-j]  # -1은 최신 창, -2는 그 이전 창
            # # 이전 창으로 전환합니다
            # driver.switch_to.window(previous_window_handle)
        except NoSuchElementException:
            # If the element is not found, simply continue to the next iteration
            print("Element not found - skipping", j)
            continue
        # except:
        #     print("1. error", j)
        #     continue

        print(df)
        df.to_csv("./crawling_data/crawlingdata_{}_8.csv".format('attraction'),index=False)