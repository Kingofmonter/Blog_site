from django import template
from blog import models
from django.db.models import Count

register = template.Library()


@register.inclusion_tag("classification.html")
def get_classification_style(username):

    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog

    # 当前站点分类名称对应的文章数
    cate_list = models.Category.objects.filter(blog=blog).values('pk').annotate(c=Count("article__title")).values_list(
        "title", "c")

    # 当前站点标签名称对应的文章数
    tag_list = models.Tag.objects.filter(blog=blog).values('pk').annotate(c=Count("article")).values_list("title", "c")

    # 当前站点日期对应的文章数
    date_list = models.Article.objects.filter(user=user).extra(
        select={"y_m_d_data": "strftime('%%Y-%%m',create_time)"}).values('y_m_d_data').annotate(
        c=Count("nid")).values_list("y_m_d_data", "c")

    return {"blog": blog, "cate_list": cate_list, "tag_list": tag_list, "date_list": date_list, "user": user}
