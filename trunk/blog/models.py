#coding=utf-8
from django.db import models
from datetime import datetime
from django.utils import encoding
from django.utils.http import urlquote
#文章类型选项
POST_TYPES = (    
    ('post', '文章'),
    ('page', '页面'),
    )
#文章状态选项
POST_STATUS = (   
    ('publish', '已发布'),
    ('draft', '草稿'),
    ('private', '私人'),
)
#评论审核状态
COMMENT_APPROVE_STATUS = (
    (0,'未审核'),
    (1,'审核通过'),
    ('spam','垃圾评论')
)
    
class Category(models.Model):
    '''category entity'''    
    name = models.CharField('类别名',maxlength=255,unique=True)
    desc = models.CharField('类别描述',maxlength=1024)
    enname = models.CharField('类别英文名',maxlength=255,unique=True,blank=True,help_text='作为url路径')
    def save(self):
        #override save
        if not self.enname:
            self.enname = encoding.iri_to_uri(self.name)
        super(Post,self).save()
    def __unicode__(self):
        return self.name
    #def __str__(self):
    #    return self.name
    
    def get_absolute_url(self):
        if self.enname:
            return '/category/%s/' % self.enname
        else:
            return '/category/%i/' % self.id
    
    class Meta:
        ordering=['name']
        verbose_name='分类'
        verbose_name_plural = '分类列表'
    
    class Admin:
        list_display = ('name','desc')
        search_fields = ['name']

class Author(models.Model):
    '''
    Blog Author Entity
    '''
    name = models.CharField('用户名',maxlength=255,unique=True)
    password = models.CharField('密码',maxlength=64)
    email = models.EmailField('Email')
    
class Post(models.Model):    
    '''Post Entity'''
    title = models.CharField('标题',maxlength=255)
    content = models.TextField('内容')
    category = models.ManyToManyField(Category,verbose_name='分类')
    post_name = models.CharField('文章缩略名',maxlength=255,unique=True,blank=True,help_text='作为文章url路径,勿使用中文,不填则使用url编码后的文章标题')
    post_type = models.CharField('类型',maxlength=10,default='post',choices=POST_TYPES)
    post_status = models.CharField('文章状态',maxlength=10,default='publish',choices = POST_STATUS)
    post_parent = models.ForeignKey('self',null=True, blank=True,related_name='child_set',verbose_name='上级页面')
    pubdate = models.DateTimeField('发布时间',auto_now_add=True,editable=False)
    hits = models.IntegerField('点击数',default=0,editable=False)
    menu_order = models.IntegerField('菜单排序',default=0)
    
    def save(self):
        #override save
        if not self.post_name:
            self.post_name = encoding.iri_to_uri(self.title)
        super(Post,self).save()
    
    def __unicode__(self):
        return self.title
    #def __str__(self):
    #    return self.title
    def get_absolute_url(self):        
        if self.post_name:
            return '/%d/%d/%d/%s/' % (self.pubdate.year,self.pubdate.month,self.pubdate.day,self.post_name)
        else:
            return '/%d/%d/%d/%i/' % (self.pubdate.year,self.pubdate.month,self.pubdate.day,self.id)
    def get_page_url(self):
        '''if post is page,get the page url link'''
        if str(self.post_name).find('http://')==0:
            #if is a http:// url
            return self.post_name
        else:
            return '/%s/' % urlquote(self.post_name)
    def get_cat_str(self):
        '''返回文章类别名列表，用逗号分隔'''
        cats = self.category.all()
        cat_strs = ''
        for cat in cats:
            if len(cat_strs)>0:
                cat_strs += ','
            cat_strs += cat.name
        return cat_strs
    get_cat_str.short_description = '文章类别'
    
    
    
    class Meta:
        ordering = ['-pubdate']
        verbose_name='文章'
        verbose_name_plural = '文章列表'

    class Admin:
        list_display = ('title','get_cat_str','pubdate','hits')
        search_fields = ['title']

class Comments(models.Model):
    '''user comments'''
    post = models.ForeignKey(Post,verbose_name='文章')
    comment_author = models.CharField('作者名',max_length=32)
    comment_author_email = models.EmailField(verbose_name='Email')
    comment_author_url = models.URLField('网址',verify_exists=False)
    comment_author_IP = models.IPAddressField(verbose_name='IP',null=True,editable=False)
    comment_date = models.DateTimeField(verbose_name='发表时间',auto_now_add=True,editable=False)
    comment_content = models.TextField(verbose_name='评论内容')
    comment_approved = models.CharField('审核状态',max_length=32,choices=COMMENT_APPROVE_STATUS)
    comment_agent = models.CharField('用户浏览器信息',editable=False,max_length=255,null=True)
    user_id = models.IntegerField('用户id',editable=False,null=True)
    
    def __unicode__(self):
        return self.comment_author
   
    def get_absolute_url(self):        
        if self.post.post_name:
            return '/%d/%d/%d/%s/#comment' % (self.post.pubdate.year,self.post.pubdate.month,self.post.pubdate.day,self.post_name)
        else:
            return '/%d/%d/%d/%i/' % (self.post.pubdate.year,self.post.pubdate.month,self.post.pubdate.day,self.id)
    
    class Meta:
        ordering = ['-comment_date']
        verbose_name='评论'
        verbose_name_plural = '评论'

    class Admin:
        #list_display = ('title','get_cat_str','pubdate','hits')
        search_fields = ['comment_author']
