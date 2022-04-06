from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HostQuiz(models.Model):
    quizname = models.CharField(max_length=255)
    quizdetails = models.TextField()
    host_id = models.ForeignKey(User,related_name='quizzes',on_delete=models.CASCADE)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    open = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quizname

class JoinQuiz(models.Model):
    candidate_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='joined')
    quiz_id = models.ForeignKey(HostQuiz,on_delete=models.CASCADE,related_name='joined_quiz_name')
    score = models.IntegerField(default=-1,null=True,blank=True)
    time_taken = models.FloatField(default=0,blank=True,null=True)
    last_joined = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)


class Questions(models.Model):
    question = models.TextField()
    quiz_id = models.ForeignKey(HostQuiz,related_name="questions",on_delete=models.CASCADE)
    right_option = models.ForeignKey('Option',related_name="rightoption",on_delete=models.SET_NULL,null=True,blank=True)
    option_index = models.IntegerField(default=0)
    image = models.BooleanField(default=False)
    points = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Option(models.Model):
    question_id = models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='options')
    option = models.CharField(max_length=2500)

    def __str__(self):
        return self.option


class Images(models.Model):
    question_id = models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/")


class Answers(models.Model):
    quiz_id = models.ForeignKey(HostQuiz,on_delete=models.CASCADE,related_name="quizdata")
    joinquiz_id = models.ForeignKey(JoinQuiz,on_delete=models.CASCADE,related_name='entered_answers',default=5)
    question_id = models.ForeignKey(Questions,on_delete=models.CASCADE)
    chosen_option = models.ForeignKey(Option,on_delete=models.CASCADE,blank=True,null=True)
    result = models.BooleanField(default=False)
    time_elapsed = models.FloatField(default=0,blank = True, null=True) 
    created_date = models.DateTimeField(auto_now=True)

class Email(models.Model):
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length=255)







