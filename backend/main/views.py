from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.models import model_to_dict
from .forms import *
from .models import *
 
# Create your views here.
@login_required
def HomeView(request):
    report = MontylyReport.objects.first()
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
            history = history.filter(created_at__range=[start,timezone.now()])    
    
    history = Paginator(history, 6)
    page_number = request.GET.get('page')
    page_obj = history.get_page(page_number)

    return render(request, 'history.html', {'histories': page_obj, 'form': form})

@login_required
def productView(request):
    products = Product.objects.select_related('group').all()
    form = ProductSearchform(request.GET or None)
    if request.method == 'GET':
        if form['time'].value():
            start = timezone.now() - timedelta(days=int(form['time'].value()))
            products = products.filter(created_at__range=[start,timezone.now()])    
        if form['group'].value():
            products = products.filter(group=form['group'].value())
        if form['query'].value():
            products = products.filter(name__icontains=form['query'].value())
        if request.GET.get('id', False):
            obj = Product.objects.select_related('group').get(id=request.GET.get('id', False))
            obj.delete()
            return HttpResponseRedirect("/product")

    products = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = products.get_page(page_number)

    return render(request, 'product.html',  {'products': page_obj, 'form': form})

@login_required
def GetCart(request):
    form = CartFilter(request.GET or None)
    cart =  Cart.objects.prefetch_related('history').all()
    return render(request, 'cartdetail.html', {'form': form, 'carts': cart})


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'addproduct.html'
    fields = '__all__'
    exclude = ('is_calc')
    success_url = '/product/'

    def form_valid(self, form):
        form.instance.is_calc = True
        return super().form_valid(form)

class EditProduct(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'addproduct.html'
    fields = ("name", "sell", "buy", 'measure', "group")
    success_url = '/product/'

class CreateHistory(LoginRequiredMixin, CreateView):
    model = HistoryProduct
    template_name = 'AddHistory.html'
    fields = '__all__'
    exclude = ('is_calc', 'price')
    success_url = '/history/'

    def get_initial(self):
        super(CreateHistory, self).get_initial()
        return {'product': self.request.GET.get('id', False)}

    def form_valid(self, form):
        form.instance.is_calc = True
        return super().form_valid(form)


@login_required
def GetProduct(request):
    if request.method == 'GET' and request.user.is_authenticated:
        obj = Product.objects.select_related('group').get(id = request.GET.get('data', True))
        return JsonResponse({'obj': model_to_dict(obj)})


@login_required
def CartView(request):
    form = CartForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            obj.is_calc = True 
            obj.mode = 'sale'
            obj.save()
            cart = Cart.objects.create(total = obj.price )
            cart.history.add(obj)
            cart.save()
            return redirect(f'/cart/{cart.id}')

    return render(request, 'cart.html', {'form': form})


@login_required
def CartDetail(request, id):
    #objects
    cart = Cart.objects.prefetch_related('history').get(id=id)
    history = cart.history.select_related('product').all()
    #forms
    form = CartForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            obj.is_calc = True 
            obj.mode = 'sale'
            obj.save()

            cart.history.add(obj)
            cart.total = cart.total + obj.price
            cart.save()
            return redirect(f'/cart/{cart.id}')

    if request.method == 'GET':
        if request.GET.get('shortinfo', False):
            cart.comment = request.GET.get('shortinfo', True)
            cart.save()

            return redirect(f'/get-carts')
        


    return render(request, 'cart.html', {'form': form, 'cart': cart, 'histories': history})
