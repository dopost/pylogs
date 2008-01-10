#!/usr/bin/env python
#coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
import re
from pygments import highlight, lexers, formatters
address = [
    {'name':'张三','address':'地址一'},
    {'name':'李四','address':'地址二'}
    ]

def index(request):
    code = u'''
    Code is All below;
    [code lang="python"]
    def save(self):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()
        # Use safe_mode in Markdown to prevent arbitrary tags.
        self.description_html = markdown(self.description, safe_mode=True)
        self.highlighted_code = self.highlight()
        self.tag_list = self.tag_list.lower() # Normalize to lower-case
        super(Snippet, self).save()
    [/code]
    The HTML code is Below:
    [code lang="html"]
     <div class="sidebar">
          <div class="sbtop"></div>
          <div class="sbinfo">
            <h3>
              Categories
            </h3>            
              <div class="sbinner">
                <ul>
                <li><a href="#">Pylogs学习笔记</a></li>
                <li><a href="#">Pylogs学习笔记</a></li>
                <li><a href="#">Pylogs学习笔记</a></li>
                </ul>
              </div>         
          </div>
          <div class="sbbottom"></div>
        </div>
    [/code]
    That's ALL!
    '''
    
    r = re.compile(r'\[code\s+lang="(\w+)"\](.+?)\[/code\]',re.DOTALL|re.I|re.M)
    allmatches = r.findall(code)
    for i in range(0,len(allmatches)):
        code = r.sub('[CODE]',code)
        code = code.replace('[CODE]',hl(allmatches[i][0],allmatches[i][1]),1)
            
        
    return HttpResponse(code)
def hl(lang,code):
    le = lexers.get_lexer_by_name(lang)
    highlightedStr =  highlight(code,
                         le,
                         formatters.HtmlFormatter(linenos=True))
    return highlightedStr
    