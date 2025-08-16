from django.db import models
from tools.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class ChatModel(TimeStampedModel):
    name = models.CharField(
        max_length=150,
        unique=True
    )
    label = models.CharField(
        max_length=150,
    )
    company = models.CharField(
        max_length=150,
    )
    level = models.IntegerField(
        default=0
    )
    output_token = models.FloatField(
        default=0.0
    )
    usage_count = models.IntegerField(
        default=0
    )
    
    
    def __str__(self):
        return f"{self.level}-{self.name}-{self.output_token}"
    class Meta:
        ordering = ('-usage_count', 'level', 'name')


class Chat(TimeStampedModel):
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='chat',
    # )
    model_name= models.CharField(
        max_length=120,
    )
    chat_id = models.CharField(
        _("Chat ID"), max_length=100
    )
    input_token = models.IntegerField(_("Input token"))
    output_token = models.IntegerField(_("Output token"))
    total_token = models.IntegerField(_("Total token"))

    def __str__(self):
        return self.chat_id
    
    def get_first_message(self):
        if self.messages.all():
            return self.messages.first().content[:40]
        
class Message(TimeStampedModel):
    class RoleChoices(models.TextChoices):
        USER = 'user', _("User")
        ASSISTANT = 'assistant', _("Assistant")
        
    class FileChoices(models.TextChoices):
        NA = '', _("Not Applied")
        IMAGE = 'image', _("Image")
        AUDIO = 'audio', _("Audio")
        VIDEO = 'video', _("Video")
        DOC = 'doc', _('Document')
        
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(
        _("Role"),
        choices=RoleChoices.choices,
        default=RoleChoices.USER
    )
    content = models.TextField()
    file_type = models.CharField(
        max_length=12,
        choices=FileChoices.choices,
        default=FileChoices.NA,
    )
    file = models.FileField(
        upload_to='ai/prompts/',
        null=True, 
        blank=True,
    )
    
    def __str__(self):
        return str(self.id)
    
    def get_message_title(self):
        return self.content[:40]
    
    