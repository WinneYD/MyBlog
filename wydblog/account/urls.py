from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name='account'
urlpatterns=[
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='registration/logout.html'),name='logout'),
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html',success_url=reverse_lazy('account:password_change_done')),name='password_change'),
    path('password_change_done/',auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),name='password_change_done'),
    path('register/',views.register,name='register'),

    ]


#Django 内置的登录、修改密码、找回密码等视图函数对应的 URL 模式位于
    #django.contrib.auth.urls.py 中，首先在工程的 urls.py 文件里包含这些 URL 模式
    #将 django.contrib.auth.urls.py 包含进来

#^users/login/$ [name='login']
#^users/logout/$ [name='logout']
#^users/password_change/$ [name='password_change']
#^users/password_change/done/$ [name='password_change_done']
#^users/password_reset/$ [name='password_reset']
#^users/password_reset/done/$ [name='password_reset_done']
#^users/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
#^users/reset/done/$ [name='password_reset_complete']

