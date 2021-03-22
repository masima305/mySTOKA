from django.contrib import admin
from .models import *


admin.site.register(LedgbookPost)
admin.site.register(LedgbookMain)
admin.site.register(PersonalSetting)
admin.site.register(StockInfo)
admin.site.register(StockCathe)
admin.site.register(StockDailyInfo)
admin.site.register(StockCatheCd)

#python manage.py createsuperuser
#admin :  ledgbookadm
#passs : yt9954yr!
# Register your models here.
