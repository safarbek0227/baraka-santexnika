from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(MontylyReport)
admin.site.register(Todo)

admin.site.register(Product)
admin.site.register(HistoryProduct)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}