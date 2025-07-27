from django.db import models
from tools.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _



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
        
    # class FileChoices(models.TextChoices):
        # IMAGE = 'image', _("Image")
        # AUDIO = 'audio', _("Audio")
        # VIDEO = 'video', _("Video")
        # DOC = 'doc', _('Document')
        
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
    # file_type = models.CharField(
    #     max_length=12,
    #     choices=FileChoices.choices,
    # )
    # file = models.FileField(
    #     upload_to='ai/prompts/'
    # )
    
    def __str__(self):
        return str(self.id)
    
    