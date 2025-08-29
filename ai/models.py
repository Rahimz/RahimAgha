from django.db import models
from tools.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from pathlib import Path

User = get_user_model()




def FileTypeDetermine(uploaded_file):
     # Check and set the file type
    file_type = Message.FileChoices.NA  # Default to Not Applied
    if uploaded_file:
        file_extension = Path(uploaded_file.name).suffix.lower()
        # content_type = uploaded_file.content_type

        # Determine file type based on extension or content type
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
            file_type = Message.FileChoices.IMAGE
        elif file_extension in ['.mp3', '.wav']:
            file_type = Message.FileChoices.AUDIO
        elif file_extension in ['.mp4', '.avi', '.mov']:
            file_type = Message.FileChoices.VIDEO
        elif file_extension in ['.doc', '.docx', '.txt']:
            file_type = Message.FileChoices.DOC
        elif file_extension in ['.pdf',]:
            file_type = Message.FileChoices.PDF
        else:
            file_type = Message.FileChoices.NA
    return file_type




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
    input_token = models.FloatField(
        default=0.0
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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chats',
    )
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
        IMAGE = 'image', _("Image") #['.jpg', '.jpeg', '.png', '.gif']
        AUDIO = 'audio', _("Audio") #['.mp3', '.wav']
        VIDEO = 'video', _("Video") #['.mp4', '.avi', '.mov', .mkv]
        DOC = 'doc', _('Document') # ['.doc', '.docx', '.txt']
        PDF = 'pdf', _('PDF') #['.pdf']
        
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
    
    
    
    def save(self, *args, **kwargs):
        # Determine file type before saving
        if self.file:
            self.file_type = FileTypeDetermine(self.file)
        super().save(*args, **kwargs)