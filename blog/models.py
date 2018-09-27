from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser

# Create your models here.


class UserInfo(AbstractBaseUser):
    '''用户信息'''

    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11,null=True)
    avatar = models.FileField(upload_to='avatar/',default=True) #用户头像 upload_to:储存文件
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    blog = models.OneToOneField(to='Blog',to_field='nid',null=True)

    def __str__(self):

        return self.username


class Blog(models.Model):
    '''博客信息（站点）'''

    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题',max_length=64)
    site_time = models.CharField(verbose_name='站点名称',max_length=64)
    theme = models.CharField(verbose_name='博客主题',max_length=64)

    def __str__(self):

        return self.title


class Category(models.Model):
    '''博客个人文章分类'''

    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid')

    def __str__(self):

        return self.title


class Tag(models.Model):
    '''标签'''

    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid')

    def __str__(self):

        return self.title


class Article(models.Model):
    '''文章表'''

    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64,verbose_name='文章标题')
    desc = models.CharField(max_length=255,verbose_name='文章简述')
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    user = models.ForeignKey(verbose_name='作者',to='UserInfo',to_field='nid')
    category = models.ForeignKey(to='Category',to_field='nid',null=True)
    tags = models.ManyToManyField(to='Tag',through='ArticletoTag',through_fields=('article','tag'))

    content = models.TextField()

    def __str__(self):

        return self.title