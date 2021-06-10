from django.conf.urls import url
from . import views
from django.urls import include, path
from django.contrib.auth import views as auth_views


app_name = 'ide'

urlpatterns = [
    url(r'^contact',views.contact,name='contact'),
    url(r'^timetable_upload',views.timetable_upload,name='timetable_upload'),
    url(r'^about',views.about,name='about'),
    url(r'^alogin',views.adminlogin,name='alogin'),
    url(r'^exam_upload',views.exam_upload,name='exam_upload'),
    url(r'^flogin',views.userlogin,name='flogin'),
    url(r'^index$', views.home,name='home'),
    url(r'^logout', views.userlogout,name='logout'),
    url(r'^register$', views.registeruser,name='register'),
    url(r'^facultyhomepage-schedule.html', views.ptimetable,name='timetable'),
    url(r'^facultyhomepage-notifications.html', views.pnot,name='fnotification'),
    url(r'^adminhomepage-notifications.html', views.apnot,name='anotification'),
    url(r'^adminhomepage-reschedule.html', views.adminreschedule,name='areschedule'),
    url(r'^adminhomepage-allocate.html', views.allocate,name='allocate'),
    path('fnotification/<int:id>/', views.pnot1,name='fnotification'),
    path('anotification/<int:id>/', views.apnot1,name='anotification'),
    url(r'^facultyhomepage-reschedule.html', views.pexam,name='reschedule'),
    path('schedule/<int:id>/', views.pexam1,name='schedule'),
    url(r'^fhome$', views.fhome),
    url(r'^ahome$', views.ahome),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='ide/forgotpassword.html'),name="reset_password"),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='ide/passwordresetdone.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='ide/passwordresetconfirm.html'),name="password_reset_confirm"),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='ide/passwordresetcomplete.html'),name="password_reset_complete"),
]