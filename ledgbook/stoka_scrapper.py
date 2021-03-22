# selenium code
from selenium import webdriver    # 라이브러리에서 사용하는 모듈만 호출
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException    # 태그가 없는 예외 처리
from .models import StockInfo

def stoka_scrap():

    #------------------- 변수 호출 -----------------------------
    stock_info_list = []
    stock_info = {}
    click_flag = True
    #------------------- 크롬 드라이버 호출 -----------------------
    chromedriver = '/Users/leejeonghoon/Desktop/dev/tool/chromeDriver/chromedriver' #크롬드라이버 호출 TODO : 프로퍼티화 필요
    #headless chrome option
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
    options.add_argument('disable-gpu')  # GPU 사용 안함
    options.add_argument('lang=ko_KR')  # 언어 설정
    driver = webdriver.Chrome(chromedriver, options=options)  # 옵션 적용

    #-------------------- 크롤링 대상 도출 -------------------------
    stocks = StockInfo.objects.all().order_by('stock_num')[:500]
    #stocks = StockInfo.objects.all()

    #-------------------- 크롤 및 자료정비 -------------------------
    progression = 0;
    for stock in stocks:

        try:

            print('------------------------------------------------')
            progression += 1
            print(str(progression)+" / "+str(len(stocks)))
            print(stock.stock_name)
            print(stock.stock_num.zfill(6))

            # 네이버모바일 크롤
            url = 'https://m.stock.naver.com/item/main.nhn#/stocks/'+stock.stock_num.zfill(6)+'/total'
            print(url)
            driver.get(url) #가지고옴.

            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'total_list')))

            #토탈리스트 뽑아옴(네이버 모바일 클래스명)
            total_data = driver.find_elements_by_class_name('total_list')
            print(total_data)

            total_list = []
            for k in total_data:
                total_list.append(k.text.split('\n'))

            if "추정PER" not in total_list[0] :
                print("not in!!!!")
                driver.find_element_by_css_selector(
                    "#content_body>div.ct_box.total_infomation._total_quote_summary > div:nth-child(5) > div > a > span").click()
                total_data = driver.find_elements_by_class_name('total_list')
                print(total_data)
                total_list = []
                for k in total_data:
                    total_list.append(k.text.split('\n'))

            else :
                print("in!!!")

            if click_flag == True :
                # 더 보기 클릭
                driver.find_element_by_css_selector("#content_body>div.ct_box.total_infomation._total_quote_summary > div:nth-child(5) > div > a > span").click()
                click_flag = False

            # 토탈 가져오는거 뽑아봄
            for l in total_list:
                print(l)

            stock_name = stock.stock_name
            stock_num = stock.stock_num

            print("시총 : "+total_list[0][13])
            stock_price = total_list[0][13]

            for i in range(len(total_list[0])) :
                if total_list[0][i] == "PER" :
                    print("월기준 : "+total_list[0][i+1])  # 월기준
                    stock_month_date = total_list[0][i+1]
                    print("배율 : " + total_list[0][i+2])  # 배율

                    if total_list[0][i+2] == 'N/A' :
                        stock_per = 'N/A'
                    elif total_list[0][i+2][-1:] == "배" :
                        stock_per = float(total_list[0][i+2][:-1].replace(',',''))
                    else :
                        stock_per = total_list[0][i+2]


                if "추정PER" not in total_list[0] :
                    driver.find_element_by_css_selector(
                        "#content_body>div.ct_box.total_infomation._total_quote_summary > div:nth-child(5) > div > a > span").click()

                if total_list[0][i] == "추정PER":
                    print("추정PER : "+total_list[0][i+1])

                    if total_list[0][i+1] == 'N/A':
                        stock_suspct_per = 'N/A'
                    elif total_list[0][i+1][-1:] == "배" :
                        stock_suspct_per = float(total_list[0][i+1][:-1].replace(',',''))
                    else:
                        stock_suspct_per = total_list[0][i+1]

            stock_info = {
                'stock_name': stock_name # 주식이름
                , 'stock_num' : stock_num # 주식번호
                , 'stock_price': stock_price # 시총
                , 'stock_month_date': stock_month_date  # 월기준
                , 'stock_per': stock_per  # 주당수익률
                , 'stock_suspct_per' : stock_suspct_per #추정PER
            }
            stock_info_list.append(stock_info)
        except TimeoutException:  # 예외 처리

             print('해당 주식정보가 존재하지 않음.')

        finally:
            print('end ----------------------------.')

    driver.quit()

    return stock_info_list