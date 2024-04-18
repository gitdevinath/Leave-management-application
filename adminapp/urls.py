from django.urls import path
from .import views
from . views import addemployee

urlpatterns = [
    #path('', views.log, name='log'),
    path('', views.index, name='demo'),
    path('login/', views.login_view, name='loginView'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leaveManagement/', views.leaveManagement, name='leaveManagement'),
    path('pendingLeaves/', views.pendingLeaves, name='pendingLeaves'),
    path('logout/', views.logout, name='logout'),
    path('homeContent/', views.homeContent, name='homeContent'),
    path('addemployee/', addemployee.as_view(), name='addemployee'),
   # path('add_superuser/', AddSuperUser.as_view(), name='AddSuperUser'),
    
    #to view the leave content on second nav
    path('addleave_content/', views.add_leaveContent, name='add_leaveContent'),

    path('add_leave/', views.add_leave, name='addLeave'),

    path('leave_content/', views.leave_content, name='leave_content'),
    path('leave_lists/<int:leave_id>', views.leave_lists, name='leave_lists'),
    path('leave_details/', views.leave_details, name='leave_details'),

    
    path('approve_leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('reject_leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),
]