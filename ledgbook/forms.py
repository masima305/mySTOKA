from django import forms
from .models import LedgbookPost
from .models import LedgbookMain

class PostForm(forms.ModelForm):

    class Meta:
        model = LedgbookPost
        fields = ('title','text')

class LedgbookMainForm(forms.ModelForm):
    class Meta:
        model = LedgbookMain
        fields = (
            'user'
            , 'year'
            , 'month'
            , 'degree'
            , 'prv_balance'
            , 'add_deposit'
            , 'revenue'
            , 'change'
            , 'change_rate'
            , 'trgt_add_deposit'
            , 'trgt_change_rate'
            , 'trgt_revenue'
            , 'trgt_cur_balance'
            , 'cur_balance'
            , 'invst_balance'
            , 'finished_yn'
            , 'achievement_rate'
        )