from django.conf.urls import url
from django.contrib.auth.views import (
	LoginView,
	LogoutView,
	PasswordResetView,
	PasswordResetDoneView,
	PasswordResetConfirmView,
	PasswordResetCompleteView,
	)

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.Home, name='home'),
    url(r'^login/$', LoginView.as_view(template_name='accounts/login.html'), name='login'),        
    
    url(r'^logout/$', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'), 
    url(r'^profile/$', views.Profile , name='profile'),
    url(r'^profile/edit/$', views.Edit_profile , name='edit_profile'),
    url(r'^profile/editpic/$', views.Edit_profilepic , name='edit_profilepic'),
    url(r'^register/$', views.Register , name='register'),
    url(r'^change-password/$', views.Change_Password , name='change_password'),    
    url(r'^reset-password/$', PasswordResetView, {'template_name': 'accounts/reset_password.html',
    										   'post_reset_redirect': 'app:password_reset_done', 
    										   'email_template_name': 'accounts/reset_password_email.html'},
    										    name='reset_password'),
    url(r'^reset-password/done/$', PasswordResetDoneView, {'template_name': 'accounts/reset_password_done.html'},
    													  name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
												PasswordResetConfirmView,
												{'template_name': 'accounts/reset_password_confirm.html',
												 'post_reset_redirect': 'app:password_reset_complete'},
												  name='password_reset_confirm'),
    url(r'^reset-password/complete/$', PasswordResetCompleteView,{'template_name': 'accounts/reset_password_complete.html'}, 
												                 name='password_reset_complete'),
    url(r'^inbox/$', views.Inbox , name='inbox'),
    url(r'^msg/(?P<pk>\d+)/$', views.Msg_View , name='msg'),
    url(r'^new_msg/$', views.New_Msg , name='new_msg'),
    url(r'^del_msg/$', views.Del_Msg , name='del_msg'),    
    url(r'^read_msg/$', views.Read_Msg , name='read_msg'),    
    url(r'^unread_msg/$', views.Unread_Msg , name='unread_msg'),    
    url(r'^side_menu/$', views.Side_Menu , name='side_menu'),    
]
