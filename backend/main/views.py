from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from .forms import *
 
# Create your views here.
@login_required
def HomeView(request):
    report = MontylyReport.objects.last()
    todo = Todo.objects.all().order_by('is_active')
    history = HistoryProduct.objects.select_related('product').all()

    return render(request, 'index.html', {'report': report, 'todos' : todo, 'histories': history})

@login_required
def workWithTodo(request):
    text = request.GET["data"]
    event = request.GET["event"]

    if event == 'add' and request.user.is_authenticated:
        Todo.objects.create(name=text)
        print('created')
        return JsonResponse({'success': 'created'}) 

    if event =='update':
        try:
            obj = Todo.objects.get(id=text)
        finally:
            obj.is_active = True
            obj.save()
            return JsonResponse({'success': 'updated'}) 
    
    if event =='delete':
        try:
            obj = Todo.objects.get(id=text)
        finally:
            obj.delete()
            return JsonResponse({'success': 'deleted'}) 

@login_required
def todoView(request):
    todo = Todo.objects.order_by('is_active','-id')
    return render(request, 'todos.html', {'todos' : todo})

@login_required
def historyView(request):
    history = HistoryProduct.objects.select_related('product').all()
    form = Searchform(request.GET or None)
    if request.method == 'GET':
        if form['mode'].value():
            history = history.filter(mode=form['mode'].value())
        if form['query'].value():
            history = history.filter(comment__icontains=form['query'].value())   
        if form['product'].value():
            history = history.filter(product=form['product'].value())   
        if form['time'].value():
            start = timezone.now() - timedelta(days=int(form['time'].value()))
            print(start)
            history = history.filter(created_at__range=[start,timezone.now()])    
    
    history = Paginator(history, 6)
    page_number = request.GET.get('page')
    page_obj = history.get_page(page_number)

    return render(request, 'history.html', {'histories': page_obj, 'form': form})

def productView(request):
    return render(request, 'product.html')