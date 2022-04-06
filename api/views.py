from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import generics,permissions,viewsets
from knox.models import AuthToken
from django.contrib.auth.models import User
from .serializer import RegisterSerializer, HostedSerializer,AnswerSerializer, RegisterSerializer1,ListQuizSerializer,HostedSerializer2,JoinQuizSerializer,ChosenAnswerSerializer,AnswerSerializer1,JoinedSerializer1,JoinedSerializer2,HostedSerializer3,QuestionSerializer2,OptionSerializer,LeaderboardSerializer,HostedSerializer4
from .models import HostQuiz,JoinQuiz,Option,Questions,Images,Answers, Email
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from knox.auth import TokenAuthentication
from django.db.models import F
from django.core.mail import send_mail
import random
import string
import secrets

# Create your views here.

@api_view(['GET'])
def apiOverview(request):

    commands = {
        'register': 'http://localhost:8000/api/register',
        'login': 'http://localhost:8000/api/token',
        'all users': 'http://localhost:8000/api/users',
        'all answers ': 'http://localhost:8000/api/answers',
        'create a quiz': 'http://localhost:8000/api/hostnow',
        'knox login': 'http://localhost:8000/api/login/',
        'knox logout': 'http://localhost:8000/api/logout/',
        'knox delete all tokens': 'http://localhost:8000/api/logoutall/',
        'listquizzes': 'http://localhost:8000/api/listquizzes',
        'questions with quiz id as parameter': 'http://localhost:8000/api/questions/1',
        'updates chosen option': 'http://localhost:8000/api/chosenanswer',
        'joinquiz': 'http://localhost:8000/api/joinquiz',
        'getanswers with joinquiz id as parameter': 'http://localhost:8000/api/getanswers/1',
        'getresults with joinquiz id as parameter': 'http://localhost:8000/api/getresults/1',
        'showresults with joinquiz id as parameter': 'http://localhost:8000/api/showresults/7',
        'joinedquizzes': 'http://localhost:8000/api/joinedquizzes',
        # path('showresults/<str:pk>',views.showResult,name='showresults'),
        # path('joinedquizzes',views.joinedQuizzes,name='showresults'),
    }

    return Response(commands)

@api_view(['GET'])
def userAccounts(request):
    users = User.objects.all()
    users = RegisterSerializer(users,many=True)

    return Response(users.data)

@api_view(['GET'])
def Answer(request):

    users = Answers.objects.all()
    users = AnswerSerializer(users,many=True)

    return Response(users.data)

@api_view(['POST'])
def register(request):

    userdata = RegisterSerializer1(data = request.data)
    data = {}
    if userdata.is_valid():
        user = userdata.save()
        data['token'] = AuthToken.objects.create(user)[1]
        data['status'] = "success"
    else:
        data['status'] = "Failed"
    
    return Response(data)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        print(request.user)
        return super(LoginAPI, self).post(request, format=None)
    
    # def post(self, request, *args, **kwargs):
    #     serializer = AuthTokenSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data
    #     return Response({
    #         "user": AuthTokenSerializer(user).data,
    #         "token": AuthToken.objects.create(user)[1]
    #     })





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def hostNow(request):

    request.data['host_id'] = request.user.id
    print(request.user.id)
    if request.user.is_superuser :
        hostnow = HostedSerializer3(data = request.data)
        if hostnow.is_valid():
            hostnow.save()
            # hostnow.data['host_id'] = request.user.id
            hostnow.data['status'] = 'success'
            return Response(hostnow.data,)

    request.data['status'] = 'failed'
    return Response(request.data,status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listquizzes(request):


    quizzes = HostQuiz.objects.all()
    print(request.user.id)

    quizzes = ListQuizSerializer(quizzes,many=True)
    return Response(quizzes.data)

# class UserAPI(generics.RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated, ]

#     quizzes = HostQuiz.objects.all()
#     quizzes = ListQuizSerializer(quizzes,many=True)

#     def get_object(self):
#         return self.request.user

@api_view(['GET'])
def questions(request,pk):
    questions = HostQuiz.objects.filter(id=pk).prefetch_related('questions')
    questions = HostedSerializer2(questions,many=True)

    return Response(questions.data)

@api_view(['POST'])
def chosenAnswers(request):

    print(request.data['time_elapsed'])
    if not Answers.objects.filter(quiz_id = request.data['quiz_id'],joinquiz_id = request.data['joinquiz_id'],question_id = request.data['question_id']).update(chosen_option = request.data['chosen_option'], time_elapsed = request.data['time_elapsed']):
        chosen_answers = ChosenAnswerSerializer(data = request.data)
        if chosen_answers.is_valid():
            x = chosen_answers.save()
            # v = str(x)
            # print(v[16:-1])

    


    return Response(chosen_answers.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def joinQuiz(request):

    request.data['candidate_id'] = request.user.id
    joinquiz = JoinQuizSerializer(data = request.data)
    data = "failed"
    if joinquiz.is_valid():
        if not JoinQuiz.objects.filter(candidate_id = request.data['candidate_id'],quiz_id = request.data['quiz_id']):
            joinquiz.save()
        else:
            joinquiz = JoinQuiz.objects.get(candidate_id = joinquiz.data['candidate_id'],quiz_id = joinquiz.data['quiz_id'])
            joinquiz = JoinQuizSerializer(joinquiz,many=False)
            
    
    return Response(joinquiz.data)

@api_view(['GET'])
def GetAnswers(request,pk):
    getanswers = Answers.objects.filter(joinquiz_id = pk)

    getanswers = AnswerSerializer1(getanswers,many=True)

    return Response(getanswers.data)
    
    
@api_view(['GET'])
def getResult(request,pk):
 
    joining = JoinQuiz.objects.filter(id=pk).prefetch_related("entered_answers")
    results = JoinedSerializer1(joining,many=True)

    scoring = {}
    scoring['points'] = 0
    scoring['time'] = 0
    print(len(results.data[0]['entered_answers']))
    for question in results.data[0]['entered_answers']:
        scoring['time'] += question['time_elapsed'] 
        if question['chosen_option']['id'] == question['question_id']['right_option']:
            print(question['chosen_option']['id'],question['question_id']['right_option'])
            scoring['points'] += question['question_id']['points']
            if Answers.objects.filter(id=question['id']).update(result=True):
                pass
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            print(question['chosen_option']['id'],question['question_id']['right_option'])
            if Answers.objects.filter(id=question['id']).update(result=False):
                pass
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

    updatescore = JoinQuiz.objects.filter(id=pk).update(score = scoring['points'], time_taken = scoring['time'])

    return Response(results.data)


@api_view(['GET'])
def showResult(request,pk):

    joining = JoinQuiz.objects.filter(id=pk).prefetch_related("entered_answers")
    results = JoinedSerializer1(joining,many=True)

    return Response(results.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def joinedQuizzes(request):

    id = request.user.id
    joined = JoinQuiz.objects.filter(candidate_id = id)

    joined = JoinedSerializer2(joined,many=True)

    return Response(joined.data)

@api_view(['POST'])
def CreateQuestion(request):
    print(request.data)
    questions = {}

    questions['question'] = request.data['question']
    questions['quiz_id']= request.data['quiz_id']
    questions['option_index'] = request.data['option_index']
    questions['points'] = request.data['points']

    opt = []

    questions = QuestionSerializer2(data = questions)
    if questions.is_valid():
        questions.save()
        question_id = questions.data['id']
        for i in request.data['options']:
            options = {}
            options['option'] = i['option']
            options['question_id'] = question_id
            option = OptionSerializer(data = options)
            if option.is_valid():
                option.save() 
                opt.append(option.data)
            else:
                return Response(option,status=status.HTTP_404_NOT_FOUND)
        
        data = questions.data 
        data['options'] = opt
        option_id = data['option_index']
        right_option = opt[option_id]['id']
        print(right_option,question_id)
        if Questions.objects.filter(id=question_id).update(right_option = right_option):
            data['right_option'] = right_option
            return Response(data)
        else:
            return Response(data,status=status.HTTP_404_NOT_FOUND)

        questions.data['status'] = "success"

        


    # questions.data['status'] = "failed"
    return Response(questions.data,status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def UpdateQuestion(request):
    print(request.data)
    x = -1
    if Questions.objects.filter(id=request.data['id']).update(question = request.data['question'],option_index = request.data['option_index'],points = request.data['points']):
        for i in request.data['options']:
            x += 1
            try:
                if i['id']:
                    p = Option.objects.filter(id = i['id']).update(option = i['option'])
            except:
                opt = {}
                opt['option'] = i['option']
                opt['question_id'] = request.data['id']
                # print(opt)
                opt = OptionSerializer(data = opt)
                if opt.is_valid():
                    opt.save()
                    request.data['options'][x] = opt.data

        print("options are ",request.data['options'])
        all_options = list(Option.objects.filter(question_id = request.data['id']).values('id'))
        # print(all_options)
        # print(len(all_options))
        
        if len(all_options) > len(request.data['options']):
            i = len(request.data['options'])
            print("i value is",i)
            while i<len(all_options):
                print("i increments to ",i)
                if Option.objects.filter(id = all_options[i]['id']).delete():
                    pass
                else:
                    return Response(request.data,status=status.HTTP_404_NOT_FOUND)
                i += 1
                

        
        option_index = request.data['option_index']
        right_option = request.data['options'][option_index]['id']
        if Questions.objects.filter(id=request.data['id']).update(right_option = right_option):
            return Response(request.data)
        else:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(request.data,status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Hosted(request):

    user_id = request.user.id
    hosted_quizzes = HostQuiz.objects.filter(host_id = user_id)

    hosted_quizzes = HostedSerializer3(hosted_quizzes,many=True)
    
    print(hosted_quizzes.data)

    return Response(hosted_quizzes.data)

@api_view(['GET'])
def leaderboard(request,pk):

    quiz_type = HostQuiz.objects.filter(id = pk).values_list('open')
    people = JoinQuiz.objects.filter(quiz_id=pk).order_by('-score')

    people = LeaderboardSerializer(people,many=True)
    scores = people.data
    scores[0]['open'] = quiz_type 
    print(scores)

    # i = 0
    # x = 0
    # y = 0
    # while i == people.data.length:
    #     while people.data[i].score == people.data[i+1].score:
    #         x = i+1
    #         i += 1

    return Response(scores)

@api_view(['DELETE'])
def deletequestion(request,pk):

    question = Questions.objects.get(id=pk).delete()

    return Response(question)

@api_view(['GET'])
def editQuizInfo(request,pk):

    quiz = HostQuiz.objects.get(id=pk)

    quiz = HostedSerializer4(quiz)

    return Response(quiz.data)

@api_view(['POST'])
def editQuizUpdate(request,pk):

    quiz = HostQuiz.objects.get(id=pk)

    quiz = HostedSerializer3(instance = quiz, data= request.data)
    if quiz.is_valid():
        quiz.save()

    return Response(quiz.data)

@api_view(['GET'])
def sendmail(request):

    emails = list(Email.objects.all().values_list())
    print(emails)

    failed = [0]

    for i in emails:

        i = list(i)
        length = 8
        password = ''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(length))
        i.append(password)
        print(i)
        dets = User.objects.create_user(username = i[1],email = i[2],password=i[3])
        dets.save()
        try:
            type = send_mail(
            "test mail",
            "This email is automatically sent by django",
            "dhruv@iamsizzling.com",
            [i[2]],
            html_message = "You have Successfully registered for the quiz. The quiz link is <a href='https://jpmc2.mananraj.co.in/'>www.jpmc2.mananraj.co.in</a>. Using the below credentials you can log into the portal <br><br><br> Username: <b>" + i[1] + " </b><br>Password: <b>" + i[3] + "</b><br><br> This is automatically sent email, Please dont reply here",
            fail_silently = False,
            )
            print(type)
            if type:
                x = "failed"
            else:
                failed.append(i[2])
        except:
            failed.append(i[2])
        
        
    
    
    return Response(failed)