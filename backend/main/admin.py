from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(MontylyReport)
admin.site.register(Todo)

admin.site.register(Product)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}


@admin.register(HistoryProduct)
class HistoryProductAdmin(admin.ModelAdmin):
	list_display = ("product", "mode", "quantity",'comment')
	list_filter = ("mode", "created_at")
	search_fields = ['comment']
