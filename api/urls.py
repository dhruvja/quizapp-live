from django.contrib import admin
from django.urls import path,include
from . import views
from .views import register, LoginAPI
from knox import views as knox_views

urlpatterns = [
    path('',views.apiOverview,name='apiOverview'),
    path('register',register,name='register'),
    path('users',views.userAccounts,name='users'),
    path('answers',views.Answer,name='answers'),
    #path('hosted',views.Hosteds,name="hosted"),
    path('hostnow',views.hostNow,name="hostnow"),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('listquizzes',views.listquizzes,name='listquizzes'),
    path('questions/<str:pk>',views.questions,name='questions'),
    path('chosenanswer',views.chosenAnswers,name='chosenanswer'),
    path('joinquiz',views.joinQuiz,name='joinquiz'),
    path('getanswers/<str:pk>',views.GetAnswers,name='getanswers'),
    path('getresults/<str:pk>',views.getResult,name='getresults'),
    path('showresults/<str:pk>',views.showResult,name='showresults'),
    path('joinedquizzes',views.joinedQuizzes,name='showresults'),
    path('createquestion',views.CreateQuestion,name='createquestions'),
    path('updatequestion',views.UpdateQuestion,name='updatequestions'),
    path('hostedquiz',views.Hosted,name='hostedquiz'),
    path('leaderboard/<str:pk>',views.leaderboard,name='leaderboard'),
    path('deletequestion/<str:pk>',views.deletequestion,name='deletequestion'),
    path('editquizinfo/<str:pk>',views.editQuizInfo,name="editquizinfo"),
    path('editquizupdate/<str:pk>',views.editQuizUpdate,name="editquizupdate"),
    path('sendmail',views.sendmail,name="sendmail")
]