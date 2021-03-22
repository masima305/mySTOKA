import pandas as pd
import ssl as ssl
import urllib as urllib
from .models import *

def tool_stock_insert_request():
    # excel 파일을 다운로드하는거와 동시에 pandas에 load하기

    # SSL통신 통과를 위한 조치 2021-03-22
    requests = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(requests, context=context)

    df = pd.read_html(response)[0]
    #df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

    df2 = df[['회사명', '종목코드', '업종', '주요제품', '상장일', '결산월', '대표자명', '홈페이지', '지역']].to_dict('records')
    StockInfo.objects.all().delete()

    for stock in df2:
        # 종목코드 확인
        stock_info = StockInfo(
            stock_name=str(stock['회사명']).strip()
            , stock_num=str(stock['종목코드']).strip()
            , stock_sectors=str(stock['업종']).strip()
            , staple_item=str(stock['주요제품']).strip()
            , listing_date=str(stock['상장일']).strip()
            , closing_date=str(stock['결산월']).strip()
            , stock_owner=str(stock['대표자명']).strip()
            , hompage_addr=str(stock['홈페이지']).strip()
            , location_addr=str(stock['지역']).strip()
        )
        stock_info.save()

    return; #TODO 리턴값 valchk 모듈 만들어서 정리


#old. 더이상 쓰지않는다.
def tool_stock_insert_file():
    flag =0;

    print("--------")

    dfSPY = pd.read_csv(filepath_or_buffer="ledgbook/static/assets/insrtData/testInsert.csv",sep=",")


    # dfSPY = pd.read_csv(filepath_or_buffer="ledgbook/static/assets/insrtData/testInsert.csv"
    #                     , index_col="stock_name"
    #                     , usecols=[
    #                         'stock_name'    # 회사명
    #                         , 'stock_num'     # 종목코드
    #                         , 'stock_sectors' # 업종
    #                         , 'staple_item'   # 주요제품
    #                         , 'listing_date'  # 상장일
    #                         , 'closing_date'  # 결산월역
    #                         , 'stock_owner'   # 대표자명
    #                         , 'hompage_addr'  # 홈페이지 주소
    #                         , 'location_addr' # 지
    #                       ]
    #                     )

    df2 = dfSPY[['회사명', '종목코드', '업종', '주요제품', '상장일', '결산월', '대표자명', '홈페이지', '지역']].to_dict('records')
    StockInfo.objects.all().delete()
    for dff in df2:
        #종목코드 확인
        stock_info = StockInfo(
              stock_name = str(dff['회사명']).strip()
            , stock_num = str(dff['종목코드']).strip()
            , stock_sectors = str(dff['업종']).strip()
            , staple_item = str(dff['주요제품']).strip()
            , listing_date = str(dff['상장일']).strip()
            , closing_date = str(dff['결산월']).strip()
            , stock_owner = str(dff['대표자명']).strip()
            , hompage_addr = str(dff['홈페이지']).strip()
            , location_addr = str(dff['지역']).strip()
        )
        stock_info.save()
    return flag