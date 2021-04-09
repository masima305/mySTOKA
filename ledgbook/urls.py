from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # 작업중인 페이지
    # 설정 페이지 작업중
    path('', views.stoka_setting, name='stoka_setting')

    # 페이지 조회 관련 url
    , path('ledgbooklist', views.ledgbook_list, name='ledgbook_list')
    , path('ledgbook/<int:pk>/', views.post_detail, name='post_detail')
    , path('post/new', views.post_new, name='post_new')

    #수익률설계
    , path('ledgbook_rich', views.ledgbook_rich, name='ledgbook_rich')

    # 저장 관련 url
    , path('saveledg/new', views.saveledg_new, name='saveledg_new')
    , path('saveledg/update', views.saveledg_update, name='saveledg_update')
    , path('savePersonalSetting/update', views.savePersonalSetting_update, name='savePersonalSetting_update')


    #-stoka

    #--페이지
    #---메인페이지
    #, path('stoka/main', views.stoka_main, name='stoka_main')

    , path('stoka/stock_stat_cathe', views.stock_stat_cathe, name='stock_stat_cathe')

    #--AJAX call
    #주식 현황 싱크
    , path('stoka/resync', views.resync_stocks, name='resync_stocks')

    #주식 리스트 확인
    , path('stoka/sch_stock_list', views.sch_stock_list  ,name='sch_stock_list')

    #카테고리에 주식 추가
    , path('stoka/add_stock_cathe', views.add_stock_cathe, name='add_stock_cathe')

    #카테고리에 주식 삭제
    , path('stoka/delete_stock_cathe', views.delete_stock_cathe, name='delete_stock_cathe')

    #카테고리 추가
    , path('stoka/add_cathe', views.add_cathe, name='add_cathe')

    #카테고리 삭제
    , path('stoka/delete_cathe', views.delete_cathe, name='delete_cathe')

    #카테고리 수정
    , path('stoka/update_cathe', views.update_cathe, name='update_cathe')

    #카테고리별 주식 목록 불러오기
    , path('stoka/reload_cathe_stocks', views.reload_cathe_stocks, name='reload_cathe_stocks')

]
