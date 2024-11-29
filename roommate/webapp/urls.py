from django.urls import path
from . import views

urlpatterns = [
    path('', views.roommate, name='roommate'),
    path('roommate', views.roommate, name='roommate'),
    path('home',views.home,name='home'),
    
    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name='signup'),
    path('contact_us',views.contact_us,name='contact_us'),
    
    path('add_post',views.add_post,name='add_post'),
    path('my_post',views.my_post,name='my_post'),
    path('edit_post',views.edit_post,name='edit_post'),
    path('remove_post',views.remove_post,name='remove_post'),
    
    path('view_post',views.view_post,name='view_post'),
    path('view_details',views.view_details,name='view_details'),
    path('favorites',views.favorites,name='favorites'),
    
    path('maleshared',views.maleshared,name='maleshared'),
    path('femaleshared',views.femaleshared,name='femaleshared'),
    path('malehostel',views.malehostel,name='malehostel'),
    path('femalehostel',views.femalehostel,name='femalehostel'),
    path('familysub',views.familysub,name='familysub'),
    path('twobhk',views.twobhk,name='twobhk'),
    path('threebhk',views.threebhk,name='threebhk'),
    
    path('profile',views.profile,name='profile'),
     path('change_password',views.change_password,name='change_password'),
    
    path('accu',views.accu,name='accu'),
    path('add_fav',views.add_fav,name='add_fav'),
    path('remove_fav',views.remove_fav,name='remove_fav'),   
    path('policy',views.policy,name='policy'),
    path('contribute',views.contribute,name='contribute'),
    path('about_us',views.about_us,name='about_us'),
]
