from django.contrib import admin

from .models import Chat, Message, ChatModel

class MessageInline(admin.TabularInline):
    model = Message
    raw_id_fields = ['chat']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_id', 'first_message', 'created', 'model_name', 'input_token', 'output_token', 'total_token']
    inlines = [MessageInline]
    def first_message(self, obj):
        """Get a preview of the first message, limited to 100 characters."""
        if obj.messages.exists():
            # return obj.messages.first().content[:100]  # Get first 100 characters
            return obj.get_first_message()  # Get first 100 characters
        return ""  # Return empty string if no messages exist

    # You can also add a short description if you want to customize the column name
    first_message.short_description = 'First Message Preview'
    
    
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'get_message_title', 'role', 'file_type', 'file']
    search_fields = ['id' , 'chat__chat_id', 'content']
    def get_message_title(self, obj):
        return obj.get_message_title()
    get_message_title.short_description = 'Message Title'
    
    
@admin.register(ChatModel)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'label', 'company']