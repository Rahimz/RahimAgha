from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from langchain_openai import ChatOpenAI

from .forms import ChatForm

API_KEY = settings.AVAL_API_KEY

@staff_member_required
def AiView(request):
    context = dict(
        page_title = 'ai'
    )
    messages = None
    ai_message = None
    # Initialize the ChatOpenAI model
    model_name = "gpt-4o-mini"
    # model_name = "claude-3-opus"
    llm = ChatOpenAI(
        model=model_name, base_url="https://api.avalai.ir/v1", api_key=API_KEY
    )
    if request.method == 'POST':
        form = ChatForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Initialize messages list with system and user prompts
            messages = [        
                {"role": "user", "content": cd['prompt']},
            ]
            # Initialize messages list with system and user prompts
            # messages = [        
            #     {"role": "user", "content": "in less than 30 words define django rest framework serializer"},
            # ]
            
            # ai_message = llm.invoke(messages)
            form = ChatForm()
    else: 
        form = ChatForm()
    context.update(
        model_name=model_name,
        messages=messages,
        ai_message=ai_message,
        form=form
    )
    return render(
        request,
        'ai/ai_home.html',
        context
    )






