from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name='home'),
    path("registration/", views.RegistrationView.as_view(), name = 'registration'),
    path('accounts/login/', views.SignInView.as_view(), name='sign-in'),
    path('logout/', auth_views.LogoutView.as_view(next_page='sign-in'), name='logout'),
    path('account-verify/<slug:token>/', views.account_verify, name = "account-verify"),


    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name="dashboard/passwordchange.html", form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name ="passwordchange" ),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name="dashboard/passwordchangedone.html"),name="passwordchangedone"),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='dashboard/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='dashboard/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='dashboard/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='dashboard/password_reset_complete.html'), name='password_reset_complete'),




    path("home_work_details/", views.home_work_details, name='home_work_details'),
    path("edit_homework/<int:pk>", views.edit_home_work, name="edit_homework"),
    path("delete_homework/<int:pk>", views.delete_homework, name="delete_homework"),
    path("add_new_homework/", views.add_new_homework, name='add_new_homework'),
    path("view_homework/<int:pk>", views.view_homework, name="view_homework"),


    path("notes_details/", views.notes_details, name='notes_details'),
    path("delete_notes/<int:pk>/", views.delete_notes, name = "delete_notes"),
    path("edit_notes/<int:pk>/", views.edit_notes, name = "edit_notes"),
    path("create_notes/", views.create_notes, name='create_notes'),


    path("youtube/", views.youtube, name='youtube'),


    path("todo/", views.todo, name='todo'),
    path("edit_todo/<int:pk>/", views.edit_todo, name = "edit_todo"),
    path("delete_todo/<int:pk>/", views.delete_todo, name = "delete_todo"),
    path("add_new_todo/", views.AddNewTodoView.as_view(), name='add_new_todo'),


    path("books/", views.books, name='books'),
    path("dictionary/", views.dictionary, name='dictionary'),



    path("contact/", views.contact, name='contact'),
    path("lecture_contact/", views.lecture_contact, name='lecture_contact'),

    path('about/', views.about, name='about'),
    path("lecture_about/", views.lecture_about, name='lecture_about'),


    path("profile/", views.profile, name='profile'),
    path('delete_profile/<int:pk>/', views.delete_profile, name = 'delete_profile'),
    path('edit_profile/<int:pk>/', views.edit_profile, name = 'edit_profile'),
    

    path("assignment/", views.assignment, name='assignment'),
    path('edit_assignment/<int:pk>/', views.edit_assignment, name = 'edit_assignment'),
    path('delete_assignment/<int:pk>/', views.delete_assignment, name = 'delete_assignment'),
    path("add_assignment/", views.add_assignment, name='add_assignment'),


    path("lecture_home/", views.lecture_home, name='lecture_home'),

    path("lecture_registration/", views.LectureRegistrationView.as_view(), name = 'lecture_registration'),

    path("lecture_profile/", views.lecture_profile, name='lecture_profile'),
    path('edit_lec_profile/<int:pk>/', views.edit_lec_profile, name = 'edit_lec_profile'),
    path('delete_lec_profile/<int:pk>/', views.delete_lec_profile, name = 'delete_lec_profile'),

    path("lecture_assignment/", views.lecture_assignment, name='lecture_assignment'),
    path('edit_assignment_lec/<int:pk>/', views.edit_assignment_lec, name = 'edit_assignment_lec'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
