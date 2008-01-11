#coding=utf-8
from django.db import models
from datetime import datetime
from django.utils import encoding
from django.utils.http import urlquote
import django.utils.html
from pylogs.utils import html
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
#文章允许评论状态
POST_COMMENT_STATUS = (
    ('open','允许评论'),
    ('closed','不允许评论'),
    ('registered','只允许注册用户评论')
)
class Tags(models.Model):
    '''Tag entity'''
    name = models.CharField('标签',unique=True,max_length=64)
    slug = models.CharField('标签缩略名',max_length=255,unique=True,blank=True,help_text='作为友好url')
    reference_count = models.IntegerField('被引用次数',default=0,editable=False)
    
    def save(self):
        #override save
        if not self.slug:
            #replace the special char of name as slug
            self.slug = self.name.replace(' ','-')
            self.slug = self.slug.replace(u'　','-')
            self.slug = self.slug.replace('.','')
            self.slug = encoding.iri_to_uri(self.slug)
        super(Tags,self).save()
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self): 
        return '/tags/%s/' % self.slug      
    
    class Meta:
        #ordering = ['-pubdate']
        verbose_name='标签'
        verbose_name_plural = '标签'

    class Admin:
        list_display = ('name','slug','reference_count')
        search_fields = ['name']
        #list_filter =('post_type','category')
        
class Category(models.Model):
    '''category entity'''    
    name = models.CharField('类别名',max_length=255,unique=True)
    desc = models.CharField('类别描述',max_length=1024)
    enname = models.CharField('类别英文名',max_length=255,unique=True,blank=True,help_text='作为url路径')
    def save(self):
        #override save
        if not self.enname:
            self.enname = encoding.iri_to_uri(self.name)
        super(Category,self).save()
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
        verbose_name_plural = '分类'
    
    class Admin:
        list_display = ('name','desc')
        search_fields = ['name']

class Author(models.Model):
    '''
    Blog Author Entity
    '''
    name = models.CharField('用户名',max_length=255,unique=True)
    password = models.CharField('密码',max_length=64)
    email = models.EmailField('Email')
    
class Post(models.Model):    
    '''Post Entity'''
    title = models.CharField('标题',max_length=255)
    content = models.TextField('内容')
    category = models.ManyToManyField(Category,null=True,blank=True,verbose_name='分类')
    post_name = models.CharField('文章缩略名',max_length=255,unique=True,blank=True,
                                 help_text='作为文章url路径,勿使用中文,不填则使用url编码后的文章标题')
    post_type = models.CharField('类型',max_length=10,default='post',choices=POST_TYPES)
    post_status = models.CharField('文章状态',max_length=10,default='publish',choices = POST_STATUS)
    post_parent = models.ForeignKey('self',null=True, blank=True,related_name='child_set',verbose_name='上级页面')
    pubdate = models.DateTimeField('发布时间',auto_now_add=True)
    hits = models.IntegerField('点击数',default=0,editable=False)
    menu_order = models.IntegerField('菜单排序',default=0)
    comment_status = models.CharField('允许评论状态',default= POST_COMMENT_STATUS[0][0],max_length=10,choices = POST_COMMENT_STATUS)
    comment_count = models.IntegerField('评论数',default=0,editable=False)
    tags = models.ManyToManyField(Tags,null=True,blank=True,verbose_name='标签',related_name='post_set')
    
    def save(self):
        #override save
        if not self.post_name:
            #replace the space of title
            self.post_name = self.title.replace(' ','-')
            self.post_name = self.post_name.replace(u'　','-')
            self.post_name = self.post_name.replace('.','')
            self.post_name = encoding.iri_to_uri(self.post_name)
                  
        super(Post,self).save()
        #update tags reference_count
        if self.tags:
            all_tags =  self.tags.all()
            for tag in all_tags:
                tag.reference_count = len(tag.post_set.all())
                tag.save()      
    
    def __unicode__(self):
        return self.title
    #def __str__(self):
    #    return self.title
    def get_absolute_url(self):        
        if self.post_name:
            return '/%d/%d/%d/%s/' % (self.pubdate.year,
                                      self.pubdate.month,
                                      self.pubdate.day,
                                      self.post_name)
        else:
            return '/%d/%d/%d/%i/' % (self.pubdate.year,
                                      self.pubdate.month,
                                      self.pubdate.day,
                                      self.id)
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
    
    def get_comments(self):
        '''Get post or page approved comments'''
        comments = self.comments_set.all()
        approved_comments = []
        for cmt in comments:
            if cmt.comment_approved == str(COMMENT_APPROVE_STATUS[1][0]):
                approved_comments.append(cmt)
        return approved_comments
    
    
    class Meta:
        ordering = ['-pubdate']
        verbose_name='文章'
        verbose_name_plural = '文章'

    class Admin:
        list_display = ('title','get_cat_str','pubdate','hits')
        search_fields = ['title']
        list_filter =('post_type','category')

class Comments(models.Model):
    '''user comments'''
    post = models.ForeignKey(Post,verbose_name='文章',related_name='comments_set')
    comment_author = models.CharField('作者名',max_length=32)
    comment_author_email = models.EmailField(verbose_name='Email')
    comment_author_url = models.URLField('网址',null=True,blank=True,verify_exists=False)
    comment_author_IP = models.IPAddressField(verbose_name='IP',null=True,editable=False)
    comment_date = models.DateTimeField(verbose_name='发表时间',auto_now_add=True,editable=False)
    comment_content = models.TextField(verbose_name='评论内容')
    comment_approved = models.CharField('审核状态',max_length=32,choices=COMMENT_APPROVE_STATUS)
    comment_agent = models.CharField('用户浏览器信息',editable=False,max_length=255,null=True)
    user_id = models.IntegerField('用户id',editable=False,null=True)
    
    def save(self):
        #decode html code
        self.comment_content = django.utils.html.escape(self.comment_content)
        self.comment_content = html.htmlDecode(self.comment_content)                   
        super(Comments,self).save()
        #if comment is approved,update related post comment count
        if self.comment_approved == str(COMMENT_APPROVE_STATUS[1][0]):
            self.post.comment_count = len(self.post.comments_set.all())
            self.post.save() 
        
    def __unicode__(self):
        return self.comment_content
   
    def get_absolute_url(self):        
        if self.post.post_name:
            return '/%d/%d/%d/%s/#comment' % (self.post.pubdate.year,
                                              self.post.pubdate.month,
                                              self.post.pubdate.day,
                                              self.post_name)
        else:
            return '/%d/%d/%d/%i/#comment' % (self.post.pubdate.year,
                                              self.post.pubdate.month,
                                              self.post.pubdate.day,
                                              self.id)
    
    class Meta:
        ordering = ['-comment_date']
        verbose_name='评论'
        verbose_name_plural = '评论'

    class Admin:
        list_filter =('comment_approved',)
        #list_display = ('title','get_cat_str','pubdate','hits')
        search_fields = ['comment_author']

class Links(models.Model):
    '''Friend links entity'''
    link_url = models.URLField('链接地址')
    link_title = models.CharField('链接标题',unique=True,max_length=32)
    link_desc = models.CharField('链接说明',null=True,blank=True,max_length=255)
    link_image = models.CharField('链接图片',null=True,blank=True,max_length=255)
    link_order = models.IntegerField('链接排序',default=0,help_text='值小的靠前')
    link_updated = models.DateTimeField('链接添加时间',auto_now=True,editable=False)
    
    def __unicode__(self):
        return self.link_title
   
    def get_absolute_url(self):        
        return self.link_url
    class Meta:
        ordering = ['link_order']
        verbose_name='链接'
        verbose_name_plural = '链接'

    class Admin:
        #pass
        list_display = ('link_title','link_url')
        #search_fields = ['link_tit']