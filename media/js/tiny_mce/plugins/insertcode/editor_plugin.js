<<<<<<< HEAD
(function(){tinymce.create('tinymce.plugins.InsertCode',{init:function(ed,url){var t=this;t.editor=ed;ed.addCommand('mceInsertCode',function(){ed.windowManager.open({file:url+'/code.htm',width:580,height:400,inline:1},{plugin_url:url});});ed.addButton('insertcode',{title:'Insert code',cmd:'mceInsertCode',image:url+'/img/icon.gif'});},getInfo:function(){return{longname:'Insert Highlight Code',author:'Sky',authorurl:'http://oteam.cn',infourl:'http://oteam.cn/about',version:"0.1"};}});tinymce.PluginManager.add('insertcode',tinymce.plugins.InsertCode);})();

=======
(function(){tinymce.create('tinymce.plugins.InsertCode',{init:function(ed,url){var t=this;t.editor=ed;ed.addCommand('mceInsertCode',function(){ed.windowManager.open({file:url+'/code.htm',width:580,height:400,inline:1},{plugin_url:url});});ed.addButton('insertcode',{title:'Insert code',cmd:'mceInsertCode',image:url+'/img/icon.gif'});},getInfo:function(){return{longname:'Insert Highlight Code',author:'Sky',authorurl:'http://oteam.cn',infourl:'http://oteam.cn/about',version:"0.1"};}});tinymce.PluginManager.add('insertcode',tinymce.plugins.InsertCode);})();

>>>>>>> 1b1aba63e4e25c4d81cdc8ee168ba60582ceb029
