from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin

from quizes.models import Question
from quizes.serializers import QuestionSerializer
from accounts.permissions import ApiAccessRequiredMixin

class QuestionListAPIView(LoginRequiredMixin, ApiAccessRequiredMixin, generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer