from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

# url: https://www.tripadvisor.co.kr/Attractions-{지역코드}-Activities-{카테고리}-oa{(페이지-1)*30}-{지역}}.html
url1 = 'https://www.tripadvisor.co.kr/Attractions-g4-Activities-{}-oa{}-Europe.html'
catecorys = ['','c61','c58','c36','c62','c26']      # Activities-a_allAttractions.true => ''로 변경 // 명소, 야외활동, 콘서트 및 쇼, 음식/음료, 이벤트, 쇼핑
link_xpath = '/html/body/div[1]/main/div[1]/div/div[{}]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/section[{}]/div/div/div/div/article/div[2]/header/div/div/div/a[{}]'
            # /html/body/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/section[2]/div/div/div/div/article/div[2]/header/div/div/div/a[2]
            # /html/body/div[1]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/section[8]/div/div/div/div/article/div[2]/header/div/div/div/a[2]
location_xpath = '/html/body/div[1]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1'
country_xpath = '/html/body/div[1]/main/div[1]/div[1]/div/div/div[2]/a/span/span'
review_title_xpath  = '/html/body/div[1]/main/div[1]/div[2]/div[2]/div[2]/div/div[1]/section[{}]/div/div/div/section/section/div[1]/div/div[5]/div/div[{}]/div/div/div[3]/a/span'
review_detail_xpath = '/html/body/div[1]/main/div[1]/div[{}]/div[2]/div[2]/div/div[1]/section[{}]/div/div/div/section/section/div[1]/div/div[5]/div/div[{}]/div/div/div[{}]/div[1]/div/span/span'

locations = []
countrys = []
addresss = []
reviews = []

catecory=2     # 콘서트&쇼핑(2,5)
for i in range(0,4):      # 4페이지까지 120개
    print('[ page', i+1,' ]')
    for j in range(2,40):       # 1페이지 - 1~30개 크롤링 / 즐길거리 목록. 1페이지에 30개, xpath: 2~39까지
        url = url1.format(catecorys[catecory], i * 30)
        driver.get(url)
        time.sleep(0.5)
        try:
            link_selector = driver.find_element(By.XPATH, link_xpath.format(3, j, 2))
        except:
            try:
                link_selector = driver.find_element(By.XPATH, link_xpath.format(2, j, 1))
            except:
                print('link_selector error', j)
                continue
        link = link_selector.get_attribute('href')
        # print(link)

        # 장소, 나라, 링크
        driver.get(link)
        time.sleep(0.5)
        location = driver.find_element(By.XPATH, location_xpath).text
        country = driver.find_element(By.XPATH, country_xpath).text
        # print(location, country)
        address = link

        link = link.split('Reviews')
        for page in range(20):  # 20페이지까지 총 200개
            ########### print('review_page:', page)
            review_link = link[0] + 'Reviews-or' + str(page * 10) + link[1]
            # print(review_link)
            driver.get(review_link)
            # time.sleep(0.5)
            for k in range(1, 12):  # 1페이지 10개인데 가끔 2로 시작해서 11로 끝남
                try:
                    try:
                        try:
                            review1 = driver.find_element(By.XPATH, review_title_xpath.format(8, k)).text
                            review2 = driver.find_element(By.XPATH, review_detail_xpath.format(2, 8, k, 5)).text
                        except:
                            try:
                                review1 = driver.find_element(By.XPATH, review_title_xpath.format(8, k)).text
                                review2 = driver.find_element(By.XPATH, review_detail_xpath.format(1, 8, k, 5)).text
                            except:
                                review1 = driver.find_element(By.XPATH, review_title_xpath.format(8, k)).text
                                review2 = driver.find_element(By.XPATH, review_detail_xpath.format(1, 8, k, 4)).text
                    except:
                        try:
                            review1 = driver.find_element(By.XPATH, review_title_xpath.format(7, k)).text
                            review2 = driver.find_element(By.XPATH, review_detail_xpath.format(2, 7, k, 5)).text
                        except:
                            review1 = driver.find_element(By.XPATH, review_title_xpath.format(7, k)).text
                            review2 = driver.find_element(By.XPATH, review_detail_xpath.format(1, 7, k, 5)).text
                except:
                    ########### print("review_error: ",k, review_link)
                    continue
                review = review1 + review2
                # print(k, review)
                reviews.append(re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', review))        ## 변경했으니 다시 돌려 한 번 확인할 것
                locations.append(location)
                countrys.append(country)
                addresss.append(address)

    print("success_crawling_page", i)
    df = pd.DataFrame({'location': locations, 'country': countrys, 'address': addresss, 'review': reviews})     # location, country, address, review
    df.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(catecory,i), index=False)


driver.close()

