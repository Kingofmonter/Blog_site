from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.http import JsonResponse
from PIL import Image,ImageDraw,ImageFont
import random
from io import BytesIO


def login(request):

    if request.method == 'POST':
        user = request.POST.get("user")
        pwd =request.POST.get("pwd")
        view_

    return render(request,'login.html')



def get_view_code_img(request):

    def get_img_color():
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    img=Image.new("RGB",(150,35),color=get_img_color())
    darw =ImageDraw.Draw(img)
    word_font = ImageFont.truetype('static/font/word_font.otf',size=28)

    view_code_str = ""
    for i in range(5):

        random_num = str(random.randint(0,9))
        random_low_alpha = chr(random.randint(95,122))
        random_upper_alpha = chr(random.randint(65,90))
        random_char = random.choice([random_num,random_low_alpha,random_upper_alpha])

        darw.text((i*20+50,5),random_upper_alpha,get_img_color(),font=word_font)

        view_code_str += random_char

    width = 150
    height = 35

    for i in range(6):
        x1 = random.randint(0,width)
        y1 = random.randint(0,height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        darw.line((x1,y1,x2,y2),fill=get_img_color())

    for i in range(100):
        darw.point([random.randint(0,width),random.randint(0,height)],fill=get_img_color())
        x = random.randint(0,width)
        y = random.randint(0,height)
        darw.arc((x,y,x+4,y+4),0,90,fill=get_img_color())


    f = BytesIO()
    img.save(f,"png")
    data = f.getvalue()


    return HttpResponse(data)