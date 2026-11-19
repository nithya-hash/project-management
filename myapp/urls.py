from django.urls import path

from.import views


urlpatterns=[
    path('',views.home,name="home"),
    path('add/', views.add, name='add'),
    path('add/insert/', views.insert, name='insert'),
    path('edit/<int:study_id>',views.edit,name='edit'),
    path('save/<int:study_id>',views.save,name='save'),
    path('detail/<int:study_id>',views.detail,name='detail'),
    path('delete/<int:study_id>',views.delete,name='delete'),
    path('login',views.login,name='login'),
    path('register', views.register, name='register'),
    path('logout',views.logout,name='logout'),

]

