from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),  # 默认访问登录页面
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('individual/', views.view_individual_performance, name='individual'),
    path('individual_form/', views.view_individual_form, name='individual_form'),
    path('team/', views.view_team_performance, name='team'),
    path('daily_ranking/', views.daily_ranking, name='daily_ranking'),
    path('daily_ranking_form/', views.daily_ranking_form, name='daily_ranking_form'),
    path('monthly_ranking/', views.monthly_ranking, name='monthly_ranking'),
    path('monthly_ranking_form/', views.monthly_ranking_form, name='monthly_ranking_form'),
    path('honor_hall/', views.honor_hall, name='honor_hall'),
    path('million_club/', views.million_club, name='million_club'),
    path('king_team/', views.king_team, name='king_team'),
    path('flying_star/', views.flying_star, name='flying_star'),
    path('add_honor/', views.add_honor, name='add_honor'),
    path('edit_honor/<int:honor_id>/', views.edit_honor, name='edit_honor'),
    path('delete_honor/<int:honor_id>/', views.delete_honor, name='delete_honor'),
    path('sales_dashboard_form/', views.sales_dashboard_form, name='sales_dashboard_form'),
    path('sales_dashboard/', views.sales_dashboard, name='sales_dashboard'),
]

