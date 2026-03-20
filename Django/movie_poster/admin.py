from django.contrib import admin
from .models import Poster

admin.site.register(Poster)

admin.site.site_header = 'JUST搜搜管理后台'  # 设置header
admin.site.site_title = 'JUST搜搜管理后台'  # 设置title
admin.site.index_title = 'JUST搜搜管理后台'
