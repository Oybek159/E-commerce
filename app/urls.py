from django.urls import path
# from django.contrib.auth import views as auth_views


from . import views
# from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('new/', views.new, name='new'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('new/<int:item_pk>/', views.new_conversation, name='new'),
    path('inbox', views.inbox, name='inbox'),
    path('inbox/<int:pk>/', views.inbox_detail, name='inbox_detail')
    # TIP 1
    #path('login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
]