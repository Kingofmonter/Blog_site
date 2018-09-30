from django.shortcuts import render, HttpResponse
from django.contrib import auth
from django.http import JsonResponse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from .Myforms import *
import random


# 登陆
def login(request):
    if request.method == 'POST':

        response = {"user": None, "msg": None}

        #接收数据
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        view_code = str(request.POST.get("view_code"))
        view_code_str = request.session.get("view_code_str")


        if view_code.upper() == view_code_str.upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)  # requset.user = 当前登陆对象
                response["user"] = user.username
            else:
                response["msg"] = "username or password is error!"

        else:
            response["msg"] = "valid code error"

        return JsonResponse(response)

    return render(request, 'login.html')


# 验证码
def get_view_code_img(request):
    def get_img_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    img = Image.new("RGB", (150, 35), color=get_img_color())
    darw = ImageDraw.Draw(img)
    word_font = ImageFont.truetype('static/font/word_font.otf', size=28)

    view_code_str = ""
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])

        darw.text((i * 20 + 50, 5), random_char, get_img_color(), font=word_font)

        view_code_str += random_char


    # width = 150
    # height = 35

    # 噪点和干扰线
    # for i in range(6):
    #     x1 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     x2 = random.randint(0, width)
    #     y2 = random.randint(0, height)
    #     darw.line((x1, y1, x2, y2), fill=get_img_color())
    #
    # for i in range(100):
    #     darw.point([random.randint(0, width), random.randint(0, height)], fill=get_img_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     darw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_img_color())

    request.session['view_code_str'] = view_code_str

    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()

    return HttpResponse(data)


# 注册
def register(request):
    if request.is_ajax():

        form = UserForm(request.POST)
        response = {"user": None, "msg": None}

        if form.is_valid():
            response["user"] = form.cleaned_data.get("user")

            # 生成用户记录
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avator = request.FILES.get("avator")

            extra = {}
            if avator:
                extra["avator"] = avator

            UserInfo.objects.create(username=user, password=pwd, email=email, **extra)

        else:
            print(form.errors)
            response["msg"] = form.errors

        return JsonResponse(response)

    form = UserForm()

    return render(request, 'register.html', {"form": form})



def index(request):

    return render(request,'index.html')
