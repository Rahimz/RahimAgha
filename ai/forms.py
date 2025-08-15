from django import forms
from ai.models import Message, ChatModel

class ChatForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea(attrs={'autofocus': 'autofocus'}))
    file = forms.FileField(required=False)
    file_type = forms.ChoiceField(choices=Message.FileChoices, widget=forms.Select(), required=False)


class ChatModelForm(forms.Form):
    # model = forms.ChoiceField(choices=LIST_OF_MODELS, widget=forms.Select())
    model = forms.ModelChoiceField(
        queryset=ChatModel.objects.all(),
        widget=forms.Select(attrs={'autofocus': 'autofocus'}),
        empty_label="Select a model"
    )
    prompt = forms.CharField(widget=forms.Textarea)
    file = forms.FileField(required=False)
    file_type = forms.ChoiceField(choices=Message.FileChoices, widget=forms.Select(), required=False)
    
    def __init__(self, *args, **kwargs):
        super(ChatModelForm, self).__init__(*args, **kwargs)
        self.fields['model'].initial = ChatModel.objects.first()
