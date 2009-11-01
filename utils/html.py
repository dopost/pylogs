<<<<<<< HEAD
#!/usr/bin/env python
#coding=utf-8
#html utility methods
import re
r = re.compile(r'\b(([A-Z]+[a-z]+){2,})\b')
def htmlDecode(str):
    """处理页面换行等，替换为html编码。并且将回车符转为<br>"""
    str = re.sub(r'[\n\r]+', '<br>', str)
    #str = re.sub(r'[\s]+','&nbsp;',str)
=======
#!/usr/bin/env python
#coding=utf-8
#html utility methods
import re
r = re.compile(r'\b(([A-Z]+[a-z]+){2,})\b')
def htmlDecode(str):
    """处理页面换行等，替换为html编码。并且将回车符转为<br>"""
    str = re.sub(r'[\n\r]+', '<br>', str)
    #str = re.sub(r'[\s]+','&nbsp;',str)
>>>>>>> 1b1aba63e4e25c4d81cdc8ee168ba60582ceb029
    return str