from django.urls import path
from .import views

app_name = "main"

urlpatterns = [
    path("", views.HomeView , name="home"),
    path("GetTodos/", views.workWithTodo , name="GetTodos"),
    path("todos/", views.todoView , name="todos"),
    path("product/", views.productView , name="product"),
    path("history/", views.historyView , name="history"),
    path("get-carts/", views.GetCart , name="getCarts"),
    path("add-product/", views.ProductCreate.as_view() , name="add-prouct"),
    path("edit-product/<pk>/", views.EditProduct.as_view() , name="edit-prouct"),
    path('create-history/', views.CreateHistory.as_view(), name="create-history"),
    path('getproduct/', views.GetProduct, name='getProduct'),
    path('cart/', views.CartView, name='cart'),
    path('cart/<id>', views.CartDetail, name='cart-detail'),
    path('data/<id>', views.DataView, name='data')
]
