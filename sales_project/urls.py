from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Django自带的管理后台
    path('', include('sales_app.urls')),  # 包含应用的URL配置
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 如果在开发模式下，添加静态文件的URL配置
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)