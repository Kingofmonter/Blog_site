from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    '''用户信息'''

    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11,null=True)
    avatar = models.FileField(upload_to='avatar/',default=True) #用户头像 upload_to:储存文件
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    blog = models.OneToOneField(to='Blog',to_field='nid',null=True,on_delete=models.CASCADE)

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
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE)

    def __str__(self):

        return self.title


class Tag(models.Model):
    '''标签'''

    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE)

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

    user = models.ForeignKey(verbose_name='作者',to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    category = models.ForeignKey(to='Category',to_field='nid',null=True,on_delete=models.CASCADE)
    tags = models.ManyToManyField(to='Tag',through='ArticletoTag',through_fields=('article','tag'))

    content = models.TextField()

    def __str__(self):

        return self.title


class ArticletoTag(models.Model):

    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章',to='Article',to_field='nid',on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签',to='Tag',to_field='nid',on_delete=models.CASCADE)

    class Meta:

        unique_together = [
            ('article','tag'),
        ]

    def __str__(self):

        v = self.article.title + "---" +self.tag.title

        return v


class ArticleUpDown(models.Model):
    '''点赞'''

    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo',null=True,on_delete=models.CASCADE)
    article = models.ForeignKey(to='Article',null=True,on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:

        unique_together = [
            ('article','user'),
        ]


class Comment(models.Model):
    '''评论表'''

    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to='Article',to_field='nid',verbose_name='评论文章',on_delete=models.CASCADE)
    user = models.ForeignKey(to='UserInfo',to_field='nid',verbose_name='评论者',on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评论内容',max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    parent_comment = models.ForeignKey(to='self',null=True,on_delete=models.CASCADE)

    def __str__(self):

        return self.content
