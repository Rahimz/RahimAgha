from rest_framework import generics

from quizes.models import Question
from quizes.serializers import QuestionSerializer


class QuestionListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer