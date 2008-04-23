#coding=utf-8
from django.utils.translation import ugettext as _
from pylogs.todo.models import Project,Task,TASK_PRIORITY,PROJECT_TYPE
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import get_object_or_404,get_list_or_404,render_to_response

def index(request):
    '''todo homepage'''    
    is_auth = request.user.is_authenticated()
    #not completed projects
    if is_auth:        
        projects = Project.objects.extra(where=['project_tasks = 0 or project_tasks <> project_completed '])
        #projects = Project.objects.filter(project_tasks__exact = project_completed)
    else:#public projects only
        projects = Project.objects.extra(where=['project_tasks = 0 or project_tasks <> project_completed  and project_type=%s'], params=[PROJECT_TYPE['public']])
    #completed projects
    if is_auth:
        com_proj = Project.objects.extra(where=['project_tasks > 0 and project_tasks = project_completed '])
    else:
        com_proj = Project.objects.extra(where=['project_tasks > 0 and project_tasks = project_completed  and project_type=%s'], params=[PROJECT_TYPE['public']])
        
    return render_to_response('todo/index.html',
                                  {'projects':projects,'completed_projects':com_proj,'is_authenticated':is_auth})
    #return HttpResponse('this a test task page')
    
def task_add(request):
    '''add task to project'''
    is_auth(request)
    pid = int(request.POST.get('pid',0))
    task = Task()
    task.task_name = request.POST.get('task_name')
    task.task_project = get_object_or_404(Project,id__exact = pid)
    priority = request.POST.get('priority')
    if priority:
        task.task_priority = priority
    else:
        task.task_priority = TASK_PRIORITY['medium']
    task.task_completed = 0    
    task.save()
    #add project task count
    task.task_project.project_tasks += 1
    task.task_project.save()
    #return HttpResponseRedirect('/todo/')
    return HttpResponse('success')
    
def project_add(request):
    '''add todo project'''    
    is_auth(request)
    project = Project()
    project.project_name = request.POST.get('project_name')
    project.project_type = request.POST.get('project_type',0)
    project.project_desc = u''
    project.project_slug = u''
    project.project_tasks = 0
    project.project_completed = 0
    project.save()
    return HttpResponse('success')

def project_del(request):
    '''delete project'''
    is_auth(request)
    project_id = int(request.POST.get('project_id',0))
    project = get_object_or_404(Project,id__exact=project_id)
    project.delete()
    return HttpResponse('success')

def project_chg_type(request):
    '''change project type'''
    is_auth(request)
    project_id = int(request.POST.get('project_id',0))
    project = get_object_or_404(Project,id__exact=project_id)
    if project.project_type == PROJECT_TYPE['public']:
        project.project_type = PROJECT_TYPE['private']
    else:
        project.project_type = PROJECT_TYPE['public']
    project.save()
    return HttpResponse('success')

def task_done(request):
    '''done a task'''
    is_auth(request)
    task_id = int(request.POST.get('task_id',0))
    task = get_object_or_404(Task,id__exact=task_id)
    task.task_completed = 1
    task.save()
    #add project completed task count
    task.task_project.project_completed += 1
    task.task_project.save()
    return HttpResponse('success')

def task_undone(request):
    '''undone a task'''
    is_auth(request)
    task_id = int(request.POST.get('task_id',0))
    task = get_object_or_404(Task,id__exact=task_id)
    task.task_completed = 0
    task.save()
    #reduce project completed task count
    task.task_project.project_completed -= 1
    task.task_project.save()
    return HttpResponse('success')

def task_del(request):
    '''delete a task'''
    is_auth(request)
    task_id = int(request.POST.get('task_id',0))
    task = get_object_or_404(Task,id__exact=task_id)
    task.task_project.project_tasks -= 1
    #is a completed task
    if task.task_completed == 1:
        task.task_project.project_completed -= 1
    task.task_project.save()
    task.delete()
    return HttpResponse('success')

def is_auth(req):
    '''check use login status'''
    if not req.user.is_authenticated():
        raise Exception(u'please login first!')