from django import forms
from ai.models import Message

class ChatForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea)
    file = forms.FileField(required=False)
    file_type = forms.ChoiceField(choices=Message.FileChoices, widget=forms.Select(), required=False)


LIST_OF_MODELS = [
    ('gpt-4o-mini', 'GPT-4O Mini'), 
    ('gpt-4.1-mini-2025-04-14', 'GPT-4.1 Mini (2025-04-14)'),
    ('gpt-4.1-2025-04-14', 'GPT-4.1 (2025-04-14)'),
    ('gemini-2.5-flash-lite', 'Gemini 2.5 Flash Lite'), 
    ('gemini-2.5-flash', 'Gemini 2.5 Flash'),
]
class ChatModelForm(forms.Form):
    model = forms.ChoiceField(choices=LIST_OF_MODELS, widget=forms.Select())
    prompt = forms.CharField(widget=forms.Textarea)
    file = forms.FileField(required=False)
    file_type = forms.ChoiceField(choices=Message.FileChoices, widget=forms.Select(), required=False)
    
    def __init__(self, *args, **kwargs):
        super(ChatModelForm, self).__init__(*args, **kwargs)
        self.fields['model'].initial = 'gpt-4o-mini'
