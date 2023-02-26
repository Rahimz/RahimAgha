from rest_framework import serializers

from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    # answers = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Question
        
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        fields = [
            'description',
            # 'answers',
            # 'correct', 
            # 'wrong_1',
            # 'wrong_2',
            # 'wrong_3',
            # 'link',
            'difficulty',
            # 'image',
            # 'image_alt',
            'uuid',
        ]

        def get_answers(self, obj):
            if not hasattr(obj, 'id'):
                return None
            return obj.get_answers()