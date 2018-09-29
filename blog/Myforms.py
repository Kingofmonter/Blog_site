from django import forms
from django.forms import widgets
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

#注册提交对象
class UserForm(forms.Form):
    user = forms.CharField(max_length=32,
                           widget=widgets.TextInput(attrs={"class":"form-control"}),
                           label="用户名",
                           error_messages={"required":"用户名不能为空"})
    pwd = forms.CharField(max_length=32,
                          widget=widgets.PasswordInput(attrs={"class":"form-control"}),
                          label="密码")
    re_pwd = forms.CharField(max_length=32,
                             widget=widgets.PasswordInput(attrs={"class":"form-control"}),
                             label="确认密码")
    email = forms.EmailField(max_length=32,
                             widget=widgets.EmailInput(attrs={"class":"form-control"}),
                             label="邮箱地址",
                             error_messages={"required": "邮箱不能为空"})

    def clean_user(self):
        val = self.cleaned_data.get("user")

        user = UserInfo.objects.filter(username=val).first()

        if not user:
            return val

        else:
            raise ValidationError("该用户已注册")

    def clean(self):

        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")

        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data

            else:
                raise ValidationError("两次密码输入不一致")
        else:
            return self.cleaned_data