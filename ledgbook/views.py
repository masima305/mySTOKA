# selenium code
from django.core import serializers
from django.db.models import FloatField
from django.db.models import Max

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models.functions import Substr, Cast

from django.http import HttpResponse
import simplejson as json
from .forms import PostForm
from .stoka_scrapper import *
from .stoka_insert_tool import *

from datetime import datetime
# Create your views here.

#====================================================================================================
#---------------------------------------------- BASE ------------------------------------------------
#====================================================================================================

# 사이드바 페이지
def sidebar(request):
    return render(request, "ledgbook/ledgbook_list.html")

# 베이스 페이지
def base(request):
    return render(request, 'ledgbook/base.html')

#====================================================================================================
#---------------------------------------------- LEDGBOOK --------------------------------------------
#====================================================================================================


# 개인수익률 설정 변경
def savePersonalSetting_update(request):
    form = json.loads(request.body)

    personalSetting = PersonalSetting.objects.get(user=request.user)
    personalSetting.setting_add_deposit = form['setting_add_deposit']
    personalSetting.setting_change_rate = form['setting_change_rate']
    personalSetting.save()

    context = "수익률 설정이 정상적으로 변경되었습니다."
    return HttpResponse(json.dumps(context), content_type="application/json")

# 수익설계 페이지
def ledgbook_rich(request):

    # 지금 date확인(TODO : 공통묶기 대상)
    now = datetime.now()
    now_year = now.year
    now_month = now.month


    # 리스트 받아오기
    bookmains = LedgbookMain.objects.filter().order_by('id')

    # 마지막 라인의 마감 여부 저장
    if bookmains.count() == 0:
        # 최초 입력이라면
        last_finished_yn = "S" # S for Start
    else:
        if ( int(now_year) > int(bookmains[bookmains.count()-1].year)
                or int(now_month) > int(bookmains[bookmains.count()-1].month)
                and bookmains[bookmains.count() - 1].finished_yn != "Y" ) :
            last_finished_yn = "F" # F for need to finish
        else:
            last_finished_yn = bookmains[bookmains.count() - 1].finished_yn # else = Y or N

    # 새로운 월 정보 등록 시 필요한 것듯
    if bookmains.count() > 0:
        last_prvBalance = bookmains[bookmains.count() - 1].cur_balance
        last_month = int(bookmains[bookmains.count() - 1].month)+1
        last_year = int(bookmains[bookmains.count() - 1].year)
    else :
        last_prvBalance = 0
        last_month = 0
        last_year = 0

    #월이 막월이면 연도 +1, 월 1
    if(last_month>12) :
        last_month = 1
        last_year += 1



    # 개인세팅
    try :
        personalSetting = PersonalSetting.objects.get(user=request.user)
    except Exception :
        personalSetting = []

    # 통계

    # 타임스템프

    # ----- send_data -------

    send_data = {
        'bookmains': bookmains
        , 'last_finished_yn': last_finished_yn
        , 'last_prvBalance' : last_prvBalance
        , 'last_month' : ""
        , 'last_year' : ""
        , 'personalSetting' : personalSetting
        , 'total_year' : last_year
        , 'total_month' : last_month
    }

    if last_finished_yn == "Y":
        send_data['last_month'] = last_month
        send_data['last_year'] = last_year

    return render(request, 'ledgbook/ledgbook_rich.html', send_data)

# 수익현황 신규등록
def saveledg_new(request):
    if request.method == "POST":
    # TODO : 업데이트 시 해당 아이디에 맞는 사람 업데이트 시켜줘야함.
        form = ""
        if request.is_ajax():
            if request.method == 'POST':
                # form = json.loads(request.body.decode("utf-8"))
                form = json.loads(request.body)

                post = LedgbookMain(
                    year=form['year']
                    , month=form['month']
                    , degree=int(form['degree'])
                    , user=request.user
                    , prv_balance=form['prv_balance']
                    , add_deposit=form['add_deposit']
                    , revenue=form['revenue']
                    , change=form['change']
                    , change_rate=form['change_rate']
                    , trgt_add_deposit=form['trgt_add_deposit']
                    , trgt_change_rate=form['trgt_change_rate']
                    , trgt_revenue=form['trgt_revenue']
                    , trgt_cur_balance=form['trgt_cur_balance']
                    , cur_balance=form['cur_balance']
                    , achievement_rate=form['achievement_rate']
                    , finished_yn=form['finished_yn']
                )
                post.save()
                context = "new"
    return HttpResponse(json.dumps(context), content_type="application/json")

# 수익현황 기존 업데이트
def saveledg_update(request):
    if request.method == "POST":
        # TODO : 업데이트 시 해당 아이디에 맞는 사람 업데이트 시켜줘야함.
        form = ""
        if request.is_ajax():
            if request.method == 'POST':
                #form = json.loads(request.body.decode("utf-8"))
                form = json.loads(request.body)


        intdegree = int(form.get('degree'))
        post = LedgbookMain.objects.get(year=form.get('year'), month=form.get('month'), degree=form.get('degree'), user_id=request.user)

        if post:
            post.degree = int(form['degree'])+1
            post.add_deposit = form['add_deposit']
            post.revenue = form['revenue']
            post.change = form['change']
            post.change_rate = form['change_rate']
            post.trgt_add_deposit = form['trgt_add_deposit']
            post.trgt_change_rate = form['trgt_change_rate']
            post.trgt_revenue = form['trgt_revenue']
            post.trgt_cur_balance = form['trgt_cur_balance']
            post.cur_balance = form['cur_balance']
            post.achievement_rate = form['achievement_rate']
            post.finished_yn = form['finished_yn']
            post.save()
        context = "update"
        return HttpResponse(json.dumps(context), content_type="application/json")

def ledgbook_list(request):
    # 키워드 : 쿼리셋에 대한 공부가 필요함.
    # posts = LedgbookPost.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = LedgbookPost.objects.all()
    return render(request, 'ledgbook/ledgbook_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(LedgbookPost, pk=pk)
    return render(request, 'ledgbook/ledgbook_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # 작성자 정보를 추가로 저장하고 커밋해야하기때문에 펄스로 줬음
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('ledgbook_detail', pk=post.pk)
    else:
        form = PostForm
        return render(request, 'ledgbook/post_edit.html', {'form': form})

#====================================================================================================
#---------------------------------------------- STOKA -----------------------------------------------
#====================================================================================================


#---------------------------------------------- pages -----------------------------------------------

# 메인페이지

def stock_stat_cathe(request):

    now = datetime.now().strftime('%Y-%m-%d')

    # 조건1 : 둘다 N/A인거는 판단 가치가 없음.
    stock_info_list = \
        StockDailyInfo.objects.filter(stock_updt = now ).exclude(stock_suspct_per = 'N/A', stock_per = 'N/A')

    stock_info_list = stock_info_list.annotate(stock_per2=Cast('stock_per',FloatField()))\
                       .annotate(stock_suspct_per2=Cast('stock_suspct_per',FloatField()))

    stock_info_list = stock_info_list.order_by('stock_per2','stock_suspct_per2')
    send_data = {
        'stock_info_list' : stock_info_list
    }



    return render(request, 'ledgbook/stoka_stock_stat_cathe.html',send_data)

# 환경설정
def stoka_setting(request):
    cathe_list = StockCathe.objects.filter(user=request.user, use_yn="Y").order_by('cathe_num')
    send_data = {
        'cathe_list': cathe_list
    }
    return render(request, 'ledgbook/stoka_setting.html',send_data)

# 주식들의 싱크를 맞춰서 DB에 저장해준다.
def resync_stocks(request):

    #주식 상장사 목록 가져오기( 리쿼스트로 가지고 옴)
    tool_stock_insert_request()

    context = "새로고침이 완료되었습니다."

    stock_info_list = stoka_scrap()
    StockDailyInfo.objects.all().delete()

    now = datetime.now().strftime('%Y-%m-%d')
    print(now)  # 형식 2015-04-19

    # 일부러 한개씩 업데이트를 친다.
    for stock in stock_info_list:

        saved_stock_info = StockDailyInfo.objects.filter(stock_num=stock["stock_num"], stock_updt=now)
        if saved_stock_info:
            for tmp_info in saved_stock_info:
                tmp_info.stock_name = stock["stock_name"]              # 주식이름
                tmp_info.stock_price = stock["stock_price"]             # 주식가격
                tmp_info.stock_month_date = stock["stock_month_date"]   # per 기준일
                tmp_info.stock_per = stock["stock_per"]                 # PER
                tmp_info.stock_suspct_per = stock["stock_suspct_per"]   # 추정 PER
                tmp_info.last_updt = datetime.now()                     # 추정 PER
                tmp_info.save()
        else:
            saved_stock_info = StockDailyInfo(
                  stock_name = stock["stock_name"]              # 주식이름
                , stock_num = stock["stock_num"]                # 종목번호
                , stock_price = stock["stock_price"]            # 주식가격
                , stock_month_date = stock["stock_month_date"]  # per 기준일
                , stock_per = stock["stock_per"]                # per 기준일
                , stock_suspct_per = stock["stock_suspct_per"]  # 추정 PER
                , stock_updt = now
                , last_updt = datetime.now()                    # 최근 업데이트
            )

            saved_stock_info.save()
    return HttpResponse(json.dumps(context), content_type="application/json")


#---------------------------------------------- ajax -----------------------------------------------
# 주식검색
def sch_stock_list(request) :
    if request.method == "POST":
        if request.is_ajax():
            form = json.loads(request.body.decode("utf-8"))
            saved_stock_info = StockInfo.objects.filter(stock_name__icontains=form["sch_stock_nm"])
            stock_list = serializers.serialize('json',saved_stock_info)
    return HttpResponse(stock_list, content_type="application/json")

# 카테고리 추가
def add_cathe(request) :
    if request.method == 'POST':
        form = json.loads(request.body.decode("utf-8"))
        user = request.user

        cathe_info = StockCathe.objects.filter(user = user)
        if cathe_info.count() == 0 :
            max_cathe_num = 0
        else :
            max_cathe_num = cathe_info.aggregate(Max('cathe_num'))['cathe_num__max']+1


        cathe_info = StockCathe(
            cathe_name = form["cathe_name"]
            , cathe_num = max_cathe_num
            , cathe_keyword = form["cathe_keyword"]
            , user = request.user
        )
        context = "등록이 완료되었음"
        cathe_info.save()

    return HttpResponse(json.dumps(context), content_type="application/json")

# 카테고리 삭제
def delete_cathe(request) :
    if request.method == 'POST':
        form = json.loads(request.body.decode("utf-8"))
        user = request.user
        cathe_name = form["cathe_name"]
        cathe_num = form["cathe_num"]

        cathe_info = StockCathe.objects.filter(user = user, cathe_num = cathe_num, cathe_name = cathe_name)

        for cathe in cathe_info :
            cathe.use_yn = "N"
            cathe.save()
        context = "삭제가 완료되었음"
    return HttpResponse(json.dumps(context), content_type="application/json")

# 카테고리 수정
def update_cathe(request) :
    if request.method == 'POST':
        form = json.loads(request.body.decode("utf-8"))
        user = request.user
        cathe_num = form["cathe_num"]

        cathe_info = StockCathe.objects.get(user = user, cathe_num = cathe_num)

        cathe_info.cathe_name = form["cathe_name"]
        cathe_info.cathe_keyword = form["cathe_keyword"]
        cathe_info.save()

        context = "수정완료"
    return HttpResponse(json.dumps(context), content_type="application/json")

# 카테고리에 주식 추가
def add_stock_cathe(request) :
    if request.method == 'POST':
        form = json.loads(request.body.decode("utf-8"))
        stock_num = form["stock_num"]
        stock_name = form["stock_name"]
        cathe_num = form["cathe_num"]
        user = request.user

        stock_cathe_info = StockCatheCd.objects.filter(cathe_num = cathe_num , stock_num = stock_num, user= user)

        if stock_cathe_info:
            context = "이미 해당 주식이 등록되어있습니다."
        else:
            stock_cathe_info = StockCatheCd(
                cathe_num=cathe_num  # 카테고리번호
                , stock_num=stock_num  # 종목번호
                , stock_name = stock_name #종목명
                , user=user  # 사용자

            )
            context = "등록이 완료되었음"
            stock_cathe_info.save()

    return HttpResponse(json.dumps(context), content_type="application/json")

# 카테고리에 주식 삭제
def delete_stock_cathe(request):
    context = "삭제호출"
    if request.method == 'POST':
        form = json.loads(request.body.decode("utf-8"))
        stock_num = form["stock_num"]
        cathe_num = form["cathe_num"]

        user = request.user

        stock_cathe_info = StockCatheCd.objects.get(cathe_num = cathe_num , stock_num = stock_num, user= user)
        stock_cathe_info.delete()
    return HttpResponse(json.dumps(context), content_type="application/json")

# 카테고리에 주식 불러오기
def reload_cathe_stocks(request):
    if request.method == 'POST':
        form = json.loads(request.body.decode("utf-8"))
        cathe_num = form["cathe_num"]
        user = request.user

        cathe_stocks = StockCatheCd.objects.filter(cathe_num=cathe_num, user=user)
        cathe_stocks = serializers.serialize('json', cathe_stocks)
    return HttpResponse(cathe_stocks, content_type="application/json")


