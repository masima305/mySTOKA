from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class LedgbookPost(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# 개인세팅
class PersonalSetting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)      # 사용자정보
    user_auth_grade = models.CharField(max_length=4 , default="0000")                 # 사용자정보
    user_mac_addr = models.CharField(max_length=4, default="0000")                    # 사용자 맥 주소
    setting_add_deposit = models.CharField(max_length=1000)                           # 목표 추가입금
    setting_change_rate = models.FloatField(blank=True, null=True)                    # 목표 증감율
    sync_pos_cnt = models.IntegerField(default=0)                                     # 추적가능 카운트수


# 장부 메인
class LedgbookMain(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    year = models.CharField(max_length=10)                               # 연도
    month = models.CharField(max_length=6)                               # 월
    degree = models.IntegerField(blank=True, null=True)                  # 차수
    prv_balance = models.IntegerField(blank=True, null=True)             # 이전잔고
    add_deposit = models.IntegerField(blank=True, null=True)             # 추가입금
    revenue = models.IntegerField(blank=True, null=True)                 # 수익
    change = models.IntegerField(blank=True, null=True)                  # 증감
    change_rate = models.FloatField(blank=True, null=True)               # 증감율
    trgt_add_deposit = models.IntegerField(blank=True, null=True)        # 목표 추가입금
    trgt_change_rate = models.FloatField(blank=True, null=True)          # 목표 증감율
    trgt_revenue = models.IntegerField(blank=True, null=True)            # 목표 수익
    trgt_cur_balance = models.IntegerField(blank=True, null=True)        # 목표 잔고
    cur_balance = models.IntegerField(blank=True, null=True)             # 현황금액
    invst_balance = models.IntegerField(blank=True, null=True)           # 투자액
    qtr_growth = models.FloatField(blank=True, null=True)                # 분기별 성장률
    finished_yn = models.CharField(max_length=2 ,blank=True, null=True)  # 마감여부
    achievement_rate = models.CharField(max_length=6, null=True)         # 달성률

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    #def __str__(self): #자바에서 toString();
    #    return self.

#------------- STOKA MODEL ------------------

# 종목정보(종목 고유정보) 모델 //
class StockInfo(models.Model):

    stock_name = models.CharField(max_length=20,blank=False, null=False)                # 회사명
    stock_num = models.CharField(max_length=6,blank=False, null=False)                  # 종목코드
    stock_sectors = models.CharField(max_length=80,blank=True, null=True)               # 업종
    staple_item = models.CharField(max_length=300, blank=True, null=True)               # 주요제품
    listing_date = models.CharField(max_length=12, blank=True, null=True)               # 상장일
    closing_date = models.CharField(max_length=12, blank=True, null=True)               # 결산월역
    stock_owner = models.CharField(max_length=80, blank=True, null=True)                # 대표자명
    hompage_addr = models.CharField(max_length=80, blank=True, null=True)               # 홈페이지 주소
    location_addr = models.CharField(max_length=80, blank=True, null=True)              # 지역
    sync_cnt = models.CharField(max_length=10000, blank=False, null=False, default="0") # 싱크 수

    def publish(self):
        self.save()

#종목정보 일자별 정보
class StockDailyInfo(models.Model):
    stock_name = models.CharField(max_length=18, blank=False, null=False, default="---")  # 종목명
    stock_num = models.CharField(max_length=6,blank=False, null=False)                    # 종목번호
    stock_price = models.CharField(max_length=50,blank=True, null=False)                  # 주식가격
    stock_month_date = models.CharField(max_length=30,blank=False, null=False)            # per 기준일
    stock_per = models.CharField(max_length=30,blank=False, null=False)                   # per 기준일
    stock_suspct_per = models.CharField(max_length=30,blank=False, null=False)            # 추정 PER
    stock_updt = models.CharField(max_length=10 ,blank=True, null=True)                   # 수집일자
    last_updt = models.DateTimeField(blank=True, null=True)                               # 최근 업데이트

# 카테고리 내의 종류
class StockCatheCd(models.Model):
    cathe_num = models.IntegerField(blank=False, null=False, default=0)   # 카테고리번호
    stock_num = models.CharField(max_length=6,  blank=False, null=False, default="000")   # 종목번호
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)          # 사용자정보
    description = models.CharField(max_length=6,  blank=False, null=False, default="000") # 카테고리 메모
    sync_yn = models.CharField(max_length=2,  blank=False, null=False, default="N")       # 종목가격 추적 YN


# 카테고리 정보
class StockCathe(models.Model):
    cathe_name = models.CharField(max_length=20, blank=False, null=False, default="---")    # 카테고리 이름
    cathe_num =  models.IntegerField(blank=False, null=False, default=0)                                  # 카테고리 번호
    cathe_keyword = models.CharField(max_length=20, blank=True, null=True)                  # 카테고리 키워드
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)            # 사용자정보
    use_yn = models.CharField(max_length=2, blank=True, null=True, default='Y')             # 사용여부

# 마이그레이션 파일 생성
#$ python manage.py makemigrations ledgbook

# 마이그레이션 적용
#$ python manage.py migrate ledgbook

# 마이그레이션 적용 현황
#$ python manage.py showmigrations ledgbook

# 지정 마이그레이션의 SQL 내역
#python manage.py sqlmigrate <app-name> <migration-name>
