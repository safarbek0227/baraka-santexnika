from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
 
# Create your views here.
@login_required
def HomeView(request):
    report = MontylyReport.objects.select_related('factory').filter(factory = request.user).last()
    todo = Todo.objects.select_related('factory').filter(factory = request.user).order_by('is_active','-id')
    history = HistoryProduct.objects.select_related('factory').filter(factory= request.user)

    return render(request, 'index.html', {'report': report, 'todos' : todo, 'historys': history})


def workWithTodo(request):
    text = request.GET["data"]
    event = request.GET["event"]

    if event == 'add' and request.user.is_authenticated:
        Todo.objects.create(name=text, factory=request.user)
        print('created')
        return JsonResponse({'success': 'created'}) 

    if event =='update':
        try:
            obj = Todo.objects.select_related('factory').get(id=text, factory=request.user)
        finally:
            obj.is_active = True
            obj.save()
            return JsonResponse({'success': 'updated'}) 
    
    if event =='delete':
        try:
            obj = Todo.objects.select_related('factory').get(id=text, factory=request.user)
        finally:
            obj.delete()
            return JsonResponse({'success': 'deleted'}) 

def todoView(request):
    todo = Todo.objects.select_related('factory').filter(factory = request.user).order_by('is_active','-id')
    return render(request, 'todos.html', {'todos' : todo})

