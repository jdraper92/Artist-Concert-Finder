from django.urls import path

from . import views

app_name = 'playlistLinks'
urlpatterns = [
    path('', views.home, name='home'),
    path('process/',views.getData,name='getData'),
    path('<int:user_id>/concerts/',views.concerts,name='concerts'),
    path('delete/',views.inputForDelete,name='inputForDelete'),
    path('deleting',views.delete,name='deleting'),
    path('<str:user_email>/deleted/',views.deleteDone,name='deleteDone'),
    path('getConcerts/',views.getConcerts,name='getConcerts'),
    path('concerts/',views.inputForConcerts,name='inputForConcerts'),
    path('update/<str:city>/',views.updateAllConcerts,name='updateAllConcerts')
]