from django.contrib import admin
from first.models import News

class News_col(admin.ModelAdmin):
    list_display=('title','link')
admin.site.register(News,News_col)
# Register your models here.
