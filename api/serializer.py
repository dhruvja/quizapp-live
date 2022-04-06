from rest_framework import serializers
from django.contrib.auth.models import User
from .models import HostQuiz,JoinQuiz,Option,Questions,Images,Answers

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = '__all__'    

class QuestionSerializer(serializers.ModelSerializer):

    options = OptionSerializer(many=True)
    right_option = serializers.CharField(read_only=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Questions
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

    chosen_option = OptionSerializer(read_only=True)
    question_id = QuestionSerializer(read_only=True)

    class Meta:
        model = Answers
        fields = '__all__'

class HostedSerializer1(serializers.ModelSerializer):

    quizdata = AnswerSerializer(many=True,read_only=True)

    class Meta:
        model = HostQuiz
        fields = '__all__'

class ListQuizSerializer(serializers.ModelSerializer):

    starttime = serializers.DateTimeField(format="%d-%m-%Y  %H:%M", required=False, read_only=True)
    endtime = serializers.DateTimeField(format="%d-%m-%Y  %H:%M", required=False, read_only=True)

    class Meta:
        model = HostQuiz
        fields = '__all__'
    
class QuestionSerializer1(serializers.ModelSerializer):

    class Meta:
        model = Questions 
        fields = ('id','right_option','question','points')
        
class AnswerSerializer2(serializers.ModelSerializer):

    chosen_option = OptionSerializer(read_only=True)
    question_id = QuestionSerializer1(read_only=True)

    class Meta:
        model = Answers
        fields = '__all__'

class JoinedSerializer1(serializers.ModelSerializer):

    entered_answers = AnswerSerializer2(read_only=True,many=True)
    quiz_id = ListQuizSerializer(read_only=True)
    candidate_id = serializers.CharField(read_only=True) 
    

    class Meta:
        model = JoinQuiz
        fields = '__all__'

class JoinedSerializer(serializers.ModelSerializer):

    quiz_id = HostedSerializer1(read_only=True)
    
    class Meta:
        model = JoinQuiz
        fields = '__all__'       


class HostedSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True)
    host_id = serializers.CharField(read_only=True)
    joined_quiz_name = JoinedSerializer(many=True)
   

    class Meta:
        model = HostQuiz
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):

    quizzes = HostedSerializer(many=True)
    joined = JoinedSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'

class RegisterSerializer1(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )
        return user


class HostedSerializer2(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True)
    host_id = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(format="%d-%m-%Y  %H:%M:%s", required=False, read_only=True)
   

    class Meta:
        model = HostQuiz
        fields = '__all__'

class ChosenAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answers
        fields = ('id','joinquiz_id','quiz_id','question_id','chosen_option','time_elapsed')

class JoinQuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = JoinQuiz
        fields = ('id','candidate_id','quiz_id')

class AnswerSerializer1(serializers.ModelSerializer):

    class Meta:
        model = Answers
        fields = '__all__'

class JoinedSerializer2(serializers.ModelSerializer):

    quiz_id = ListQuizSerializer(read_only=True)

    class Meta:
        model = JoinQuiz
        fields = '__all__'

class HostedSerializer3(serializers.ModelSerializer):

    # starttime = serializers.DateTimeField(format="%d-%m-%Y  %H:%M", required=False, read_only=True)
    # endtime = serializers.DateTimeField(format="%d-%m-%Y  %H:%M", required=False, read_only=True)
    
    class Meta:
        model = HostQuiz
        fields = '__all__'


class QuestionSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Questions
        fields = '__all__'

class LeaderboardSerializer(serializers.ModelSerializer):

    candidate_id = serializers.CharField(read_only=True) 

    class Meta:
        model = JoinQuiz
        fields = '__all__'

class HostedSerializer4(serializers.ModelSerializer):

    starttime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M", required=False, read_only=True)
    endtime = serializers.DateTimeField(format="%Y-%m-%dT%H:%M", required=False, read_only=True)
    
    class Meta:
        model = HostQuiz
        fields = '__all__'