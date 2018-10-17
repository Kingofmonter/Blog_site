from django.shortcuts import render, HttpResponse, redirect
from django.db.models.functions import TruncMonth
from django.contrib import auth
from django.http import JsonResponse
from django.db.models import Count,F
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from .Myforms import *
from . import models
import random
import json


# 登陆
def login(request):
    if request.method == 'POST':

        response = {"user": None, "msg": None}

        username = request.POST.get("user")
        password = request.POST.get("pwd")
        view_code = str(request.POST.get("view_code"))
        view_code_str = request.session.get("view_code_str")

        if view_code.upper() == view_code_str.upper():
            user = auth.authenticate(username=username, password=password)
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

    # 干扰线，噪点

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

            UserInfo.objects.create_user(username=user, password=pwd, email=email, **extra)

        else:
            print(form.errors)
            response["msg"] = form.errors

        return JsonResponse(response)

    form = UserForm()

    return render(request, 'register.html', {"form": form})


# 首页
def index(requset):
    article_list = models.Article.objects.all()

    return render(requset, 'index.html', {"article_list": article_list})


# 注销
def logout(request):
    auth.logout(request)

    return redirect('/login/')


# 个人站点视图
def home_site(request, username, **kwargs):
    user = UserInfo.objects.filter(username=username).first()

    # 判断用户存在
    if not user:
        return render(request, 'not_found.html')

    # 当前站点所有文章
    article_list = models.Article.objects.filter(user=user)

    if kwargs:

        condition = kwargs.get("condition")
        param = kwargs.get("param")

        if condition == "category":
            article_list = models.Article.objects.filter(user=user).filter(category__title=param)
        elif condition == "tag":
            article_list = models.Article.objects.filter(user=user).filter(tags__title=param)
        else:
            year, month = param.split('-')
            article_list = models.Article.objects.filter(user=user).filter(create_time__year=year,
                                                                           create_time__month=month)

    # 查询站点对象
    blog = user.blog

    # 分类名称对应的文章数
    ret = models.Category.objects.values('pk').annotate(c=Count("article__title")).values("title", "c")

    return render(request, "home_site.html",
                  {"blog": blog, "user": user, "article_list": article_list, "ret": ret, "username": username})


# 文章详情
def article_detail(request, username, article_id):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog

    article_obj = models.Article.objects.filter(pk=article_id).first()
    comment_list = models.Comment.objects.filter(article_id=article_id)

    return render(request, "article_detail.html", locals())


# 点赞
def digg(request):

    article_id = request.POST.get("article_id")
    is_up = json.loads(request.POST.get("is_up"))
    user_id = request.user.pk

    print(is_up)

    user = models.ArticleUpDown.objects.filter(article_id=article_id,user_id=user_id).first()

    response={"state":True}
    if not user:

        models.ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)

        if is_up:
            models.Article.objects.filter(nid=article_id).update(up_count=F("up_count")+1)
        else:
            models.Article.objects.filter(nid=article_id).update(down_count=F("down_count")+1)

    else:
        response["state"] = False
        response["handle"] = user.is_up

    return JsonResponse(response)



#评论
def comment(request):

   print(request.POST)

   user_id = request.user.pk
   article_id = request.POST.get("article_id")
   pid = request.POST.get("pid")
   content = request.POST.get("content")

   comment = models.Comment.objects.create(article_id=article_id,user_id=user_id,parent_comment_id=pid,content=content)

   response = {}
   response["create_time"] = comment.create_time.strftime("%Y-%m-%d %X")
   response["username"] = comment.user.username
   response["content"] = comment.content

   return JsonResponse(response)
