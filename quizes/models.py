from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
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

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)

DIFFICULTY_CHOICES = (
    (1, _('1')),
    (2, _('2')),
    (3, _('3')),
    (4, _('4')),
    (5, _('5')),
)

class Question(TimeStampedModel):

    # quiz = models.ForeignKey(
    #     Quiz,
    #     on_delete=models.SET_NULL,
    #     related_name='questions',
    #     null=True,
    #     blank=True,
    # )
    description = models.TextField()
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
        choices=DIFFICULTY_CHOICES
    )
    uses = models.PositiveIntegerField(
        default=0
    )
    correct_responses = models.PositiveIntegerField(
        default=0
    )
    no_response = models.PositiveIntegerField(
        default=0
    )
    image = models.ImageField(
        upload_to='book-images/',
        null=True, 
        blank=True
    )
    image_alt = models.CharField(
        max_length=350,
        null=True,
        blank=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        unique=True
    )
    published = models.BooleanField(
        default=True
    )

    objects = models.Manager()
    get_published = PublishedManager()

    @property
    def get_correct_percent(self):
        if self.uses != 0:
            return round(self.correct_responses / self.uses * 100, 1)
        return 0
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
    questions_id = ArrayField(
        models.IntegerField(null=True, blank=True),
        null=True, blank=True
    )
    questions = models.ManyToManyField(
        Question, 
        related_name='quizes'
    )
    final_result = models.PositiveIntegerField(
        default=0
    )
    ip = models.GenericIPAddressField(
        null=True, 
        blank=True
    )
    class Meta:
        ordering = ('-created',)
    # we need time of quiz to be set
    # session check if there is any quiz or not 
    def __str__(self):
        return str(self.uuid)
    


class QuizResponse(TimeStampedModel):
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='responses'
    )
    question = models.ForeignKey(
        Question, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='question_uses'
    )
    answers = ArrayField(
        models.CharField(max_length=350, blank=True),
        null=True,
        blank=True
    )
    step = models.PositiveIntegerField(
        default=1
    )
    done = models.BooleanField(
        default=False
    )
    correct_answer = models.CharField(
        max_length=350,
        null=True, 
        blank=True
    )
    user_response = models.CharField(
        max_length=350,
        null=True, 
        blank=True
    )
    result = models.BooleanField(
        default=False
    )
    def save(self, *args, **kwargs):
        if self.user_response == self.correct_answer:
            self.result = True
        return super().save(*args, **kwargs)
    

class Compliment(models.Model):
    RESULT_DIFFICULTY_CHOICES = (
        (0, _('0')),
        (1, _('1')),
        (2, _('2')),
        (3, _('3')),
        (4, _('4')),
        (5, _('5')),
    )
    content = models.CharField(
        max_length=300,
        unique=True
    )
    # it sets by admin from 1-5 easy to hard
    difficulty = models.IntegerField(
        default=1,
        choices=RESULT_DIFFICULTY_CHOICES
    )
    def __str__(self):
        return self.content[:50]