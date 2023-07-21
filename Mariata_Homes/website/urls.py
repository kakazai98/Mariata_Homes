from django.urls import path

from website import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login.html', views.login, name='login'),
    path('login.html', views.logout, name='logout'),
    path('admin.html', views.admin, name='admin'),
    path('approve.html', views.approve, name='approve'),
    path('update.html', views.update, name='update'),
    path('delete.html',views.delete,name='delete'),
    path('notification.html',views.send_email, name='notification')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


