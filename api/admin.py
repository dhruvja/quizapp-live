from django.contrib import admin
from .models import HostQuiz,JoinQuiz,Option,Questions,Images,Answers,Email
# Register your models here.

admin.site.register(HostQuiz) 
admin.site.register(JoinQuiz)
admin.site.register(Option)
admin.site.register(Questions)
admin.site.register(Images)
admin.site.register(Answers)
admin.site.register(Email)
