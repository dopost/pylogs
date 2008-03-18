#!/usr/bin/env python
from django.newforms import ModelForm
from pylogs.blog.models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title','content','post_name','category','post_status')
    

