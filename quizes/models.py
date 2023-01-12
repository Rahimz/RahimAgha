from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid 
import random


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.

    """
    created = models.DateTimeField(
        _('created'),
        auto_now_add=True,

    )
    modified = models.DateTimeField(
        _('modified'),
        auto_now=True
    )

    def save(self, *args, **kwargs):
        """
        Overriding the save method in order to make sure that
        modified field is updated even if it is not given as
        a parameter to the update field argument.
        """
        update_fields = kwargs.get('update_fields', None)
        if update_fields:
            kwargs['update_fields'] = set(update_fields).union({'modified'})

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Question(TimeStampedModel):
    # quiz = models.ForeignKey(
    #     Quiz,
    #     on_delete=models.SET_NULL,
    #     related_name='questions',
    #     null=True,
    #     blank=True,
    # )
    description = models.CharField(
        max_length=350,        
    )
    correct = models.CharField(
        _('Correct answer'),
        max_length=350,
    )
    wrong_1 = models.CharField(
        _('Wrong answer 1'),
        max_length=350,
    )
    wrong_2 = models.CharField(
        _('Wrong answer 2'),
        max_length=350,
    )
    wrong_3 = models.CharField(
        _('Wrong answer 3'),
        max_length=350,
    )
    link = models.URLField(
        blank=True, 
        null=True,
    )
    # it sets by admin from 1-5 easy to hard
    difficulty = models.IntegerField(
        default=1,
    )
    uses = models.PositiveIntegerField(
        default=0
    )
    correct_responses = models.PositiveIntegerField(
        default=0
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        unique=True
    )
    published = models.BooleanField(
        default=True
    )


    def __str__(self):        
        return self.description[:35]    
    
    def get_answers(self):
        return random.sample([self.correct, self.wrong_1, self.wrong_2, self.wrong_3], 4)       


class Quiz(TimeStampedModel):
    DIFFICULTY_CHOICES = (
        ('1', _('Easy 1-3-1')),
        ('2', _('Medium 1-2-2')),
        ('3', _('Hard 1-1-3')),
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,  
        editable=False,
        unique=True
    )    
    published = models.BooleanField(
        default=True
    )
    result = models.CharField(
        max_length=10,
        null=True, 
        blank=True
    )
    difficulty = models.CharField(
        max_length=50,
        choices=DIFFICULTY_CHOICES,
        default='1',
    )
    completed = models.BooleanField(
        default=False,
    )
    number_of_questions = models.IntegerField(
        default=5
    )
    questions = models.ManyToManyField(
        Question, 
        related_name='quizes'
    )
    # we need time of quiz to be set
    # session check if there is any quiz or not 
    def __str__(self):
        return str(self.uuid)
    
